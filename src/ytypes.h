#include <Python.h>
#include <ycp/YCPValue.h>

YCPValue pyval_to_ycp(PyObject *input);
PyObject *ycp_to_pyval(YCPValue val);

