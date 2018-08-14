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

  File:	      Y2CCPython.h

/-*/

#include <Python.h>
#ifndef _Y2CCPython_h
#define _Y2CCPython_h

#include "Y2PythonComponent.h"

/**
 * @short Y2ComponentCreator that creates Python-from-YCP bindings.
 *
 * A Y2ComponentCreator is an object that can create components.
 * It receives a component name and - if it knows how to create
 * such a component - returns a newly created component of this
 * type. Y2CCPython can create components with the name "Python".
 */
class Y2CCPython : public Y2ComponentCreator
{
private:
    Y2Component *cpython;

public:
    /**
     * Creates a Python component creator
     */
    Y2CCPython() : Y2ComponentCreator( Y2ComponentBroker::BUILTIN ),
	cpython (0) {};

    ~Y2CCPython () {
	if (cpython)
	    delete cpython;
    }

    /**
     * Returns true, since the Python component is a YaST2 server.
     */
    bool isServerCreator() const { return true; };

    /**
     * Creates a new Python component.
     */
    Y2Component *create( const char * name ) const
    {
	// create as many as requested, they all share the static YPython anyway
	if ( ! strcmp( name, "python") ) return new Y2PythonComponent();
	else return 0;
    }

    /**
     * always returns the same component, deletes it finally
     */
    Y2Component *provideNamespace (const char *name);

};

#endif	// ifndef _Y2CCPython_h


// EOF
