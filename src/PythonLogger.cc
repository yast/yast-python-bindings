#include "PythonLogger.h"
#include <ycp/ExecutionEnvironment.h>


void
PythonLogger::error (string error_message)
{
    y2_logger(LOG_ERROR, "Python", YaST::ee.filename().c_str(), YaST::ee.linenumber(),
	      "", "%s", error_message.c_str());
}


void
PythonLogger::warning (string warning_message)
{
    y2_logger(LOG_ERROR, "Python", YaST::ee.filename().c_str(), YaST::ee.linenumber(),
	      "", "%s", warning_message.c_str());
}


PythonLogger*
PythonLogger::instance ()
{
    if ( ! m_pythonlogger )
    {
	m_pythonlogger = new PythonLogger ();
    }
    return m_pythonlogger;
}

PythonLogger* PythonLogger::m_pythonlogger = NULL;
