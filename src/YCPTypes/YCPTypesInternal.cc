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
