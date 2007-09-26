/*---------------------------------------------------------------------\
|								       |
|		       __   __	  ____ _____ ____		       |
|		       \ \ / /_ _/ ___|_   _|___ \		       |
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
YPython * YPython::_yPython = 0;

YPython::YPython() {

  PyObject* pMain;
  PyObject* pMainDict;
  pMain = PyImport_AddModule("__main__");
  PyRun_SimpleString("from ycp import *");
  pMainDict = PyModule_GetDict(pMain);
  pPathClass = PyDict_GetItemString(pMainDict, "Path");
  pSymbolClass = PyDict_GetItemString(pMainDict, "Symbol");
  pTermClass = PyDict_GetItemString(pMainDict, "Term");
  
}


YPython::~YPython() {  

  Py_CLEAR(pPathClass);
  Py_CLEAR(pSymbolClass);
  Py_CLEAR(pTermClass);

}


YPython *
YPython::yPython()
{
    if ( ! _yPython )
	_yPython = new YPython();

    return _yPython;
}



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
 */
YCPValue
YPython::loadModule( YCPList argList )
{
    Py_Initialize();

    return YCPVoid();
}

/**
 * evaluate of function from python
 * @param string name of module
 * @param string name of function
 * @param bool is it method?
 * @param YCPList argumnets from YCP to python function(0 - dummy)
 * @return YCPValue return value from python's function
 */
YCPValue
YPython::callInner (string module, string function, bool method,
		  YCPList argList)
{
    


  PyObject* pMain;
  PyObject* pMainDict;
  PyObject* pFunc;
  PyObject* pArgs;
  PyObject* pReturn;
 
  YCPValue result = YCPNull ();
  

  pMain = PyImport_AddModule("__main__");
  //PyRun_SimpleString("import __main__");
  pMainDict = PyModule_GetDict(pMain);
  
  
  
  pFunc = PyDict_GetItemString(pMainDict, function.c_str());
  
  
  pArgs = PyTuple_New(argList->size()-1);

  PyObject *pArg;
  //Parsing argumments

  y2milestone ("name of function %s and nuber of arguments %d", function.c_str(), argList->size()-1);
  
  for ( int i=1; i < argList->size(); i++ ) {
      //FIXME  add checking for all types from YCP and conversion to python types...

      pArg = YCPTypeToPythonSimpleType(argList->value(i));
      
      if (!pArg)
         pArg = fromYCPListToPythonList(argList->value(i));

      if (!pArg)
         pArg = fromYCPListToPythonTuple(argList->value(i));

      if (!pArg)
         pArg = fromYCPMapToPythonDict(argList->value(i));
      if (!pArg)
         pArg = fromYCPTermToPythonTerm(argList->value(i));

      PyTuple_SetItem(pArgs,i-1, pArg);

  } 
  

  pReturn = PyObject_CallObject(pFunc, pArgs);
  
  Py_CLEAR(pArgs);



  if (pReturn) {
     //result = YCPInteger(PyInt_AsLong(pReturn)); //new YCPValue();

     if (!PythonTypeToYCPSimpleType(pReturn, result))
        result =  fromPythonTupleToYCPList(pReturn);

     if (result.isNull())
        result = fromPythonListToYCPList (pReturn);

     if (result.isNull())
        result = fromPythonDictToYCPMap (pReturn);

     if (result.isNull())
        result = fromPythonTermToYCPTerm(pReturn);


  }   
  Py_CLEAR(pReturn);

  if (result.isNull ()) {
     y2error ("Result is NULL when returning from %s", function.c_str());
     result = YCPVoid ();
  }

  return result;
}


   /**
    * Transfer from python simple type to ycp simple type
    * transfered are: boolean, integer, string, float,
    **/
bool YPython::PythonTypeToYCPSimpleType(PyObject* pPythonValue, YCPValue &out) {
  PyObject * value;
  // boolean value handling
  if (PyBool_Check(pPythonValue)) {
     PyObject * true_value = PyBool_FromLong(1);
     int compare = PyObject_Compare(pPythonValue, true_value);
     if (compare == 0) {       
        out = YCPBoolean (true);
     } else if (compare < 1) {
        out = YCPBoolean (false);
     } else { 
        return false;
     }
     return true;
  }
  
  //integer value handling
  if (PyInt_Check(pPythonValue)) {

     out = YCPInteger(PyInt_AsLong(pPythonValue));
     return true;
  }

  //float value handling
  if (PyFloat_Check(pPythonValue)) {

     out = YCPFloat(PyFloat_AsDouble(pPythonValue));
     return true;
  }

  //string value handling
  if (PyString_Check(pPythonValue)) {

     out = YCPString(PyString_AsString(pPythonValue));
     return true;
  }

  if (pPythonValue == Py_None) {
     out = YCPNull();
     return true;
  }

  if (PyInstance_Check(pPythonValue)) {
     if (PyObject_HasAttrString(pPythonValue, "type"))  {
        PyObject * py_attr = PyObject_GetAttrString(pPythonValue,"type");
        if (PyString_Check(py_attr)) {
	   string type = PyString_AsString(py_attr);
           if (type.compare("symbol") == 0) {
	      value = PyObject_GetAttrString(pPythonValue,"value");
	      out = YCPSymbol(PyString_AsString(value));
              return true;
           }
           if (type.compare("path") == 0) {
	      value = PyObject_GetAttrString(pPythonValue,"value");
	      out = YCPPath(PyString_AsString(value));
              return true;
           }
        } //end of if (PyString_Check(py_attr))
     } //end of if (PyObject_HasAttrString(pPythonValue, "type"))
  }
  return false;
}

   /**
    * Transfer from ycp simple type to python simple type
    * transfered are: boolean, integer, string, float,
    **/
PyObject* YPython::YCPTypeToPythonSimpleType(YCPValue in) {
  
  if (in.isNull()) {
     return Py_None;
 
  } else if (in->isBoolean()) {
     long val = 0;
     bool true_false = in->asBoolean()->value();      
     true_false ? val = 1 : val =0;      
     return PyBool_FromLong(val);

  } else if (in->isInteger()) {
     return PyInt_FromLong(in->asInteger()->value());

  } else if (in->isFloat()) {
     double val = in->asFloat()->value();
     return PyFloat_FromDouble(val);

  } else if (in->isString()) {
     return PyString_FromString((in->asString()->value()).c_str());

  } else if (in->isVoid()) {
     return Py_None;

  } else if (in->isPath()) {
     if (pPathClass) {
        PyObject *value =  PyString_FromString(in->asPath()->toString().c_str());
        PyObject *pyArgs = PyTuple_New(1);
        PyTuple_SetItem(pyArgs, 0, value);
        return PyInstance_New(pPathClass, pyArgs, NULL);

     } else {
        return Py_None;
     }
  } else if (in->isSymbol()) {
     if (pSymbolClass) {
        //add hack delete first char (`) from output 
        PyObject *value =  PyString_FromString(in->asSymbol()->toString().erase(0,1).c_str());
        PyObject *pyArgs = PyTuple_New(1);
        PyTuple_SetItem(pyArgs, 0, value);
        return PyInstance_New(pSymbolClass, pyArgs, NULL);

     } else {
        return Py_None;
     }
  } else
     return NULL;
}

/**
  * Convert a Python list to a YCPList.
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
         if (PythonTypeToYCPSimpleType(pItem, ycp_value)) {
            if (!ycp_value.isNull ()) {
	       ycp_List->add(ycp_value);
            } else {
               return YCPNull ();
            }
         } else { //end of if (PythonTypeToYCPSimpleType(item, ycp_value))
            ycp_value = fromPythonListToYCPList(pItem);
            if (ycp_value.isNull ())
               ycp_value = fromPythonDictToYCPMap (pItem);
            if (ycp_value.isNull ())
               ycp_value = fromPythonTupleToYCPList(pItem);
            if (ycp_value.isNull ())
               ycp_value = fromPythonTermToYCPTerm(pItem);

            if (!ycp_value.isNull ())
	       ycp_List->add(ycp_value);
            else
               return YCPNull ();
         } // end of else for if (PythonTypeToYCPSimpleType(item, ycp_value))
     } //end of for (int i = 0; i < list_size; i++)
  } else { //end if (PyList_Check(pPythonList) > 0)
     y2milestone ("Value is not Python List");
     return YCPNull ();
  } //end else of if (PyList_Check(pPythonList) > 0) 

  return ycp_List;
}

/**
  * Convert a Python Tuple to a YCPList.
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
         if (PythonTypeToYCPSimpleType(pItem, ycp_value)) {
            if (!ycp_value.isNull ()) {
	       ycp_List->add(ycp_value);
            } else {
               return YCPNull ();
            }
         } else { //end of if (PythonTypeToYCPSimpleType(item, ycp_value))
             ycp_value = fromPythonListToYCPList(pItem);

             if (ycp_value.isNull ())
                ycp_value = fromPythonTupleToYCPList(pItem);

             if (ycp_value.isNull ())
                ycp_value = fromPythonDictToYCPMap(pItem);

             if (ycp_value.isNull ())
                ycp_value = fromPythonTermToYCPTerm(pItem);

             if (!ycp_value.isNull ())
		ycp_List->add(ycp_value);
             else
                return YCPNull ();
         } // end of else for if (PythonTypeToYCPSimpleType(item, ycp_value))
     } //end of for (int i = 0; i < list_size; i++)
  } else { //end if (PyTuple_Check(pPythonList) > 0)
     y2milestone ("Value is not Python Tuple");
     return YCPNull ();
  } //end else of if (PyTuple_Check(pPythonList) > 0) 

  return ycp_List;
}

/**
  * Convert a YCPList to a Python list.
 **/
PyObject* YPython::fromYCPListToPythonList (YCPValue ycp_List) {

  PyObject* pPythonList;
  PyObject* pItem;
  int ret = 0;
  if (ycp_List->isList()) {
     if (ycp_List->asList()->size()>0)
        pPythonList = PyList_New(ycp_List->asList()->size());
     else {
        y2error("YCP list is empty."); 
        return Py_None;
     }
     y2milestone ("Size of list %d",ycp_List->asList()->size());
     for ( int i = 0; i < ycp_List->asList()->size(); i++ ) {
         pItem = YCPTypeToPythonSimpleType(ycp_List->asList()->value(i));

         if (!pItem)
            pItem = fromYCPListToPythonList(ycp_List->asList()->value(i));

         if (!pItem)
            pItem = fromYCPListToPythonTuple(ycp_List->asList()->value(i));

         if (!pItem)
	    pItem = fromYCPMapToPythonDict(ycp_List->asList()->value(i));

         if (!pItem)
	    pItem = fromYCPTermToPythonTerm(ycp_List->asList()->value(i));

         ret = PyList_SetItem(pPythonList, i, pItem);

         if (ret <0)
            y2error("PyList_SetItem doesn't add item into python list.");  

     }
     Py_INCREF(pPythonList);
     return pPythonList;

  } else {
    y2milestone ("Value is not YCPList");
    return NULL;
  }
}

/**
  * Convert a YCPList to a Python tuple.
 **/
PyObject* YPython::fromYCPListToPythonTuple (YCPValue ycp_List) {

  PyObject* pPythonTuple;
  PyObject* pItem;
  int ret = 0;
  if (ycp_List->isList()) {
     if (ycp_List->asList()->size()>0)
        pPythonTuple = PyTuple_New(ycp_List->asList()->size());
     else {
        y2error("YCP list is empty."); 
        return Py_None;
     }
     y2milestone ("Size of list %d",ycp_List->asList()->size());
     for ( int i = 0; i < ycp_List->asList()->size(); i++ ) {
         pItem = YCPTypeToPythonSimpleType(ycp_List->asList()->value(i));

         if (!pItem)
            pItem = fromYCPListToPythonList(ycp_List->asList()->value(i));

         if (!pItem)
            pItem = fromYCPListToPythonTuple(ycp_List->asList()->value(i));

         if (!pItem)
	    pItem = fromYCPMapToPythonDict(ycp_List->asList()->value(i));

         if (!pItem)
	    pItem = fromYCPTermToPythonTerm(ycp_List->asList()->value(i));

         ret = PyTuple_SetItem(pPythonTuple, i, pItem);

         if (ret <0)
            y2error("PyList_SetItem doesn't add item into python list.");  

     }
     Py_INCREF(pPythonTuple);
     return pPythonTuple;

  } else {
    y2milestone ("Value is not YCPList");
    return NULL;
  }
}


/**
  * Convert a YCPMap to a Python Dictionary.
 **/
PyObject* YPython::fromYCPMapToPythonDict (YCPValue ycp_Map) {

  PyObject* pPythonDict;
  PyObject* pKey;
  PyObject* pValue;
  int ret = -1;
  if (ycp_Map->isMap()) {
     if (ycp_Map->asMap()->size()>0) {
        pPythonDict = PyDict_New();
        for (YCPMapIterator it = ycp_Map->asMap()->begin(); it != ycp_Map->asMap()->end(); ++it ) {
            pKey = YCPTypeToPythonSimpleType(it.key());
            if (!pKey) {
               y2error("Transfer key YCPMap to PyObject falsed.");
               return NULL;
            }
            pValue =  YCPTypeToPythonSimpleType(it.value());
	    if (!pValue)
               pValue = fromYCPListToPythonList(it.value());
	    if (!pValue)
               pValue = fromYCPListToPythonTuple(it.value());
            if (!pValue)
               pValue = fromYCPMapToPythonDict(it.value());
            if (!pValue)
               pValue = fromYCPTermToPythonTerm(it.value());


            if (pValue) {
               ret = PyDict_SetItem(pPythonDict, pKey, pValue);
               if (ret < 0) {
                  y2error("Adding value and key from YCPMap to Python Dictionary falsed.");
                  return NULL;
               }
            } else {
               y2error("Transfer value from YCPMap to PyObject falsed.");
               return NULL;
               
            }             
        } // end of for (YCPMapIterator it = ycp_Map->begin(); it != ycp_Map->end(); ++it )

     } else { // end if (ycp_Map->asMap()->size()>0)
        y2error("YCP map is empty."); 
        return NULL;
     } // end else of if (ycp_Map->asMap()->size()>0)

  } else { // end if (ycp_Map->isMap())
     y2milestone ("Value is not YCPMap");
     return NULL;
  } // end else of if (ycp_Map->isMap())
  Py_INCREF(pPythonDict);
  return pPythonDict;
}


/**
  * Convert a Python Dictionary to a YCPMap.
 **/
YCPMap YPython::fromPythonDictToYCPMap (PyObject* pPythonDict) {

  PyObject* pListKeys;
  PyObject* pListValues;
  YCPValue ycp_key;
  YCPValue ycp_value;
  YCPMap ycp_Map;
  if (PyDict_Check(pPythonDict)>0) {
     if (PyDict_Size(pPythonDict)>0) {
        pListKeys = PyDict_Keys(pPythonDict);
        pListValues = PyDict_Values(pPythonDict);
        for (int i=0; i < PyList_Size(pListKeys); i++) {
            if (PythonTypeToYCPSimpleType(PyList_GetItem(pListKeys, i),ycp_key)) {
	       if (PythonTypeToYCPSimpleType(PyList_GetItem(pListValues, i),ycp_value)) {
                  ycp_Map->add (ycp_key, ycp_value);
               } else {
                  ycp_value = fromPythonListToYCPList(PyList_GetItem(pListValues, i));
                  if (ycp_value.isNull ())
                     ycp_value = fromPythonTupleToYCPList(PyList_GetItem(pListValues, i));
                  if (ycp_value.isNull ())
                     ycp_value = fromPythonDictToYCPMap (PyList_GetItem(pListValues, i));
                  if (ycp_value.isNull ())
                     ycp_value = fromPythonTermToYCPTerm(PyList_GetItem(pListValues, i));

		  ycp_Map->add (ycp_key, ycp_value);
               }

            } else {
               y2error("Cannot convert key from python dictionary");
               return YCPNull ();
            }               
        } 
        
     } else {
        y2milestone ("Python dictionary is empty");
        return YCPNull ();
     }
  } else {
     y2milestone ("Value is not python dictionary");
     return YCPNull ();
  }
  return ycp_Map;
}

/**
  * Convert a Python Term to a YCPTerm.
 **/

YCPTerm YPython::fromPythonTermToYCPTerm (PyObject* pPythonTerm) {
  PyObject *value;
  PyObject *pyName;
  string name;
  YCPValue ycp_value;

  if (PyInstance_Check(pPythonTerm)) {
     if (PyObject_HasAttrString(pPythonTerm, "type"))  {
        PyObject * py_attr = PyObject_GetAttrString(pPythonTerm,"type");
        if (PyString_Check(py_attr)) {
	   string type = PyString_AsString(py_attr);
           if (type.compare("term") == 0) {
              pyName = PyObject_GetAttrString(pPythonTerm,"name");
              if (PyString_Check(pyName)) {
		 name = PyString_AsString(pyName);
		 value = PyObject_GetAttrString(pPythonTerm,"value");
                 if (PyTuple_Check(value))

                 ycp_value = fromPythonTupleToYCPList(value);
                 
                 if (!ycp_value.isNull ()) {
                    //printf("term is: %s\n",YCPTerm(name,ycp_value->asList())->toString().c_str());
                    return YCPTerm(name,ycp_value->asList());
                    
                 } else {
                    y2error("Value was not converted to YCPTerm");
                    return YCPNull ();
                 }
              } else {
                 y2error ("The name of Term is not string");
                 return YCPNull ();
              }
           } else {
              y2milestone ("Value is not python Term");
              return YCPNull ();
           }
        } else {
           y2error ("Value is not any python class for ycp types");
           return YCPNull ();
        }
     }
  } else {
     return YCPNull ();
  }	
  return YCPNull ();
}


/**
  * Convert a YCPTerm to a Python Term.
 **/
PyObject* YPython::fromYCPTermToPythonTerm (YCPValue ycp_Term) {

  PyObject* pPythonTerm;
  PyObject* pName;
  PyObject* pValue;

  if (ycp_Term->isTerm()) {
     if (ycp_Term->asTerm()->args()->size()>0) {
        pName = PyString_FromString(ycp_Term->asTerm()->name().c_str());
        YCPValue list = ycp_Term->asTerm()->args();
        pValue = fromYCPListToPythonTuple(list);
        if (pValue) {
	   if (pTermClass) {
              PyObject *pyArgs = PyTuple_New(2);
              PyTuple_SetItem(pyArgs, 0, pName);
              PyTuple_SetItem(pyArgs, 1, pValue);
              pPythonTerm = PyInstance_New(pTermClass, pyArgs, NULL);
           } else {
              y2error("There is missing Term class in python");
              return Py_None;
           }
        } else {
           y2error("Converting to python tuple failed");
           return Py_None;
        }
 
     } else { // end if (ycp_Map->asMap()->size()>0)
        y2error("YCP term is empty."); 
        return NULL;
     } // end else of if (ycp_Map->asMap()->size()>0)

  } else { // end if (ycp_Map->isMap())
     y2milestone ("Value is not YCPTerm");
     return NULL;
  } // end else of if (ycp_Map->isMap())
  Py_INCREF(pPythonTerm);
  return pPythonTerm;
}

