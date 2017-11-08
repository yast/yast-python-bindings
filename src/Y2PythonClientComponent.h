#ifndef Y2PythonClientComponent_h
#define Y2PythonClientComponent_h

#include "Y2.h"
#include <string.h>

/**
 * @short YaST2 Component: Python bindings
 */
class Y2PythonClientComponent : public Y2Component
{
public:
    /**
     * Destructor.
     */
    ~Y2PythonClientComponent();

    static Y2PythonClientComponent* instance();

    void setClient(const string& _client) { client = _client; }

    /**
     * The name of this component.
     */
    string name() const { return "pythonclient"; }

    YCPValue doActualWork(const YCPList& arglist, Y2Component *displayserver);

private:
    string client;
    static Y2PythonClientComponent* _instance;

    /**
     * Constructor.
     */
    Y2PythonClientComponent();

};

#endif	// Y2PythonComponent_h
