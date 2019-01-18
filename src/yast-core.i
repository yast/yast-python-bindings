%module ycp
%begin %{
#define SWIG_PYTHON_2_UNICODE
%}

%feature("autodoc", "3");

%include std_string.i
%include std_map.i
%inline %{
using namespace std;
%}

%{
#include "yast.h"
#include "YPython.h"
#include "YPythonCode.h"
#include <ycp/YCPByteblock.h>
%}

%include ycp.i
%include ytypes.i
%include y2log.i

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

%include "yast.h"

