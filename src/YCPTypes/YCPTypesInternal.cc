#include "YCPTypesInternal.h"

/********** YCPTypeString fucntions **********/
void YCPTypeString_dealloc(YCPTypeString *self)
{
    Py_XDECREF(self->value);
    self->ob_type->tp_free((PyObject *)self);
}

PyObject *YCPTypeString_new(PyTypeObject *type, PyObject *args,
                                         PyObject *kwds)
{
    YCPTypeString *self;

    self = (YCPTypeString *)type->tp_alloc(type, 0);
    if (self != NULL){
        self->value = PyString_FromString("");
        if (self->value == NULL){
            Py_DECREF(self);
            return NULL;
        }

        self->hash = -1;
    }

    return (PyObject *)self;
}

int YCPTypeString_init(YCPTypeString *self, PyObject *args, PyObject *kwds)
{
    const char *value=NULL;
    PyObject *tmp;

    if (!PyArg_ParseTuple(args, "s", &value))
        return -1;

    if (value != NULL) {
        tmp = self->value;
        self->value = Py_BuildValue("s", value);
        Py_XDECREF(tmp);
    }

    return 0;
}

long YCPTypeString_hash(YCPTypeString *self)
{
    if (self->hash != -1){
        self->hash = PyObject_Hash(self->value);
    }
    return self->hash;
}

PyObject *YCPTypeString_New(PyObject *value, PyTypeObject *type)
{
    PyObject *ret;
    PyObject *args;

    if (!PyString_Check(value)){
        return Py_None;
    }

    // create args variable
    args = PyTuple_New(1);
    Py_INCREF(value);
    if (PyTuple_SetItem(args, 0, value) != 0){
        Py_XDECREF(args);
        Py_DECREF(value);
    }

    // create new Path object
    ret = YCPTypeString_new(type, Py_None, Py_None);
    if (ret == NULL){
        Py_XDECREF(args);
        return Py_None;
    }

    // initialize Path object
    if (YCPTypeString_init((YCPTypeString *)ret, args, Py_None) == -1){
        Py_XDECREF(args);
        return Py_None;
    }

    Py_XDECREF(args);
    return ret;
}

