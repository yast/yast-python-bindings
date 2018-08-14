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

  File:	      Y2PythonComponent.h



/-*/


#ifndef Y2PythonComponent_h
#define Y2PythonComponent_h

#include <Python.h>
#include "Y2.h"


/**
 * @short YaST2 Component: Python bindings
 */
class Y2PythonComponent : public Y2Component
{
public:
    /**
     * Constructor.
     */
    Y2PythonComponent();

    /**
     * Destructor.
     */
    ~Y2PythonComponent();

    /**
     * The name of this component.
     */
    string name() const { return "python"; }

    /**
     * Is called by the generic frontend when the session is finished.
     */
    void result( const YCPValue & result );

    /**
     * Implements the Python:: functions.
     **/
// not yet, prototype the transparent bindings first
//    YCPValue evaluate( const YCPValue & val );

    /**
     * Try to import a given namespace. This method is used
     * for transparent handling of namespaces (YCP modules)
     * through whole YaST.
     * @param name_space the name of the required namespace
     * @return on errors, NULL should be returned. The
     * error reporting must be done by the component itself
     * (typically using y2log). On success, the method
     * should return a proper instance of the imported namespace
     * ready to be used. The returned instance is still owned
     * by the component, any other part of YaST will try to
     * free it. Thus, it's possible to share the instance.
     */
    Y2Namespace *import (const char* name);
};

#endif	// Y2PythonComponent_h
