#include "YCPTypes.h"
#include "YCPTypes/YCPTypesInternal.h"
using std::string;

bool initYCPTypes(PyObject *module)
{
    if (PyType_Ready(&SymbolType) < 0)
        return false;
    if (PyType_Ready(&PathType) < 0)
        return false;
    if (PyType_Ready(&TermType) < 0)
        return false;

    Py_INCREF(&SymbolType);
    PyModule_AddObject(module, "Symbol", (PyObject *)&SymbolType);
    Py_INCREF(&PathType);
    PyModule_AddObject(module, "Path", (PyObject *)&PathType);
    Py_INCREF(&TermType);
    PyModule_AddObject(module, "Term", (PyObject *)&TermType);

    return true;
}

bool isYCPType(PyObject *obj)
{
    if (isSymbol(obj) || isPath(obj) || isTerm(obj))
        return true;
    return false;
}

YCPType getYCPType(PyObject *obj)
{
    if (isSymbol(obj))
        return SYMBOL;
    if (isPath(obj))
        return PATH;
    if (isTerm(obj))
        return TERM;
    return NOT_YCP_TYPE;
}


/***** Symbol *****/
bool isSymbol(PyObject *obj)
{
    if (PyObject_IsInstance(obj, (PyObject *)&SymbolType))
        return true;
    return false;
}

string Symbol_getValue(Symbol *obj)
{
    if (isSymbol((PyObject *)obj)){
        return string(PyString_AsString(obj->value));
    }
    return string();
}

PyObject *Symbol_New(PyObject *value)
{
    return YCPTypeString_New(value, &SymbolType);
}

PyObject *Symbol_NewString(const char *value)
{
    PyObject *val = Py_BuildValue("s", value);
    PyObject *ret = Symbol_New(val);
    Py_DECREF(val);

    return ret;
}
/***** Symbol END *****/


/***** Path *****/
bool isPath(PyObject *obj)
{
    if (PyObject_IsInstance(obj, (PyObject *)&PathType))
        return true;
    return false;
}

string Path_getValue(Path *obj)
{
    if (isPath((PyObject *)obj)){
        return string(PyString_AsString(obj->value));
    }
    return string();
}

PyObject *Path_New(PyObject *value)
{
    return YCPTypeString_New(value, &PathType);
}

PyObject *Path_NewString(const char *value)
{
    PyObject *val = Py_BuildValue("s", value);
    PyObject *ret = Path_New(val);
    Py_DECREF(val);

    return ret;
}
/***** Path END *****/


/***** Term *****/
bool isTerm(PyObject *obj)
{
    if (PyObject_IsInstance(obj, (PyObject *)&TermType))
        return true;
    return false;
}

string Term_getName(Term *obj)
{
    if (isTerm((PyObject *)obj)){
        return string(PyString_AsString(obj->name));
    }
    return string();
}

PyObject *Term_getValue(Term *obj)
{
    if (isTerm((PyObject *)obj)){
        return obj->value;
    }
    return Py_None;
}


PyObject *Term_New(PyObject *name, PyObject *value)
{
    PyObject *ret;
    PyObject *args;
    int size, i;
    PyObject *tmp;

    if (!PyTuple_Check(value) || !PyString_Check(name)){
        return Py_None;
    }

    // create args variable
    size = PyTuple_Size(value);
    args = PyTuple_New(size + 1);
    Py_INCREF(name);
    if (PyTuple_SetItem(args, 0, name) != 0){
        Py_XDECREF(args);
        Py_DECREF(name);
        return Py_None;
    }
    for (i=1; i < size + 1; i++){
        tmp = PyTuple_GetItem(value, i-1);
        Py_INCREF(tmp);
        if (PyTuple_SetItem(args, i, tmp) != 0){
            Py_XDECREF(args);
            Py_DECREF(tmp);
            return Py_None;
        }
    }

    // create new object
    ret = Term_new(&TermType, Py_None, Py_None);
    if (ret == NULL){
        Py_XDECREF(args);
        return Py_None;
    }

    // initialize object
    if (Term_init((Term *)ret, args, Py_None) == -1){
        Py_XDECREF(args);
        return Py_None;
    }

    Py_XDECREF(args);
    return ret;
}

PyObject *Term_NewString(const char *name, PyObject *value)
{
    PyObject *nam = Py_BuildValue("s", name);
    PyObject *ret = Term_New(nam, value);
    Py_DECREF(nam);

    return ret;
}
/***** Term END *****/

