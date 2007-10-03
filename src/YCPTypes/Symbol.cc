#include "YCPTypesInternal.h"

/**
 * Compare two Symbol objects.
 * If obj1 or obj2 are not Symbols returns -1 (it means not equal)
 */
static int Symbol_cmp(PyObject *obj1, PyObject *obj2)
{
    char *str1, *str2;
    int ret = 0;

    // check is obj1 and obj2 are Symbols
    if (PyObject_IsInstance(obj1, (PyObject *)&SymbolType) != 1 ||
        PyObject_IsInstance(obj2, (PyObject *)&SymbolType) != 1)
        return -1;

    str1 = PyString_AsString(((Symbol *)obj1)->value);
    str2 = PyString_AsString(((Symbol *)obj2)->value);

    ret = strcmp(str1, str2);
    if (ret != 0)
        return ret < 0 ? -1 : 1;
    return ret;
}


static PyObject *Symbol_str(PyObject *self)
{
    if (isSymbol(self)){
        Py_INCREF(((Symbol *)self)->value);
        return ((Symbol *)self)->value;
    }

    return Py_None;
}


static PyMethodDef Symbol_methods[] = {
    {"isSymbol", (PyCFunction)YCPType_isSymbol, METH_NOARGS, "Return true if object is Symbol."},
    {"isPath", (PyCFunction)YCPType_isPath, METH_NOARGS, "Return true if object is Path."},
    {"isTerm", (PyCFunction)YCPType_isTerm, METH_NOARGS, "Return true if object is Term."},
    {NULL}  /* Sentinel */
};

/**
 * List of accessible members of Symbol.
 */
static PyMemberDef Symbol_members[] = {
    // value is accessible only for read
    {"value", T_OBJECT_EX, offsetof(Symbol, value), READONLY, "Value of symbol"},
    {NULL}  /* Sentinel */
};

PyTypeObject SymbolType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "ycp.Symbol",             /*tp_name*/
    sizeof(Symbol), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)YCPTypeString_dealloc,/*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)Symbol_cmp,       /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    (hashfunc)YCPTypeString_hash,     /*tp_hash */
    0,                         /*tp_call*/
    (reprfunc)Symbol_str,      /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "YCP Symbols",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Symbol_methods,             /* tp_methods */
    Symbol_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)YCPTypeString_init,      /* tp_init */
    0,                         /* tp_alloc */
    YCPTypeString_new,                 /* tp_new */
};

