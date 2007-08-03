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

  File:	      Y2PythonComponent.cc



/-*/

#define y2log_component "Y2Python"
#include <Python.h>
#include <ycp/y2log.h>
#include <ycp/pathsearch.h>

#include "Y2PythonComponent.h"

//XXX -> not rewrited
#include "YPython.h"
#include "YPythonNamespace.h"
using std::string;


Y2PythonComponent::Y2PythonComponent()
{
    // Actual creation of a Python interpreter is postponed until one of the
    // YPython static methods is used. They handle that.

    y2milestone( "Creating Y2PythonComponent" );
}


Y2PythonComponent::~Y2PythonComponent()
{
    YPython::destroy();
}


void Y2PythonComponent::result( const YCPValue & )
{
}


Y2Namespace *Y2PythonComponent::import (const char* name)
{
    // TODO where to look for it
    // must be the same in Y2CCPython and Y2PythonComponent

    string module = YCPPathSearch::find (YCPPathSearch::Module, string (name) + ".py");
    if (module.empty ())
    {
	y2internal ("Couldn't find %s after Y2CCPython pointed to us", name);
	return NULL;
    }
    
    module.erase (module.size () - 3 /* strlen (".py") */);
    YCPList args;
    args->add (YCPString(/*module*/ name));

    // load it
    //XXX -> not rewrited
    YPython::loadModule (args);

    // introspect, create data structures for the interpreter
    Y2Namespace *ns = new YPythonNamespace (name);

    return ns;
}
