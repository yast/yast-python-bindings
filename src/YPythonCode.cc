#include "YPythonCode.h"

YPythonCode::YPythonCode (PyObject *pFunc):YCode() {
    m_kind = YCode::yeReference;
    _pFunc = pFunc;
}

YCPValue YPythonCode::evaluate(bool cse) {
    PyObject * pReturn = NULL;
    YCPValue result = YCPVoid();
    PyObject * pFunction = NULL;
    PyObject * pArgs = NULL;
    int args_size;

    args_size = PyTuple_Size(_pFunc);

    if (args_size >=1) {
        pFunction = PyTuple_GetItem(_pFunc, 0);
        if (args_size > 1) {
            pArgs = PyTuple_GetSlice(_pFunc, 1, args_size);
        }
    }
    if (Py_IsInitialized()) {
        pReturn = PyObject_CallObject(pFunction, pArgs);
        if (pReturn)
            result = pyval_to_ycp(pReturn);
    }
    return result;
}

YCode::ykind YPythonCode::kind() const {
    return m_kind;
}

std::ostream & YPythonCode::toStream (std::ostream & str) const {
    return str;
}

std::ostream & YPythonCode::toXml (std::ostream & str, int indent ) const {
    return str;
}

