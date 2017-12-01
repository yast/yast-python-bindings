#include <Python.h>
#include <y2/Y2Namespace.h>
#include <y2/Y2Component.h>
#include <y2/Y2ComponentCreator.h>
#include <ycp/y2log.h>
#include <ycp/YBlock.h>
#include <ycp/YExpression.h>
#include <ycp/YStatement.h>
#include <ycp/Import.h>
#include <ycp-ui/YUIComponent.h>
#include <wfm/Y2WFMComponent.h>
#include <ycp/Parser.h>
#include <ycp/YCPMap.h>
#include <ycp/YCPList.h>
#include <ycp/YCPPath.h>
#include <ycp/YCPTerm.h>
#include <ycp/YCPString.h>
#include <ycp/YCPVoid.h>
#include <ycp/YCPFloat.h>
#include <ycp/YCPBoolean.h>
#include <ycp/SymbolTable.h>
#include <yui/YUILoader.h>
#include <yui/YSettings.h>

#include "PythonLogger.h"

#include <string>
#include <cstdarg>
#include <sstream>
using namespace std;

YCPValue CallYCPFunction(const char * namespace_name, const char * function_name, YCPList args);
void SetYCPVariable(const string & namespace_name, const string & variable_name, YCPValue value);
YCPValue GetYCPVariable(const string & namespace_name, const string & variable_name);
PyObject* import_module(const string & ns_name);

bool widget_names();
YCPValue _SCR_Run(char *function, YCPList args);

