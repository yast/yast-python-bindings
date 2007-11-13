/*---------------------------------------------------------------------\
|								       |
|			__   __	  ____ _____ ____		       |
|			\ \ / /_ _/ ___|_   _|___ \		       |
|			\ V / _` \___ \ | |   __) |		       |
|			 | | (_| |___) || |  / __/		       |
|			 |_|\__,_|____/ |_| |_____|		       |
|								       |
|				core system			       |
|						     (C) SuSE Linux AG |
\----------------------------------------------------------------------/

  File:	      YPython.cc



/-*/

#include <Python.h>
#include <stdlib.h>
#include <list>
#include <iosfwd>
#include <sstream>
#include <iomanip>




#define y2log_component "Y2Python"
#include <ycp/y2log.h>
#include <ycp/pathsearch.h>


#include <YPython.h>
#include <ycp/YCPValue.h>
#include <ycp/YCPBoolean.h>
#include <ycp/YCPByteblock.h>
#include <ycp/YCPFloat.h>
#include <ycp/YCPInteger.h>
#include <ycp/YCPList.h>
#include <ycp/YCPMap.h>
#include <ycp/YCPPath.h>
#include <ycp/YCPString.h>
#include <ycp/YCPSymbol.h>
#include <ycp/YCPTerm.h>
#include <ycp/YCPVoid.h>
#include <ycp/YCPCode.h>
#include <ycp/YCPExternal.h>
#include <ycp/Point.h>

#include "YCPTypes.h"
#include "YPythonNamespace.h"
#include "YCPDeclarations.h"

#include <iostream>
#define DBG(str) \
    std::cerr << __FILE__ << ": " << __LINE__ << ": " << str << std::endl; \
    std::cerr.flush()

YPython * YPython::_yPython = 0;

PyObject * YPython::_pMainDicts = NULL;

YPython::YPython(){}


YPython::~YPython(){}


/**
 * return static _yPython
 **/

YPython *
YPython::yPython()
{
    if ( ! _yPython )
	_yPython = new YPython();

    return _yPython;
}

/**
 * return static _pMainDicts
 **/

PyObject* 
YPython::pMainDicts()
{

    return _pMainDicts;
}

/**
 * "static" destructor
 **/


YCPValue
YPython::destroy()
{
    y2milestone( "Shutting down embedded Python interpreter." );

    if ( _yPython )
	delete _yPython;

    _yPython = 0;
    Py_Finalize();
    return YCPVoid();
}



/**
 * Loads a module.
 **/
YCPValue
YPython::loadModule(string module)
{
    string path;
    string module_name;
    PyObject* pModuleName;
    size_t found;
    PyObject* pMain;

    //found last "/" in path
    found = module.find_last_of("/");
    //extract directory from path module
    path = module.substr(0,found+1);
    //extract module name from path
    module_name = module.substr(found+1);
    //delete last 3 chars from module name ".py"
    module_name.erase(module_name.size()-3); //delete ".py"

    //initialize python and set the path where are python modules
    if (!Py_IsInitialized()) {
       setenv("PYTHONPATH", path.c_str(), 1);       
       Py_Initialize();
       if (!YPython::_pMainDicts)
          YPython::_pMainDicts = PyDict_New();
    }

    if (!YPython::_pMainDicts)
       YPython::_pMainDicts = PyDict_New();
    //create python string for name of module 
    pModuleName = PyString_FromString(module_name.c_str());
    //check if dictionary contain "dictionary" for module
    if (PyDict_Contains(YPython::_pMainDicts, pModuleName) == 0) {
       pMain = PyImport_ImportModule(module_name.c_str());
       if (pMain == NULL){
           y2error("Can't import module %s", module_name.c_str());

           if (PyErr_Occurred() != NULL){
               PyErr_Print();
           }

           return YCPError("The module was not imported");
       }

       int ret = PyDict_SetItem(YPython::_pMainDicts, pModuleName, PyModule_GetDict(pMain));
       if (ret != 0)
          return YCPError("The module was not imported");
    } else {

       //return YCPError("The module is imported");
       y2error("The module is imported");
       return YCPVoid();
    }


    return YCPVoid();
 
}

/**
 * evaluate of function from python
 * @param string name of module
 * @param string name of function
 * @param bool is it method? TODO !!
 * @param YCPList argumnets from YCP to python function(0 - dummy)
 * @return YCPValue return value from python's function
 **/
YCPValue
YPython::callInner (string module, string function, bool method,
		  YCPList argList)
{
    PyObject* pMainDict;  // dictionary of module
    PyObject* pFunc;      // function from dictionary
    PyObject* pArgs;      // tuple object of argument for function
    PyObject* pReturn;    // return value from python
    YCPValue result = YCPNull ();

    //obtain correct dictionary for module
    pMainDict = PyDict_GetItemString(YPython::yPython()->pMainDicts(),module.c_str());
    //obtain function from dictionary
    pFunc = PyDict_GetItemString(pMainDict, function.c_str());
    pArgs = PyTuple_New(argList->size()-1);

    //Parsing argumments
    PyObject *pArg;
    y2milestone ("name of function %s and number of arguments %d", function.c_str(), argList->size()-1);
    for ( int i=1; i < argList->size(); i++ ) {
        pArg = YCPTypeToPythonType(argList->value(i));
        PyTuple_SetItem(pArgs,i-1, pArg);
    }
    //calling function from python
    pReturn = PyObject_CallObject(pFunc, pArgs);
    //delete arguments
    Py_CLEAR(pArgs);
    //convert python value to YCPValue
    if (pReturn)
        result = PythonTypeToYCPType(pReturn); // create YCP value
    else
        y2error("pReturn == 0");
    //delete pReturn
    Py_CLEAR(pReturn);

    if (result.isNull ()) {
        y2error ("Result is NULL when returning from %s", function.c_str());
        result = YCPVoid ();
    }

    return result;
}


/**
 * convert python value to YCPValue
 * @param pythonValue
 * @return YCPValue covnerted value from pythonValue
 **/

YCPValue YPython::PythonTypeToYCPType(PyObject *pythonValue)
{
    // null (in python None)
    if (pythonValue == Py_None)
        return YCPNull();

    //boolean
    if (PyBool_Check(pythonValue)){
        int cmp_result = PyObject_Compare(pythonValue, Py_True);
        if (PyErr_Occurred() != NULL){
            return YCPNull();
        }
        if (cmp_result == 0){
            return YCPBoolean(true);
        }else{
            return YCPBoolean(false);
        }
    }

    // integer
    if (PyInt_Check(pythonValue))
        return YCPInteger(PyInt_AsLong(pythonValue));

    //float
    if (PyFloat_Check(pythonValue))
        return YCPFloat(PyFloat_AsDouble(pythonValue));

    //string
    if (PyString_Check(pythonValue))
        return YCPString(PyString_AsString(pythonValue));

    //functions ->Reference
    if (PyFunction_Check(pythonValue))
	return fromPythonFunToReference (pythonValue);

    //function
    if (PyFunction_Check(pythonValue))
        return YCPByteblock((const unsigned char *)PyFunction_GetCode(pythonValue), (long) sizeof(PyFunction_GetCode(pythonValue)));

    //list
    if (PyList_Check(pythonValue))
        return fromPythonListToYCPList(pythonValue);

    //tuple -> list
    if (PyTuple_Check(pythonValue))
        return fromPythonTupleToYCPList(pythonValue);

    //dict -> map
    if (PyDict_Check(pythonValue))
        return fromPythonDictToYCPMap(pythonValue);

    

    // term, symbol, path
    switch (getYCPType(pythonValue)){
        case SYMBOL:
            return YCPSymbol(Symbol_getValue((Symbol *)pythonValue));
        case PATH:
            return YCPPath(Path_getValue((Path *)pythonValue));
        case TERM:
            return fromPythonTermToYCPTerm(pythonValue);
	case CODE:
            return YCPCode(new YPythonCode(Code_getValue((Code *)pythonValue)));

        case NOT_YCP_TYPE:
            return YCPNull();
    }

    return YCPNull();
}
/**
 * convert YCPValue to python value 
 * @param YCPValue
 * @return pythonValue covnerted value from YCPValue
 **/

PyObject *YPython::YCPTypeToPythonType(YCPValue value)
{
    // null -> None
    if (value.isNull())
        return Py_None;
    //void -> None
    if (value->isVoid())
        return Py_None;

    // boolean
    if (value->isBoolean()){
        if (value->asBoolean()->value())
            return PyBool_FromLong(1);
        return PyBool_FromLong(0);
    }

    //integer
    if (value->isInteger())
        return PyInt_FromLong(value->asInteger()->value());

    //float
    if (value->isFloat())
        return PyFloat_FromDouble(value->asFloat()->value());

    //string
    if (value->isString())
        return PyString_FromString(value->asString()->value().c_str());

    //list -> tuple
    if (value->isList())
        return fromYCPListToPythonTuple(value->asList());

    //map -> dict
    if (value->isMap())
        return fromYCPMapToPythonDict(value->asMap());

    //path
    if (value->isPath())
        return Path_NewString(value->asPath()->toString().c_str());

    //symbol
    if (value->isSymbol())
        return Symbol_NewString(value->asSymbol()->toString().erase(0,1).c_str());

    //term
    if (value->isTerm())
        return fromYCPTermToPythonTerm(value->asTerm());

    return Py_None;
}





/********** PRIVATE: **********/

/**
  * Convert a Python list to a YCPList.
  * @param PyObject (python list)
  * @return YCPList covnerted value from pythonValue
 **/
YCPList YPython::fromPythonListToYCPList (PyObject* pPythonList) {
    YCPList ycp_List;
    PyObject * pItem;
    YCPValue ycp_value;

    //checking for list (is it really list?)
    if (PyList_Check(pPythonList) > 0) {
        int list_size = PyList_Size(pPythonList);
        for (int i = 0; i < list_size; i++) {
            pItem = PyList_GetItem(pPythonList, i);
            ycp_value = PythonTypeToYCPType(pItem);

            if (!ycp_value.isNull ()) {
                ycp_List->add(ycp_value);
            } else {
                return YCPNull ();
            }
        }
    }else{
        y2milestone ("Value is not Python List");
        return YCPNull ();
    }

    return ycp_List;
}

/**
  * Convert a Python Tuple to a YCPList.
  * @param PyObject (python tuple)
  * @return YCPList covnerted value from pythonValue
 **/
YCPList YPython::fromPythonTupleToYCPList (PyObject* pPythonTuple) {
    YCPList ycp_List;
    PyObject * pItem;
    YCPValue ycp_value;

    //checking for list (is it really list?)
    if (PyTuple_Check(pPythonTuple) > 0) {
        int list_size = PyTuple_Size(pPythonTuple);
        for (int i = 0; i < list_size; i++) {
            pItem = PyTuple_GetItem(pPythonTuple, i);
            ycp_value = PythonTypeToYCPType(pItem);

            if (!ycp_value.isNull ()) {
                ycp_List->add(ycp_value);
            } else {
                return YCPNull ();
            }
        }
    }else{
        y2milestone ("Value is not Python Tuple");
        return YCPNull ();
    }

    return ycp_List;
}

/**
  * Convert a YCPList to a Python list.
  * @param YCPValue (list)
  * @return PyObject (python list) covnerted value from YCPValue
 **/
PyObject* YPython::fromYCPListToPythonList (YCPValue ycp_List) {
    PyObject* pPythonList;
    PyObject* pItem;
    int ret = 0;

    if (ycp_List->isList()) {
        pPythonList = PyList_New(ycp_List->asList()->size());

        y2milestone ("Size of list %d",ycp_List->asList()->size());
        for ( int i = 0; i < ycp_List->asList()->size(); i++ ) {
            pItem = YCPTypeToPythonType(ycp_List->asList()->value(i));
            ret = PyList_SetItem(pPythonList, i, pItem);

            if (ret <0)
                y2error("PyList_SetItem doesn't add item into python list.");
        }
        Py_INCREF(pPythonList); //TODO: Review this - is it really needed? PyList_New returns New Reference.
        return pPythonList;

    } else {
        y2milestone ("Value is not YCPList");
        return Py_None;
    }
}

/**
  * Convert a YCPList to a Python tuple.
  * @param YCPValue (list)
  * @return PyObject (python tuple) covnerted value from YCPValue
 **/
PyObject* YPython::fromYCPListToPythonTuple (YCPValue ycp_List) {
    PyObject* pPythonTuple;
    PyObject* pItem;
    int ret = 0;

    if (ycp_List->isList()) {
        pPythonTuple = PyTuple_New(ycp_List->asList()->size());

        y2milestone ("Size of list %d",ycp_List->asList()->size());
        for ( int i = 0; i < ycp_List->asList()->size(); i++ ) {
            pItem = YCPTypeToPythonType(ycp_List->asList()->value(i));
            ret = PyTuple_SetItem(pPythonTuple, i, pItem);

            if (ret <0)
                y2error("PyList_SetItem doesn't add item into python list.");  
        }
        Py_INCREF(pPythonTuple); //TODO: Review this.
        return pPythonTuple;

    } else {
        y2milestone ("Value is not YCPList");
        return NULL;
    }
}


/**
  * Convert a YCPMap to a Python Dictionary.
  * If something goes wrong, iteration is trying proceed...
  * @param YCPValue (map)
  * @return PyObject (python dictionary) covnerted value from YCPValue
 **/
PyObject* YPython::fromYCPMapToPythonDict (YCPValue ycp_Map) {
    PyObject* pPythonDict;
    PyObject* pKey;
    PyObject* pValue;
    int ret = -1;

    if (ycp_Map->isMap()) {
        pPythonDict = PyDict_New();

        for (YCPMapIterator it = ycp_Map->asMap()->begin(); it != ycp_Map->asMap()->end(); ++it ) {
            pKey = YCPTypeToPythonType(it.key());
            pValue = YCPTypeToPythonType(it.value());

            if (pValue && pKey){
                ret = PyDict_SetItem(pPythonDict, pKey, pValue);

                if (ret < 0)
                    y2error("Adding value and key from YCPMap to Python Dictionary falsed.");
            }else{
                y2error("Transformation key and/or value to python type failed.");
            }
        }
    }else{
        y2milestone ("Value is not YCPMap");
        return Py_None;
    }

    Py_INCREF(pPythonDict);// TODO: Review this
    return pPythonDict;
}


/**
  * Convert a Python Dictionary to a YCPMap.
  * @param PyObject (python dictionary)
  * @return YCPMap covnerted value from PyObject
 **/
YCPMap YPython::fromPythonDictToYCPMap (PyObject* pPythonDict) {
    YCPValue ycp_key;
    YCPValue ycp_value;
    YCPMap ycp_Map;

    if (PyDict_Check(pPythonDict)>0) {
        if (PyDict_Size(pPythonDict) == 0)
            return ycp_Map;

        PyObject *key, *value;
        Py_ssize_t pos = 0;

        while (PyDict_Next(pPythonDict, &pos, &key, &value)) {
            ycp_key = PythonTypeToYCPType(key);
            ycp_value = PythonTypeToYCPType(value);

            ycp_Map->add(ycp_key, ycp_value);
        }
    }else{
        y2milestone ("Value is not python dictionary");
        return YCPNull();
    }

    return ycp_Map;
}


/**
  * Convert a Python Term to a YCPTerm.
  * Argument should be Term!
  * @param PyObject (python Term)
  * @return YCPTerm covnerted value from PyObject
 **/
YCPTerm YPython::fromPythonTermToYCPTerm (PyObject* pythonTerm) {
    PyObject *value;
    string name;
    YCPValue ycp_value;

    if (!isTerm(pythonTerm)){
        y2error("Argument is not Term!");
        return YCPNull();
    }

    name = Term_getName((Term *)pythonTerm);
    value = Term_getValue((Term *)pythonTerm);
    ycp_value = fromPythonTupleToYCPList(value);

    if (!ycp_value.isNull())
        return YCPTerm(name, ycp_value->asList());

    return YCPNull();
}


/**
  * Convert a YCPTerm to a Python Term.
  * Given argument should be term!
  * @param YCPValue (Term)
  * @return PyObject (python dictionary) covnerted value from YCPValue
 **/
PyObject* YPython::fromYCPTermToPythonTerm (YCPValue ycp_Term) {
    PyObject *value;

    if (!ycp_Term->isTerm()){
        y2error("Argument is not term!");
        return Py_None;
    }

    value = fromYCPListToPythonTuple(ycp_Term->asTerm()->args());
    if (value == Py_None){
        y2error("fromYCPListToPythonTuple FIALED");
        return Py_None;
    }

    return Term_NewString(ycp_Term->asTerm()->name().c_str(), value);
}

/**
 * init namespace
 * @param char * name of module
 * @param char * name of function
 * @return namespace of YCP
 */

static Y2Namespace * getNs (const char * ns_name) {
  Import import(ns_name);	// has a static cache
  Y2Namespace *ns = import.nameSpace();
  if (ns == NULL) {
     y2error ("... for a Python call of %s", ns_name);
  } else {
     ns->initialize ();
  }
  return ns;
}


/**
 * Find function in Global Dictionary
 * confirm if function is from imported module or not
 * return 1 if module is in dictionary and function too
 * retrun 0 if module is in dictionary and function not
 * return -1 if missing both (module and dinctionary)
**/

int YPython::findModuleFuncInDict(string module, string function) {

    PyObject * pModuleName = PyString_FromString(module.c_str());
    if (_pMainDicts==NULL)
       return -1;
    if (PyDict_Contains(_pMainDicts, pModuleName)) {

       PyObject * pMainDict = PyDict_GetItemString(_pMainDicts, module.c_str());
       if (PyDict_Contains(pMainDict, PyString_FromString(function.c_str())))
          return 1;
       else
          return 0;

    } else {

       return -1;
    }

}

/**
  * Adding module name and function into 
  * global dictionary 
  * (necessary for calling python function via reference)
 **/
bool YPython::addModuleAndFunction(string module, string fun_name, PyObject* function) {

  
    PyObject * pModuleName = PyString_FromString(module.c_str());
    //check if dictionary contain "dictionary" for module

    if (_pMainDicts==NULL) {
       _pMainDicts = PyDict_New();
    }

    if (PyDict_Contains(_pMainDicts, pModuleName)) {       
       PyObject * pMainDict = PyDict_GetItemString(_pMainDicts, module.c_str());

       if (PyDict_Contains(pMainDict, PyString_FromString(fun_name.c_str()))) {
	  return true;

       } else {
          //PyObject * newDict = PyDict_New();
          if (PyDict_SetItemString(pMainDict, fun_name.c_str(), function) < 0) {
             y2error("Adding new function %s to local dictionary", fun_name.c_str());
             return false;
          }

          if (PyDict_DelItemString(_pMainDicts, module.c_str()) <0) {
             y2error("Deleting local dictionary %s from global dictionary failed", module.c_str());
             return false;
          }

          if (PyDict_SetItemString(_pMainDicts, module.c_str(), pMainDict) <0) {
             y2error("Adding new local dictionary %s to global dictionary", module.c_str());
             return false;
          }

          return true;
       }
    } else {
       PyObject * newDict = PyDict_New();

       if (PyDict_SetItemString(newDict, fun_name.c_str(), function) < 0) {
             y2error("Adding new function %s to local dictionary", fun_name.c_str());
             return false;
       }       

       if (PyDict_SetItemString(_pMainDicts, module.c_str(), newDict) <0) {
             y2error("Adding new local dictionary %s to global dictionary", module.c_str());
             return false;
       }

       return true;
    }
}

YCPValue YPython::findSymbolEntry(Y2Namespace *ns, string module, string function) {

  if (ns) {
     TableEntry *sym_te = ns->table ()->find (function.c_str());

     if (sym_te == NULL) {
	y2error ("No such symbol %s::%s", module.c_str(), function.c_str());
	return YCPNull();
     }

     SymbolEntryPtr sym_entry = sym_te->sentry();
     //cout << "entry" << sym_entry->toString()<< endl;
     return YCPReference(sym_entry);

  } else {
     y2error("Creating/Importing namespace for function %s failed", function.c_str());
     return YCPNull();
  }
}

/**
  * Convert Python Function to YCPCode.
  * 
  * @param pointer to python function
  * @return YCPReference - Referecne
 **/

YCPValue YPython::fromPythonFunToReference (PyObject* pyFun) {
    
    PyObject *fun_code = PyFunction_GetCode(pyFun);
    string fun_name = PyString_AsString(((PyCodeObject *) fun_code)->co_name);
    string file_path = PyString_AsString(((PyCodeObject *) fun_code)->co_filename);
    //int no_args = ((PyCodeObject *) fun_code)->co_argcount;

    //found last "/" in path
    size_t found = file_path.find_last_of("/");
    //extract module name from path
    string module_name = file_path.substr(found+1);
    //delete last 3 chars from module name ".py"
    module_name.erase(module_name.size()-3);

    int find = findModuleFuncInDict(module_name, fun_name);
  
    FunctionTypePtr sym_tp;
    Y2Namespace *ns;

    //namespace exist and includes function
    if (find == 1) {
       ns = getNs (module_name.c_str());

       return findSymbolEntry(ns, module_name, fun_name);

    //namespace exist but doesn't include function
    } else if (find ==0) {
       addModuleAndFunction(module_name, fun_name, pyFun);

       ns = getNs (module_name.c_str());

       if (ns) {

          SymbolEntry *result = ((YPythonNamespace *)ns)->AddFunction(pyFun);
          if (result)
             return YCPReference(result);
          else {
             y2error("Adding function %s to namespace %s failed", fun_name.c_str(), module_name.c_str());
             return YCPNull();
          }
             
       } else {
          y2error("Importing namespace %s for function %s failed",
                  module_name.c_str(), fun_name.c_str());
          return YCPNull();
       }

    //namespace and function don't exist
    } else {

       addModuleAndFunction(module_name, fun_name, pyFun);
       ns = new YPythonNamespace(module_name, pyFun);

       //register new namespace
       Import import(module_name, ns);

       return findSymbolEntry(ns, module_name, fun_name);

    }

    return YCPNull();
}



YPythonCode::YPythonCode (PyObject *pFunc):YCode() {
    m_kind = YCode::yeReference;
    _pFunc = pFunc;
}

YCPValue YPythonCode::evaluate(bool cse) {

    PyObject * pReturn = NULL;
    YCPValue result = YCPVoid();
    PyObject * pFunction = NULL;
    PyObject * pArgs = NULL;
    int args_size;
        
    args_size = PyTuple_Size(_pFunc);

    if (args_size >=1) {
       pFunction = PyTuple_GetItem(_pFunc, 0);
       if (args_size > 1) {
          pArgs = PyTuple_GetSlice(_pFunc, 1, args_size);
       }
    }
    if (Py_IsInitialized()) {
       pReturn = PyObject_CallObject(pFunction, pArgs);
       //convert python value to YCPValue
       if (pReturn) {
          result = YPython::yPython()->PythonTypeToYCPType(pReturn); // create YCP value
       } else {
          y2error("pReturn == 0");
       }
    }
    return result;

}

YCode::ykind YPythonCode::kind() const {

    return m_kind;
}

std::ostream & YPythonCode::toStream (std::ostream & str) const {

    return str;
}

std::ostream & YPythonCode::toXml (std::ostream & str, int indent ) const {

    return str;

}
