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

#include "YPythonNamespace.h"
#include "ytypes.h"
#include "yast.h"

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
    //Py_Finalize();
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
              //string err = PyErrorHandler();
              y2error("Python error: %s", PyErrorHandler().c_str());
               //PyErr_Print();
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
    PyObject* pArgs = NULL;      // tuple object of argument for function
    PyObject* pReturn;    // return value from python
    YCPValue result = YCPNull ();

    // obtain correct dictionary for module
    pMainDict = PyDict_GetItemString(YPython::yPython()->pMainDicts(),module.c_str());

    // obtain function from dictionary
    if (PyDict_Contains(pMainDict,PyString_FromString(function.c_str())))
       pFunc = PyDict_GetItemString(pMainDict, function.c_str());
	else {
	   y2error("Function %s is not found.", function.c_str());
	   return result;
	}

    if (argList->size() !=0)
       pArgs = PyTuple_New(argList->size()-1);

    // Parsing argumments
    PyObject *pArg;

    for ( int i=1; i < argList->size(); i++ ) {
        pArg = ycp_to_pyval(argList->value(i));
        PyTuple_SetItem(pArgs,i-1, pArg);
    }

    // calling function from python
    if (PyCallable_Check(pFunc))
       pReturn = PyObject_Call(pFunc, pArgs, NULL);
	else {
	   y2error("Function %s is not callable.", function.c_str());
	   return result;
	}
    // delete arguments
    Py_CLEAR(pArgs);

    // convert python value to YCPValue
    if (pReturn)
        result = pyval_to_ycp(pReturn); // create YCP value
    else{
        y2error("PyObject_CallObject(pFunc, pArgs) failed!");
        if (PyErr_Occurred() != NULL){
           y2error("Python error: %s", PyErrorHandler().c_str());
           //PyErr_Print();
        }
    }
    // delete pReturn
    Py_CLEAR(pReturn);

    if (result.isNull ()) {
       result = YCPVoid ();
    }

    return result;
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



string YPython::PyErrorHandler() {
   /* process Python-related errors */
   /* call after Python API raises an exception */
 
   PyObject *errobj, *errdata, *errtraceback, *pystring;

   string result = "error type: ";
   /* get latest python exception info */
   PyErr_Fetch(&errobj, &errdata, &errtraceback);
 
   pystring = NULL;
   if (errobj != NULL &&
      (pystring = PyObject_Str(errobj)) != NULL &&     /* str(object) */
      (PyString_Check(pystring))
      )
       //strcpy(save_error_type, PyString_AsString(pystring));
      result += PyString_AsString(pystring);
   else
      result += "<unknown exception type>";
   Py_XDECREF(pystring);
   result +="; error value: ";

   pystring = NULL;
   if (errdata != NULL &&
      (pystring = PyObject_Str(errdata)) != NULL &&
      (PyString_Check(pystring))
      )
       //strcpy(save_error_info, PyString_AsString(pystring));
      result += PyString_AsString(pystring);
   else
       //strcpy(save_error_info, "<unknown exception data>");
      result += "<unknown exception value>";
   Py_XDECREF(pystring);

   result +="; error traceback: ";

   pystring = NULL;
   if (errdata != NULL &&
      (pystring = PyObject_Str(errtraceback)) != NULL &&
      (PyString_Check(pystring))
      )
       //strcpy(save_error_info, PyString_AsString(pystring));
      result += PyString_AsString(pystring);
   else
       //strcpy(save_error_info, "<unknown exception data>");
      result += "<unknown exception traceback>";
   Py_XDECREF(pystring);
   //printf("%s\n%s\n", save_error_type, save_error_info);
   Py_XDECREF(errobj);
   Py_XDECREF(errdata);         /* caller owns all 3 */
   Py_XDECREF(errtraceback);    /* already NULL'd out */
   return result;

}

