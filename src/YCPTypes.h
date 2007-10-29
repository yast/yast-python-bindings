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
 * Return new object created from str.
 * Return New Reference!
 */
PyObject *Symbol_New(PyObject *str);
PyObject *Symbol_NewString(const char *);


/**
 * Path
 */
typedef YCPTypeString Path;
extern PyTypeObject PathType;

bool isPath(PyObject *);
std::string Path_getValue(Path *);

PyObject *Path_New(PyObject *str);
PyObject *Path_NewString(const char *);


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

PyObject *Term_New(PyObject *name, PyObject *list_value);
PyObject *Term_NewString(const char *name, PyObject *list_value);

/**
 * Code
 * Code is composed from value (pointer to function call)
 */
typedef struct{
    PyObject_HEAD
    PyObject *value; // pointer to function
    long hash;
} Code;
extern PyTypeObject CodeType;

bool isCode(PyObject *);


/**
 * Returns list or None.
 * Borrowed reference!
 */
PyObject *Code_getValue(Code *);

PyObject *Code_New(PyObject *value);



/**
 * Initialize all YCP types
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
enum YCPType { NOT_YCP_TYPE, PATH, SYMBOL, TERM, CODE };
YCPType getYCPType(PyObject *);

#endif
