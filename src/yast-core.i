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
#include <ycp/YCPByteblock.h>
#include "YPythonCode.h"
%}

%include ycp.i
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

%varargs(25, char * opt = NULL) Opt;
%include "yast.h"

