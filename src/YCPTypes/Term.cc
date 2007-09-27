#include "YCPTypesInternal.h"

/**
 * Deallocate Term object
 */
static void Term_dealloc(Term *self)
{
    Py_XDECREF(self->name);
    Py_XDECREF(self->value);
    self->ob_type->tp_free((PyObject *)self);
}

/**
 * This function is called before Term_init.
 * In this function is set only default values.
 */
PyObject *Term_new(PyTypeObject *type, PyObject *args,
                                         PyObject *kwds)
{
    Term *self;

    self = (Term *)type->tp_alloc(type, 0);
    if (self != NULL){
        self->name = PyString_FromString("");
        if (self->name == NULL){
            Py_DECREF(self);
            return NULL;
        }
        self->value = PyTuple_New(0);
        if (self->value == NULL){
            Py_DECREF(self);
            return NULL;
        }

        self->hash = -1;
    }

    return (PyObject *)self;
}

/**
 * Initialize Term object.
 */
int Term_init(Term *self, PyObject *args, PyObject *kwds)
{
    PyObject *name = NULL;
    PyObject *value = NULL;
    PyObject *tmp;
    int args_size;

    // check number of arguments
    args_size = PyTuple_Size(args);
    if (args_size < 1){
        PyErr_SetString(PyExc_TypeError, ": function takes exactly 1 argument (0 given)");
        return -1;
    }

    // name:
    name = PyTuple_GetItem(args, 0);
    if (PyString_CheckExact(name)){
        tmp = self->name;
        Py_INCREF(name);
        self->name = name;
        Py_XDECREF(tmp);
    }else{
        PyErr_SetString(PyExc_TypeError, ": argument 1 must be string");
        return -1;
    }

    // value:
    if (args_size > 1){
        value = PyTuple_GetSlice(args, 1, args_size); // return new reference
        if (value != NULL){
            tmp = self->value;
            self->value = value;
            Py_XDECREF(tmp);
        }
    }

    return 0;
}

/**
 * Returns hash of Term object.
 */
static long Term_hash(Term *self)
{
    if (self->hash != -1){
        self->hash = PyObject_Hash(self->name) + PyObject_Hash(self->value);
    }
    return self->hash;
}

/**
 * Compare two Term objects.
 * If obj1 or obj2 are not Terms returns -1 (it means not equal)
 */
static int Term_cmp(PyObject *obj1, PyObject *obj2)
{
    // check if obj1 and obj2 are Terms
    if (PyObject_IsInstance(obj1, (PyObject *)&TermType) != 1 ||
        PyObject_IsInstance(obj2, (PyObject *)&TermType) != 1)
        return -1;

    if (PyObject_Compare(((Term *)obj1)->name, ((Term *)obj2)->name) == 0 &&
        PyObject_Compare(((Term *)obj1)->value, ((Term *)obj2)->value) == 0){
        return 0;
    }
    return 1;
}



static PyMethodDef Term_methods[] = {
    {NULL}  /* Sentinel */
};

/**
 * List of accessible members of Term.
 */
static PyMemberDef Term_members[] = {
    // value is accessible only for read
    {"name", T_OBJECT_EX, offsetof(Term, name), READONLY, "Name of the Term"},
    {"value", T_OBJECT_EX, offsetof(Term, value), READONLY, "Value of the Term"},
    {NULL}  /* Sentinel */
};

PyTypeObject TermType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "ycp.Term",             /*tp_name*/
    sizeof(Term), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Term_dealloc,/*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)Term_cmp,       /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    (hashfunc)Term_hash,/*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "YCP Terms",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Term_methods,             /* tp_methods */
    Term_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Term_init,/* tp_init */
    0,                         /* tp_alloc */
    Term_new,                 /* tp_new */
};


