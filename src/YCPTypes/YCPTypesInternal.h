#ifndef _YCP_TYPES_INTERNAL_H_
#define _YCP_TYPES_INTERNAL_H_

#include <iostream>
#define DBG(str) \
    std::cerr << str << std::endl

#include "YCPTypes.h"

/********** YCPTypeString fucntions **********/
/**
 * Function which deallocate YCPTypeString type
 */
void YCPTypeString_dealloc(YCPTypeString *self);

/**
 * Create new YCPTypeString object. This function is called before _init function.
 */
PyObject *YCPTypeString_new(PyTypeObject *type, PyObject *args,
                                         PyObject *kwds);

/**
 * Initialize YCPTypeString object.
 */
int YCPTypeString_init(YCPTypeString *self, PyObject *args, PyObject *kwds);

/**
 * Returns hash value of YCPTypeString object
 */
long YCPTypeString_hash(YCPTypeString *self);

/**
 * Return new object that has type type.
 */
PyObject *YCPTypeString_New(PyObject *str, PyTypeObject *type);



PyObject *Term_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int Term_init(Term *self, PyObject *args, PyObject *kwds);
#endif
