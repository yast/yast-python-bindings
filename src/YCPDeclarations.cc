#include "YCPDeclarations.h"
#include <iostream>

#define y2log_component "YCPDeclarations"
#include <ycp/y2log.h>

using std::string;
using std::vector;
#define DBG(str) \
    std::cerr << __FILE__ << ": " << __LINE__ << ": " << str << std::endl; \
    std::cerr.flush()


/********** STATIC MEMBERS **********/
YCPDeclarations YCPDeclarations::_instance;
YCPDeclarations *YCPDeclarations::instance()
{
    return &_instance;
}

/********** STATIC MEMBERS END **********/




/********** PRIVATE **********/
bool YCPDeclarations::_isInCache(PyFunctionObject *func) const
{
    int len = _cache.size();
    for (int i=0; i < len; i++){
        if (_cache[i]->function == func)
            return true;
    }

    return false;
}

void YCPDeclarations::_cacheFunction(PyFunctionObject *func)
{
    PyObject *item;
    PyObject *params;
    PyObject *return_type;
    PyObject *tmp;
    cache_function_t *function;
    Py_ssize_t tuple_size;

    if (!_init())
        return;

    if (_isInCache(func)){
        y2debug("function (%ld, %s) is already in cache.", (long)func, PyString_AsString(func->func_name));
        return;
    }

    item = _getItemFromFunctionMap((PyObject *)func);
    if (item == NULL || !PyDict_Check(item)){
        y2debug("function (%ld, %s) is not declared using YCPDeclare", (long)func, PyString_AsString(func->func_name));
        return;
    }

    return_type = PyDict_GetItemString(item, "return_type");
    if (return_type == NULL || !PyString_Check(return_type)){
        y2debug("Invalid return type of function (%ld, %s)", (long)func, PyString_AsString(func->func_name));
        return;
    }
    params = PyDict_GetItemString(item, "parameters");
    if (params == NULL || !PyTuple_Check(params)){
        y2debug("Invalid parameters of function (%ld, %s)", (long)func, PyString_AsString(func->func_name));
        return;
    }

    //allocate memory
    function = new cache_function_t;

    //function
    function->function = func;

    //return type:
    function->return_type = _interpretType(PyString_AsString(return_type));

    //parameters:
    tuple_size = PyTuple_Size(params);
    for (Py_ssize_t i=0; i < tuple_size; i++){
        tmp = PyTuple_GetItem(params, i);
        function->parameters.push_back(_interpretType(PyString_AsString(tmp)));
    }

    //add new function item
    _cache.push_back(function);
    y2debug("function (%ld, %s) cached", (long)func, PyString_AsString(func->func_name));
}

const YCPDeclarations::cache_function_t *YCPDeclarations::_getCachedFunction(PyFunctionObject *func) const
{
    cache_function_t *ret = NULL;
    int len = _cache.size();

    y2debug("Searching for function (%ld, %s)...", (long)func, PyString_AsString(func->func_name));
    for (int i=0; i < len; i++){
        if (_cache[i]->function == func){
            y2debug("    ==> Function found on position %d", i);
            ret = _cache[i];
            break;
        }
    }

    if (ret == NULL){
        y2debug("    ==> Function not found");
    }

    return ret;
}


PyObject *YCPDeclarations::_getItemFromFunctionMap(PyObject *key)
{
    if (!_init())
        return NULL;

    if (_py_self == NULL)
        return NULL;

    PyObject *dict = PyModule_GetDict(_py_self);
    PyObject *func_map = PyDict_GetItemString(dict, "_function_map");

    if (!PyDict_Check(func_map)){
        y2error("Map _function_map not found in python module YCPDeclarations");
        return NULL;
    }

    return PyDict_GetItem(func_map, key);
}


constTypePtr YCPDeclarations::_interpretType(const char *c_type) const
{
    string type(c_type);

    if (type == "void")
        return Type::Void;
    if (type == "boolean")
        return Type::Boolean;
    if (type == "float")
        return Type::Float;
    if (type == "integer")
        return Type::Integer;
    if (type == "path")
        return Type::Path;
    if (type == "string")
        return Type::String;
    if (type == "symbol")
        return Type::Symbol;
    if (type == "term")
        return Type::Term;
    if (type == "map")
        return Type::Map;
    if (type == "list")
        return Type::List;

    // default:
    return Type::Any;
}


bool YCPDeclarations::_init()
{
    if (_py_self != NULL)
        return true;

    if (!Py_IsInitialized()){
        y2error("Python interpret is not initialized!");
        return false;
    }

    _py_self = PyImport_ImportModule("YCPDeclarations");
    if (_py_self == NULL){
        y2error("Failed to import YCPDeclarations module!");
        return false;
    }

    y2milestone("YCPDeclarations successfuly initialized!");
    return true;
}
/********** PRIVATE END **********/




/********** PUBLIC **********/

YCPDeclarations::YCPDeclarations() : _py_self(NULL)
{
    y2debug("Constructor called");
}

YCPDeclarations::~YCPDeclarations()
{
    int cache_len = _cache.size();
    for (int i=0; i < cache_len; i++){
        delete _cache[i];
    }

    if (_py_self != NULL)
        Py_DECREF(_py_self);

    y2debug("Destructor called");
}


int YCPDeclarations::numParams(PyFunctionObject *func)
{
    _cacheFunction(func);

    const cache_function_t *function = _getCachedFunction(func);
    if (function == NULL)
        return -1;

    y2debug("Number of parameters of function (%ld, %s) is %d",
            (long)func, PyString_AsString(func->func_name), (int)function->parameters.size());
    return function->parameters.size();
}

bool YCPDeclarations::exists(PyFunctionObject *func)
{
    _cacheFunction(func);

    return _isInCache(func);
}

vector<constTypePtr> YCPDeclarations::params(PyFunctionObject *func)
{
    _cacheFunction(func);

    const cache_function_t *function = _getCachedFunction(func);
    if (function == NULL){
        return vector<constTypePtr>();
    }

    return function->parameters;
}

constTypePtr YCPDeclarations::returnType(PyFunctionObject *func)
{
    _cacheFunction(func);

    const cache_function_t *function = _getCachedFunction(func);
    if (function == NULL){
        return _interpretType("any");
    }

    return function->return_type;
}

bool YCPDeclarations::init()
{
    return _init();
}
/********** PUBLIC END **********/
