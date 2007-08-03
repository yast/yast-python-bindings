/**
 * 
 *
 * This is the path from Python to YCP. It defines XSUBs.
 */

#include <Python.h>
#include <y2/Y2Namespace.h>
#include <y2/Y2Component.h>
#include <y2/Y2ComponentCreator.h>
#include <ycp/y2log.h>
#include <ycp/YBlock.h>
#include <ycp/YExpression.h>
#include <ycp/YStatement.h>
#include <ycp/Import.h>
#include <yui/YUIComponent.h>
#include <wfm/Y2WFMComponent.h>
#include <ycp/YCPMap.h>

#include "YPython.h"



PyObject * Call_YCPFunction (PyObject *args);

/**
 * init namespace
 * @param char * name of module
 * @param char * name of function
 * @return namespace of YCP
 */

static Y2Namespace * getNs (const char * ns_name, const char * func_name) {
  Import import(ns_name);	// has a static cache
  Y2Namespace *ns = import.nameSpace();
  if (ns == NULL) {
     y2error ("... for a Python call of %s", func_name);
     //printf("... for a Python call of %s\n", func_name);
  } else {
     ns->initialize ();
  }
  return ns;
}


static PyObject * ycp_handle_function(PyObject *self, PyObject *args) {
  return Call_YCPFunction (args);
}



static PyMethodDef YCPMethods[] = {
  {"run",  ycp_handle_function, METH_VARARGS, "Calling YCP from Python"},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initycp(void) {
  (void) Py_InitModule("ycp", YCPMethods);
}





PyObject * Call_YCPFunction (PyObject *args) {


  int number_args = PyTuple_Size(args);
  char * ns_name = new char[101];
  char * func_name = new char[101];
  PyObject * pPythonValue;
  PyObject * pReturnValue;
  YCPValue ycpArg = YCPNull ();
  YCPValue ycpRetValue = YCPNull ();

  
  YPython *ypython = YPython::yPython ();
  if (number_args >= 2) {
     //obtain name of namespace (first argument)
     pPythonValue = PyTuple_GetItem(args, 0);
     if (pPythonValue) {
        if (PyString_Check(pPythonValue)) {
           ns_name = strcpy(ns_name, PyString_AsString(pPythonValue)); 

        } else {
           y2error ("Wrong type of name for namespace. String is necessary.");
           //printf("Wrong type of name for namespace. String is necessary.\n");
         
           return PyInt_FromLong(-1);
        }

     } else {
        y2error ("Missing name of namespace.");
        //printf("Missing name of namespace.\n");
        return PyInt_FromLong(-1);

     }
     //obtain name of function (second argumet)
     pPythonValue = PyTuple_GetItem(args, 1);
     if (pPythonValue) {
        if (PyString_Check(pPythonValue)) {
           func_name = strcpy(func_name, PyString_AsString(pPythonValue)); 

        } else {
           y2error ("Wrong type of name for function. String is necessary.");
           //printf("Wrong type of name for function. String is necessary..\n");
           return PyInt_FromLong(-1);
        }

     } else {
        y2error ("Missing name of function.");
        //printf("Missing name of function.\n");
        return PyInt_FromLong(-1);

     }
     //printf("namespace: %s\n", ns_name);
     //printf("function: %s\n", func_name);
     // create namespace
     Y2Namespace *ns = getNs (ns_name, func_name);
     if (ns == NULL) {
        y2error ("Creating namespace fault.");
        //printf("Creating namespace fault..\n");
        return PyInt_FromLong(-1);
     }
     // we want either a function or a variable
     // so find a symbol of an unspecified category
     TableEntry *sym_te = ns->table ()->find (func_name);
     if (sym_te == NULL) {
	y2error ("No such symbol %s::%s", ns_name, func_name);
        //printf("No such symbol %s::%s\n", ns_name, func_name);
	return PyInt_FromLong(-1);
     }

     Y2Function *func_call = ns->createFunctionCall (func_name, NULL);
     if (func_call == NULL) {
	y2error ("No such function %s::%s", ns_name, func_name);
        //printf("No such symbol %s::%s\n", ns_name, func_name);
        return PyInt_FromLong(-1);
     }
     
     for (int i=2; i< number_args; i++) {
         pPythonValue = PyTuple_GetItem(args, i);
         if (pPythonValue) {
            if (!(ypython->PythonTypeToYCPSimpleType(pPythonValue,ycpArg))) {
               ycpArg = ypython->fromPythonListToYCPList (pPythonValue);
               if (ycpArg.isNull())
                  ycpArg = ypython->fromPythonDictToYCPMap (pPythonValue);
            }
            bool ok = func_call->appendParameter (ycpArg);
	    if (!ok) {
               y2error ("Problem with adding arguments of function %s", func_name);
               //printf("Problem with adding arguments of function %s\n", func_name);
               return PyInt_FromLong(-1);
	    }
         } else {
            y2error ("Missing argument of function.");
            //printf("Missing argument of function.\n");
            return PyInt_FromLong(-1);

         }
     }
     bool ok = func_call->finishParameters ();
     if (!ok) {
	y2error ("Problem with finishing arguments for adding arguments of function %s", func_name);
        //printf("Problem with finishing arguments for adding arguments of function %s\n", func_name);
        return  PyInt_FromLong(-1);
     }
     ycpRetValue = func_call->evaluateCall ();
     delete func_call;
     if (ycpRetValue.isNull ()) {
	y2error ("Return value of function %s is NULL", func_name);
        //printf("Return value of function %s is NULL\n", func_name);
        return PyInt_FromLong(-1);
     }
     delete []ns_name;
     delete []func_name;
     pReturnValue = ypython->YCPTypeToPythonSimpleType(ycpRetValue);
     if (!pReturnValue)
         pReturnValue = ypython->fromYCPListToPythonList(ycpRetValue);
     if (!pReturnValue)
         pReturnValue = ypython->fromYCPMapToPythonDict(ycpRetValue);
     return pReturnValue;
     
  } else {
     y2error ("Number of arguments is not enough.");
     //printf("Number of arguments is not enough.\n");
     return PyInt_FromLong(-1);
  }    

}

int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initycp();

    Py_Finalize();
}
