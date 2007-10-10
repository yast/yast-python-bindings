"""
 This module defines class YCPDeclare which can be used for defining
 what return type and what types of arguments has function which will be
 exported to YCP. For usage see YCPDeclare.__doc__.


 Internal:
 Important is variable _function_map which holds information about
 functions. Contents of _function_map can be accessed from C:

    PyObject *import = PyImport_ImportModule("YCPDeclarations");
    PyObject *dict = PyModule_GetDict(import);
    PyObject *func_map = PyDict_GetItemString(dict, "_function_map");
    // now in func_map should be stored map describing functions declared by
    // YCPDeclare

 _function_map has form:
    _function_map = {
        pointer_to_function : {
            "return_type" : "string",
            "parameters" : [ list of strings representing types ]
        }
    }

"""

import inspect

_function_map = {}
def _addToFunctionMap(func_pointer, return_type, params_types):
    global __function_map
    _function_map[func_pointer] = {"return_type" : return_type,
                                   "parameters" : params_types}

class YCPDeclare:
    """
     Functor for definig return type and types of parameters
     of function which will be exported into YCP. Best usage
     is as decorator (see http://www.python.org/dev/peps/pep-0318).

     Example of usage:
         form YCPDeclarations import YCPDeclare

         @YCPDeclare("string", "int", "int")
         def function(i, ii):
             \"\"\" Function which returns string a accept two
                    integers as arguments. \"\"\"
             return str(i+ii)
    """

    # tuple of types which can be used
    # This list must be synchronized with
    # YCPDeclarations::_interpretType function from YCPDeclarations.h!!
    _available_types = (
        "any",
        "boolean",
        "string",
        "integer",
        "term",
        "symbol",
        "path",
        "float"
    )

    def __init__(self, return_type, *params_types):
        self._return_type = ""
        self._params = []

        self._checkTypes((return_type,) + params_types)

        self._return_type = return_type
        self._params = params_types

    def __call__(self, func):
        """ Overridden operator() """

        self._checkNumParams(func, len(self._params))

        _addToFunctionMap(func, self._return_type, self._params)
        return func


    def _checkTypes(self, types):
        """ Check if defined types are in _available_types """

        _invalid_types = []
        for type in types:
            if type not in self._available_types:
                _invalid_types.append(type)

        if len(_invalid_types) != 0:
            raise Exception("Unknnown types: " + str(_invalid_types))


    def _checkNumParams(self, func, numTypes):
        """ Check if number of parameters equals to number of defined types """

        args = len(inspect.getargspec(func)[0])
        if args != numTypes:
            raise Exception("Number of declared types does not match number of arguments.")
        

