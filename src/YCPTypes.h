#ifndef _YCPTYPES_H_
#define _YCPTYPES_H_

#include <string>
#include "Python.h"
#include "structmember.h"

/**
 * Generic YCP type which has one string member named value
 * and one member for storing computed hash.
 */
typedef struct {
    PyObject_HEAD
    PyObject *value; //string
    long hash;
} YCPTypeString;

/**
 * Symbol
 */
typedef YCPTypeString Symbol;
extern PyTypeObject SymbolType;

bool isSymbol(PyObject *);
std::string Symbol_getValue(Symbol *);


/**
 * Path
 */
typedef YCPTypeString Path;
extern PyTypeObject PathType;

bool isPath(PyObject *);
std::string Path_getValue(Path *);


/**
 * Term
 * Term is composed from name (string) and value (tuple of various types)
 */
typedef struct{
    PyObject_HEAD
    PyObject *name; // string
    PyObject *value; // tuple of various types
    long hash;
} Term;
extern PyTypeObject TermType;

bool isTerm(PyObject *);
std::string Term_getName(Term *);

/**
 * Returns list or None.
 * Borrowed reference!
 */
PyObject *Term_getValue(Term *);


/**
 * Initialize alll YCP types
 */
bool initYCPTypes(PyObject *module);

bool isYCPType(PyObject *);


/**
 * Usage:
 *      switch (getType(obj)){
 *          case PATH:
 *            ...
 *          case SYMBOL:
 *            ...
 *      }
 */
enum YCPType { NOT_YCP_TYPE, PATH, SYMBOL, TERM };
YCPType getType(PyObject *);

#endif
