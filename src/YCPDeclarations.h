#ifndef _YCPDECLARATIONS_H_
#define _YCPDECLARATIONS_H_

#include <Python.h>
#include <ycp/Type.h>
#include <vector>
#include <string>
#include <memory>

/**
 * This class stores information about declarations in python module which were
 * done by YCPDeclarations module (YCPDeclaratios.py).
 * This is class is singelton and static method instance() returns pointer to
 * object.
 *
 * All methods which return any information about declared functions are
 * called with argument pointer to PyFunctionObject (which identifies
 * function unambiguously.
 *
 * Example of usage:
 *
 *      #include "YCPDeclarations.h"
 *
 *      PyObject *func = PyDict_GetItemString(dict, "function");
 *      YCPDeclarations *decl = YCPDeclarations::instance();
 *      int num_params = decl->numParams((PyFunctionObject *)func);
 *      ...
 *
 */
class YCPDeclarations {
  private:
    /**
     * structure where can be stored cached function.
     */
    typedef struct{
        PyFunctionObject *function;
        constTypePtr return_type;
        std::vector<constTypePtr> parameters;
    } cache_function_t;


    /**
     * Pointer to Python module YCPDeclarations.
     */
    PyObject *_py_self;

    /**
     * List of cached functions.
     */
    std::vector<cache_function_t *> _cache;

    /**
     * Private construct.
     * Call YCPDeclarations::instance() to get pointer to YCPDeclarations
     * object.
     */
    YCPDeclarations();

    /**
     * Return item from function map which has key key.
     * Return borrowed reference!
     */
    PyObject *_getItemFromFunctionMap(PyObject *key);

    /**
     * Interpret string as YCP type.
     * This method must be synchronized with variable
     * YCPDeclare._available_types from YCPDeclarations.py!!
     */
    constTypePtr _interpretType(const char *) const;

    /**
     * Return true, if func is in internal cache.
     */
    bool _isInCache(PyFunctionObject *func) const;

    /**
     * Cache function func if it is not already cached.
     */
    void _cacheFunction(PyFunctionObject *func);

    /**
     * Return pointer to struct which defines cached function.
     * Memory pointed by returned pointer must _not_ be deleted! It points
     * into internal list.
     */
    const cache_function_t *_getCachedFunction(PyFunctionObject *func) const;


    /**
     * Try to initialize _py_self. If _py_self is already initialized, nothing is done.
     */
    bool _init();

  public:
    ~YCPDeclarations();

    /**
     * Return number of parameters in declaration or -1 if function is not registered.
     */
    int numParams(PyFunctionObject *pointer_to_function);

    /**
     * Return true if function exists in YCPDeclarations module.
     */
    bool exists(PyFunctionObject *pointer_to_function);

    /**
     * Return list of YCP types corresponding with parameters fo function.
     */
    std::vector<constTypePtr> params(PyFunctionObject *pointer_to_function);

    /**
     * Return return YCP type of function.
     */
    constTypePtr returnType(PyFunctionObject *pointer_to_function);

    /**
     * Initialize class.
     */
    bool init();

  //static
  private:
    /**
     * Here is stored pointer to YCPDeclare object.
     */
    static YCPDeclarations _instance;
  public:
    /**
     * Return pointer to instance of YCPDeclare object.
     */
    static YCPDeclarations *instance();
};

#endif
/* vim: set sw=4 ts=4 et ft=cpp cindent : */
