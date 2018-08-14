/*-----------------------------------------------------------*- c++ -*-\
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

  File:	      YPython.h


/-*/


#ifndef YPython_h
#define YPython_h

#include <Python.h>

#include <ycp/YCPList.h>
#include <ycp/YCPValue.h>
#include <ycp/Type.h>
#include <ycp/YCPCode.h>
#include <ycp/YCode.h>



class YPython
{
public:

    /**
     * Load a Python module - equivalent to "use" in Python.
     *
     * Returns a YCPError on failure, YCPVoid on success.
     **/
    static YCPValue loadModule(string module);

    /**
     * Access the static (singleton) YPython object. Create it if it isn't
     * created yet.
     *
     * Returns 0 on error.
     **/
    static YPython * yPython();

    /**
     * Access the static _pMainDicts
     * 
     **/

    PyObject* pMainDicts();

    /**
     * static _pMainDicts includes dictionaries of all imported python modules
     * 
     **/

    static PyObject* _pMainDicts;

    /**
     * Destroy the static (singleton) YPython object and unload the embedded Python
     * interpreter.
     *
     * Returns YCPVoid().
     **/
    static YCPValue destroy();

    /**
     * Generic Python call.
     **/
    YCPValue callInner (string module, string function, bool method,
			YCPList argList);
    
    static YPython * _yPython;


    /**
     * Transform Python type to YCP type and return new YCPValue built
     * from python object.
     */
    YCPValue PythonTypeToYCPType(PyObject*);

    /**
     * Transform YCP type to Python type and return reference to new
     * Python object.
     */
    PyObject *YCPTypeToPythonType(YCPValue);

   /**
     * Handler for python errors, info will be saved into  yast logs
     * FUnction saves info from void PyErr_Fetch(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback)
     **/
    static string PyErrorHandler();

    /**
     * Prepare YCPReference for calling python function in YCP via reference
     **/
    YCPValue fromPythonFunToReference (PyObject* pyFun);

private:

    /**
     * Find function in Global Dictionary
     * confirm if function is from imported module or not
     * return 1 if module is in dictionary and function too
     * retrun 0 if module is in dictionary and function not
     * return -1 if missing both (module and dinctionary)
     **/

    int findModuleFuncInDict(string module, string function);

   /**
     * Adding module name and function into 
     * global dictionary 
     * (necessary for calling python function via reference)
     **/
    bool addModuleAndFunction(string module, string fun_name, PyObject* function);


    /**
     * Convert a Python list to a YCPList.
     **/
    YCPList fromPythonListToYCPList (PyObject* pPythonList);

    /**
     * Convert a YCPList to a Python list.
     **/
    PyObject* fromYCPListToPythonList (YCPValue ycp_List);

    /**
     * Convert a Python Dictionary to a YCPMap.
     **/
    YCPMap fromPythonDictToYCPMap (PyObject* pPythonDict);


    /**
     * Convert a YCPMap to a Python Dictionary.
     **/
    PyObject* fromYCPMapToPythonDict (YCPValue ycp_Map);

    /**
     * Convert a Python Tuple to YCPList
     **/
    YCPList fromPythonTupleToYCPList (PyObject* pPythonTuple);

    /**
     * Convert a YCPList to a Python tuple.
     **/
    PyObject* fromYCPListToPythonTuple (YCPValue ycp_List);

    /**
     * Convert a Python Tuple to YCPList
     **/
    YCPTerm fromPythonTermToYCPTerm (PyObject* pPythonTerm);

    /**
     * Convert a YCPList to a Python tuple.
     **/
    PyObject* fromYCPTermToPythonTerm (YCPValue ycp_Term);

    /**
     * Function find in namespace function and return symbol entry
     **/
    YCPValue findSymbolEntry(Y2Namespace *ns, string module, string function);

protected:

    /**
     * Protected constructor. Use one of the static methods rather than
     * instantiate an object of this class yourself.
     **/
    YPython();

    /**
     * Destructor.
     **/
    ~YPython();

    


};


#endif	// YPython_h
