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
     *
     * import a Python module
     */

    PyObject* importModule(string module);

    /**
     * Load a Python YAST module
     *
     * Returns a YCPError on failure, YCPVoid on success.
     **/
    YCPValue loadModule(string module);

    /**
     * Access the static (singleton) YPython object. Create it if it isn't
     * created yet.
     *
     * Returns 0 on error.
     **/
    static YPython& yPython();

    /**
     * Access the static _pMainDicts
     *
     **/

    PyObject* pMainDicts();


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


    /**
      * Handler for python errors, info will be saved into  yast logs
      * FUnction saves info from void PyErr_Fetch(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback)
      **/
    string PyErrorHandler();

    /**
     * Prepare YCPReference for calling python function in YCP via reference
     **/
    YCPValue fromPythonFunToReference (PyObject* pyFun);

private:


    static YPython * _yPython;
    /**
     * static _pMainDicts includes dictionaries of all imported python modules
     *
     **/

    PyObject* _pMainDicts;
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
