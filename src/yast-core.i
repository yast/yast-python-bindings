%module ycp

%feature("autodoc", "3");

%include std_string.i
%include std_map.i
%inline %{
using namespace std;
%}

%{
#include <ycp/YCPFloat.h>
#include "yast.h"
#include <ycp/YCPCode.h>
#include <ycp/YCPMap.h>
#include "YPythonCode.h"
%}

%feature("valuewrapper") YCPBoolean;
class YCPBoolean;
%feature("valuewrapper") YCPInteger;
class YCPInteger;
%feature("valuewrapper") YCPString;
class YCPString;

%ignore YCPTermRep;
%include <ycp/YCPTerm.h>
%ignore YCPListRep;
%include <ycp/YCPList.h>
%ignore YCPStringRep;
%include <ycp/YCPString.h>
%ignore YCPSymbolRep;
%include <ycp/YCPSymbol.h>
%ignore YCPIntegerRep;
%include <ycp/YCPInteger.h>
%ignore YCPBooleanRep;
%include <ycp/YCPBoolean.h>
%ignore YCPFloatRep;
%include <ycp/YCPFloat.h>
%ignore YCPMapRep;
%ignore YCPMapIterator;
%include "YCPMap.h"

%include ytypes.i

%typemap(out) YCPValue {
    $result = ycp_to_pyval($1);
}
%typemap(in) YCPValue {
    $1 = pyval_to_ycp($input);
}
%typemap(in) YCPList {
    $1 = pyval_to_ycp($input)->asList();
}
%typemap(in) YCodePtr {
    $1 = new YPythonCode($input);
}
%typemap(typecheck,precedence=5000) YCodePtr {
    $1 = PyFunction_Check(PyTuple_GetItem($input, 0));
}

%ignore YCPCodeRep;
%ignore YCPEntryRep;
%ignore YCPEntry;
%include <ycp/YCPCode.h>
%extend YCPCode {
    YCPValue evaluate (bool cse = false) {
        return (*($self))->evaluate(cse);
    }
}

%varargs(25, char * opt = NULL) Opt;
%include "yast.h"

