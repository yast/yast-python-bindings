#include "YCPTypes.h"
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

YCPType getType(PyObject *obj)
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
    if (PyInstance_Check(obj)
        && PyObject_IsInstance(obj, (PyObject *)&SymbolType))
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
/***** Symbol END *****/


/***** Path *****/
bool isPath(PyObject *obj)
{
    if (PyInstance_Check(obj)
        && PyObject_IsInstance(obj, (PyObject *)&PathType))
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
/***** Path END *****/


/***** Term *****/
bool isTerm(PyObject *obj)
{
    if (PyInstance_Check(obj)
        && PyObject_IsInstance(obj, (PyObject *)&TermType))
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
/***** Term END *****/

