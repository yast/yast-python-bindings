#include "YCPDeclarations.h"
#include <iostream>
using std::string;
using std::vector;
//#define DBG(str) \
    std::cerr << __FILE__ << ": " << __LINE__ << ": " << str << std::endl; \
    std::cerr.flush()
#define DBG(str)


/********** STATIC MEMBERS **********/
std::auto_ptr<YCPDeclarations> YCPDeclarations::_instance;
YCPDeclarations *YCPDeclarations::instance()
{
    if (_instance.get() == 0){
        _instance = std::auto_ptr<YCPDeclarations>(new YCPDeclarations());
    }
    return _instance.get();
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

    DBG("Called _cacheFunction(" << (long)func << ")");

    if (_isInCache(func)){
        DBG("YCPDeclarations::_cacheFunction(" << (long)func << ") - is in cache");
        return;
    }

    item = _getItemFromFunctionMap((PyObject *)func);
    if (item == NULL || !PyDict_Check(item)){
        DBG("YCPDeclarations::_cacheFunction(" << (long)func << ") - " << "error in item: " << (long)item);
        return;
    }

    return_type = PyDict_GetItemString(item, "return_type");
    if (return_type == NULL || !PyString_Check(return_type)){
        DBG("YCPDeclarations::_cacheFunction(" << (long)func << ") - " << "error in return_type: " << (long)return_type);
        return;
    }
    params = PyDict_GetItemString(item, "parameters");
    if (params == NULL || !PyTuple_Check(params)){
        DBG("YCPDeclarations::_cacheFunction(" << (long)func << ") - " << "error in params: " << (long)params);
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
    DBG("_cacheFunction(" << (long)func << ") - _cache.size() : " << _cache.size());
}

const YCPDeclarations::cache_function_t *YCPDeclarations::_getCachedFunction(PyFunctionObject *func) const
{
    cache_function_t *ret = NULL;
    int len = _cache.size();

    DBG("");
    DBG("_getCachedFunction(" << (long)func << ") - " << "start searching");
    for (int i=0; i < len; i++){
        DBG("== " << "_cache[" << i << "]->function: " << (long)_cache[i]->function);
        if (_cache[i]->function == func){
            ret = _cache[i];
            break;
        }
    }

    DBG("_getCachedFunction(" << (long)func << ") -> " << (long)ret);
    DBG("");
    return ret;
}


PyObject *YCPDeclarations::_getItemFromFunctionMap(PyObject *key)
{
    if (_py_self == NULL)
        return NULL;

    PyObject *dict = PyModule_GetDict(_py_self);
    PyObject *func_map = PyDict_GetItemString(dict, "_function_map");

    if (!PyDict_Check(func_map)){
        return NULL;
    }
    DBG("_function_map : " << (long)func_map);

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

    // default:
    return Type::Any;
}
/********** PRIVATE END **********/




/********** PUBLIC **********/

YCPDeclarations::YCPDeclarations()
{
    DBG("YCPDeclarations - constructor");
    _py_self = PyImport_ImportModule("YCPDeclarations");
    if (_py_self == NULL){
        DBG("YCPDeclarations::YCPDeclarations() - Failed to import YCPDeclarations module!");
    }
}

YCPDeclarations::~YCPDeclarations()
{
    DBG("YCPDeclarations - destructor");

    int cache_len = _cache.size();
    for (int i=0; i < cache_len; i++){
        delete _cache[i];
    }

    if (_py_self != NULL)
        Py_DECREF(_py_self);
}



int YCPDeclarations::numParams(PyFunctionObject *func)
{
    _cacheFunction(func);

    const cache_function_t *function = _getCachedFunction(func);
    if (function == NULL)
        return -1;

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
/********** PUBLIC END **********/
