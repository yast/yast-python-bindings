#include "YCPTypesInternal.h"

/**
 * Deallocate Code object
 */
static void Code_dealloc(Code *self)
{
    //Py_XDECREF(self->name);
    Py_XDECREF(self->value);
    self->ob_type->tp_free((PyObject *)self);
}

/**
 * This function is called before Code_init.
 * In this function is set only default values.
 */
PyObject *Code_new(PyTypeObject *type, PyObject *args,
                                         PyObject *kwds)
{
    Code *self;

    self = (Code *)type->tp_alloc(type, 0);
    if (self != NULL){
        self->value = Py_None;
        if (self->value == NULL){
            Py_XDECREF(self);
            return NULL;
        }

        self->hash = -1;
    }

    return (PyObject *)self;
}

/**
 * Initialize Code object.
 */
int Code_init(Code *self, PyObject *args, PyObject *kwds)
{
    //PyObject *name = NULL;
    PyObject *value = NULL;
    PyObject *tmp;
   // PyObject *pReturn;
    int args_size;

    // check number of arguments
    args_size = PyTuple_Size(args);
    if (args_size < 1){
        PyErr_SetString(PyExc_TypeError, ": function takes exactly 1 argument (0 given)");
        return -1;
    }

    // value:
    value = PyTuple_GetItem(args, 0);
    if (PyFunction_Check(value)){
        tmp = PyFunction_GetCode(self->value);
        Py_INCREF(value);
        self->value = value;
        /*
        printf("Code_init...\n");
	pReturn = PyObject_CallObject(self->value, NULL);
        if (pReturn != NULL)
           printf("Calling value: %d",PyInt_AsLong(pReturn));
        else
           printf("pReturn == NULL");*/
        Py_XDECREF(tmp);
    } else {
        PyErr_SetString(PyExc_TypeError, ": argument 1 must be function");
        return -1;
    }
    /*
    // value:
    if (args_size > 1){
        value = PyTuple_GetSlice(args, 1, args_size); // return new reference
        if (value != NULL){
            tmp = self->value;
            self->value = value;
            Py_XDECREF(tmp);
        }
    }
    */
    return 0;
}

/**
 * Returns hash of Term object.
 */
static long Code_hash(Code *self)
{
    if (self->hash == -1){
        self->hash = PyObject_Hash(self->value);
    }
    return self->hash;
}

/**
 * Compare two Code objects.
 * If obj1 or obj2 are not Code returns -1 (it means not equal)
 */
static int Code_cmp(PyObject *obj1, PyObject *obj2)
{
    // check if obj1 and obj2 are Terms
    if (PyObject_IsInstance(obj1, (PyObject *)&CodeType) != 1 ||
        PyObject_IsInstance(obj2, (PyObject *)&CodeType) != 1)
        return -1;

    if (PyObject_Compare(((Code *)obj1)->value, ((Code *)obj2)->value) == 0){
        return 0;
    }
    return 1;
}


static PyMethodDef Code_methods[] = {
    {"isCode", (PyCFunction)YCPType_isCode, METH_NOARGS, "Return true if object is Code."},
    {"isSymbol", (PyCFunction)YCPType_isSymbol, METH_NOARGS, "Return true if object is Symbol."},
    {"isPath", (PyCFunction)YCPType_isPath, METH_NOARGS, "Return true if object is Path."},
    {"isTerm", (PyCFunction)YCPType_isTerm, METH_NOARGS, "Return true if object is Term."},
    {NULL}  /* Sentinel */
};

/**
 * List of accessible members of Term.
 */
static PyMemberDef Code_members[] = {
    // value is accessible only for read
    {"value", T_OBJECT_EX, offsetof(Code, value), READONLY, "Value of the Code"},
    {NULL}  /* Sentinel */
};

PyTypeObject CodeType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "ycp.Code",             /*tp_name*/
    sizeof(Code), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Code_dealloc,/*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)Code_cmp,       /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    (hashfunc)Code_hash,/*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "YCP Code",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Code_methods,             /* tp_methods */
    Code_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Code_init,/* tp_init */
    0,                         /* tp_alloc */
    Code_new,                 /* tp_new */
};


