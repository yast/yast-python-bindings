%{
YCPValue pyval_to_ycp(PyObject *input)
{
    int ret;
    void *arg = 0;

    if (input == Py_None)
        return YCPNull();
    if (PyBool_Check(input)) {
        if (PyObject_RichCompareBool(input, Py_True, Py_EQ) == 1)
            return YCPBoolean(true);
        else
            return YCPBoolean(false);
    }
    if (PyInt_Check(input))
        return YCPInteger(PyInt_AsLong(input));
    if (PyFloat_Check(input))
        return YCPFloat(PyFloat_AsDouble(input));
    if (PyString_Check(input))
        return YCPString(PyString_AsString(input));
    if (PyUnicode_Check(input))
        return YCPString(_PyUnicode_AsString(input));
    if (PyList_Check(input)) {
        auto size = PyList_Size(input);
        if (size > 0 && PyFunction_Check(PyList_GetItem(input, 0))) {
            auto t = PyTuple_New(size);
            for (int i = 0; i < size; i++)
                PyTuple_SetItem(t, i, PyList_GetItem(input, i));
            return YCPCode(new YPythonCode(t));
        } else {
            YCPList l;
            for (int i = 0; i < size; i++)
                l->add(pyval_to_ycp(PyList_GetItem(input, i)));
            return l;
        }
    }
    if (PyFunction_Check(input))
        return YCPCode(new YPythonCode(PyTuple_Pack(1, input)));
    if (PyDict_Check(input)) {
        YCPMap m;
        if (PyDict_Size(input) == 0)
            return m;

        PyObject *key, *value;
        Py_ssize_t pos = 0;
        while (PyDict_Next(input, &pos, &key, &value))
            m->add(pyval_to_ycp(key), pyval_to_ycp(value));
        return m;
    }
    if (PyTuple_Check(input)) {
        auto size = PyTuple_Size(input);
        YCPList l;
        for (int i = 0; i < size; i++)
            l->add(pyval_to_ycp(PyTuple_GetItem(input, i)));
        return l;
    }
    ret = SWIG_ConvertPtr(input, &arg, SWIGTYPE_p_YCPValue, SWIG_POINTER_DISOWN | 0);
    if (SWIG_IsOK(ret))
        return *(reinterpret_cast<YCPValue*>(arg));

    return YCPNull();
}

PyObject *ycp_to_pyval(YCPValue val)
{
    if (val.isNull() || val->isVoid())
        Py_RETURN_NONE;
    if (val->isString())
        return PyString_FromString(val->asString()->value().c_str());
    else if (val->isInteger())
        return PyInt_FromLong(val->asInteger()->value());
    else if (val->isBoolean())
        return PyBool_FromLong(val->asBoolean()->value());
    else if (val->isFloat())
        return PyFloat_FromDouble(val->asFloat()->value());
    else if (val->isSymbol())
        return PyString_FromString(val->asSymbol()->symbol().c_str());
    else if (val->isPath())
        return PyString_FromString(val->asPath()->toString().c_str());
    else if (val->isList()) {
        PyObject* pItem;
        PyObject* pPythonTuple = PyTuple_New(val->asList()->size());
        for (int i = 0; i < val->asList()->size(); i++) {
            pItem = ycp_to_pyval(val->asList()->value(i));
            PyTuple_SetItem(pPythonTuple, i, pItem);
        }
        Py_INCREF(pPythonTuple);
        return pPythonTuple;
    } else if (val->isMap()) {
        PyObject* pKey;
        PyObject* pValue;
        PyObject* pPythonDict = PyDict_New();
        for (YCPMap::const_iterator it = val->asMap()->begin(); it != val->asMap()->end(); ++it) {
            pKey = ycp_to_pyval(it->first);
            pValue = ycp_to_pyval(it->second);
            if (pValue && pKey) {
                PyDict_SetItem(pPythonDict, pKey, pValue);
            }
        }
        Py_INCREF(pPythonDict);
        return pPythonDict;
    } else if (val->isTerm())
        return ycp_to_pyval(val->asTerm()->args());

    Py_RETURN_NONE;
}
%}

%include "ytypes.h"

