#include "YCPTypesInternal.h"
using std::string;

/**
 * Compare two Path objects.
 * If obj1 or obj2 are not Paths returns -1 (it means not equal)
 */
static int Path_cmp(PyObject *obj1, PyObject *obj2)
{
    char *str1, *str2;
    int ret = 0;

    // check is obj1 and obj2 are Paths
    if (PyObject_IsInstance(obj1, (PyObject *)&PathType) != 1 ||
        PyObject_IsInstance(obj2, (PyObject *)&PathType) != 1)
        return -1;

    str1 = PyString_AsString(((Path *)obj1)->value);
    str2 = PyString_AsString(((Path *)obj2)->value);

    ret = strcmp(str1, str2);
    if (ret != 0)
        return ret < 0 ? -1 : 1;
    return ret;
}

static PyObject *Path_str(PyObject *self)
{
    if (isPath(self)){
        Py_INCREF(((Path *)self)->value);
        return ((Path *)self)->value;
    }
    return Py_None;
}

/**
 * Returns New Reference!
 */
static PyObject *Path_append(Path *self, PyObject *arg)
{
    const char *str = PyString_AsString(self->value);
    string new_value(str);

    // check if arg is string
    if (!PyString_CheckExact(arg)){
        PyErr_SetString(PyExc_TypeError, ": argument 1 must be string");
        return Py_None;
    }

    // concate strings
    str = PyString_AsString(arg);
    new_value += ".";
    new_value += str;

    return Path_NewString(new_value.c_str());
}

/**
 * Returns New Reference!
 */
static PyObject *Path_prepend(Path *self, PyObject *arg)
{
    string new_value;

    // check if arg is string
    if (!PyString_CheckExact(arg)){
        PyErr_SetString(PyExc_TypeError, ": argument 1 must be string");
        return Py_None;
    }

    // concate strings
    new_value = PyString_AsString(arg);
    new_value += ".";
    new_value += PyString_AsString(self->value);

    return Path_NewString(new_value.c_str());
}

static PyMethodDef Path_methods[] = {
    {"append", (PyCFunction)Path_append, METH_O, "Return new Path object with appended path given in argument."},
    {"prepend", (PyCFunction)Path_prepend, METH_O, "Return new Path object with perpended path given in argument."},
    {"isCode", (PyCFunction)YCPType_isCode, METH_NOARGS, "Return true if object is Code."},
    {"isSymbol", (PyCFunction)YCPType_isSymbol, METH_NOARGS, "Return true if object is Symbol."},
    {"isPath", (PyCFunction)YCPType_isPath, METH_NOARGS, "Return true if object is Path."},
    {"isTerm", (PyCFunction)YCPType_isTerm, METH_NOARGS, "Return true if object is Term."},
    {NULL}  /* Sentinel */
};

/**
 * List of accessible members of Path.
 */
static PyMemberDef Path_members[] = {
    // value is accessible only for read
    {"value", T_OBJECT_EX, offsetof(Path, value), READONLY, "Value of symbol"},
    {NULL}  /* Sentinel */
};

PyTypeObject PathType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "ycp.Path",             /*tp_name*/
    sizeof(Path), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)YCPTypeString_dealloc,/*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)Path_cmp,       /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    (hashfunc)YCPTypeString_hash,/*tp_hash */
    0,                         /*tp_call*/
    (reprfunc)Path_str,        /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "YCP Paths",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Path_methods,             /* tp_methods */
    Path_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)YCPTypeString_init,/* tp_init */
    0,                         /* tp_alloc */
    YCPTypeString_new,                 /* tp_new */
};

