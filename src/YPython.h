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
#include <ycp/Type.h>


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



private:
    


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
