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

  File:	      Y2CCPython.cc


/-*/

#include <Python.h>
#include "Y2CCPython.h"
#include <ycp/pathsearch.h>
#define y2log_component "Y2Python"
#include <ycp/y2log.h>

// This is very important: We create one global variable of
// Y2CCPython. Its constructor will register it automatically to
// the Y2ComponentBroker, so that will be able to find it.
// This all happens before main() is called!

Y2CCPython g_y2ccpython;

Y2Component *Y2CCPython::provideNamespace (const char *name)
{
    y2debug ("Y2CCPython::provideNamespace %s", name);
    if (strcmp (name, "Python") == 0)
    {
	// low level functions

	// leave implementation to later
	return 0;
    }
    else
    {
	// is there a python module?
	// must be the same in Y2CCPython and Y2PythonComponent
	string module = YCPPathSearch::find (YCPPathSearch::Module, string (name) + ".py");
	if (!module.empty ())
	{
	    if (!cpython)
	    {
		cpython = new Y2PythonComponent ();
	    }
	    return cpython;
	}

	// let someone else try creating the namespace
	return 0;
    }
}
