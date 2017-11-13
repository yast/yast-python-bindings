#ifndef _Y2CCPythonClient_h
#define _Y2CCPythonClient_h

#include "Y2PythonClientComponent.h"

/**
 * @short Y2ComponentCreator that creates Python client component
 *
 * A Y2ComponentCreator is an object that can create components.
 * It receives a component name and - if it knows how to create
 * such a component - returns a newly created component of this
 * type. Y2CCPythonClient can create components with the name "PythonClient".
 */
class Y2CCPythonClient : public Y2ComponentCreator
{
private:
    Y2Component *cpython;

public:
    /**
     * Creates a Python component creator
     */
    Y2CCPythonClient() : Y2ComponentCreator( Y2ComponentBroker::BUILTIN ),
	cpython (0) {};

    ~Y2CCPythonClient () {
	if (cpython)
	    delete cpython;
    }

    /**
     * 
     */
    bool isServerCreator() const { return false; };

    /**
     * Creates a new Python component.
     */
    Y2Component *create( const char * name ) const;

    /**
     * always returns the same component, deletes it finally
     */
    Y2Component *provideNamespace (const char *name);

};

#endif
