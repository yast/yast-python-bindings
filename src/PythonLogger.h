
#ifndef PythonLogger_h
#define PythonLogger_h

#include "ycp/y2log.h"

/**
 * @short A class to provide logging for Python bindings errors and warning
 */
class PythonLogger : public Logger
{
    static PythonLogger* m_pythonlogger;

public:
    void error (string message);
    void warning (string message);

    static PythonLogger* instance ();
};

#endif	// ifndef PythonLogger_h


// EOF
