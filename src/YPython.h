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
     * Load a Perl module - equivalent to "use" in Python.
     *
     * Returns a YCPError on failure, YCPVoid on success.
     **/
    static YCPValue loadModule( YCPList argList );

    /**
     * Access the static (singleton) YPython object. Create it if it isn't
     * created yet.
     *
     * Returns 0 on error.
     **/
    static YPython * yPython();



    /**
     * Destroy the static (singleton) YPython object and unload the embedded Perl
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
    * Transfer from python simple type to ycp simple type
    * transfered are: boolean, integer, string, float,
    **/
    bool PythonTypeToYCPSimpleType(PyObject* pPythonValue, YCPValue &out);

   /**
    * Transfer from ycp simple type to python simple type
    * transfered are: boolean, integer, string, float,
    **/
    PyObject* YCPTypeToPythonSimpleType(YCPValue in);

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
