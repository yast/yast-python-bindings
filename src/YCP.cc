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
//#include <ycp/YBlock.h>
#include <ycp/YExpression.h>
#include <ycp/YStatement.h>
#include <ycp/Import.h>
#include <yui/YUIComponent.h>
#include <wfm/Y2WFMComponent.h>
#include <ycp/YCPMap.h>
#include <ycp/YCPList.h>
#include <ycp/YCPString.h>
#include <ycp/SymbolTable.h>

#include "YPython.h"


YCPList ycp_ListFunctions;

PyObject * Call_YCPFunction (PyObject *args);

PyObject * Import_YCPNameSpace (PyObject *args);

PyObject * Init_UI (PyObject *args);


static bool HandleSymbolTable (const SymbolEntry & se) {
  if (se.isFunction ()) {

     ycp_ListFunctions->add(YCPString(se.name()));

     cout << se.name() << endl;
     constFunctionTypePtr type = (constFunctionTypePtr)se.type();
     if (type->parameters())
        cout << type->parameters()->toString() << endl;


  }
  return true;
}

/*
void MyClass::Foo () {
  my_y2namespace->table()->forEach (&DoIt);
}
*/


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


static PyObject * ycp_import_namespace(PyObject *self, PyObject *args) {

  return Import_YCPNameSpace (args);
}

static PyObject * ycp_init_ui(PyObject *self, PyObject *args) {

  return Init_UI (args);
}

static PyMethodDef YCPMethods[] = {
  {"run",  ycp_handle_function, METH_VARARGS, "Calling YCP from Python"},
  {"import_module",  ycp_import_namespace, METH_VARARGS, "Import namespace from YCP module"},
  {"init_ui",  ycp_init_ui, METH_VARARGS, "Initialization of UI for YCP"},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initycp(void) {

  char func_code[] = 
    "def _factory(module, name):\n\
	def FunctionCall(*args):\n\
	   return ycp.run(module, name, *args)\n\
	return FunctionCall";

  (void) Py_InitModule("ycp", YCPMethods);


  PyRun_SimpleString(func_code);

}



bool RegFunctions(char *NameSpace, YCPList list_functions) {

  string reg_line_dict = "ycp.__dict__['";
  string reg_line_name;
  string reg_line_factory = " = _factory(\"";
  reg_line_factory += NameSpace;
  reg_line_factory += "\",\"";
  reg_line_name.insert(0,NameSpace);
  reg_line_name += "_";
  string function;
  string command;


  for (int i=0; i<list_functions.size();i++) {
    function = list_functions->value(i)->asString()->value();

    command = reg_line_dict;
    command += reg_line_name;
    command += function;
    command += "']";
    command +=reg_line_factory;
    command += function;
    command += "\")";

    PyRun_SimpleString(command.c_str());
    //printf("command for ycp %s\n", command.c_str());
  
  }

  return true;

}

Y2Component *owned_uic = 0;

PyObject * Init_UI (PyObject *args) {

  PyObject * pPythonValue;
  PyObject* pResult = PyBool_FromLong(0);
  int number_args = PyTuple_Size(args);
  string ui_name = "ncurses";

  if (number_args == 1) {
     pPythonValue = PyTuple_GetItem(args, 0);
     if (pPythonValue) {
        if (PyString_Check(pPythonValue)) {
           ui_name = PyString_AsString(pPythonValue); 

        } else {
           y2error ("Wrong type of function argument. String is necessary.");
           return pResult;
        }
     }
  } else if (number_args != 0) {
	y2error ("Zero or one arguments required (ui name, default %s", ui_name.c_str());
	return pResult;
  }

  Y2Component *c = YUIComponent::uiComponent ();

  if (c == 0) {
     y2debug ("UI component not created yet, creating %s", ui_name.c_str());
     c = Y2ComponentBroker::createServer (ui_name.c_str());

     if (c == 0) {
        y2error ("Cannot create component %s", ui_name.c_str());
        return pResult;
     }

     if (YUIComponent::uiComponent () == 0) {
        y2error ("Component %s is not a UI", ui_name.c_str());
        return pResult;
     } else {
        // got it - initialize, remember
        c->setServerOptions (0, NULL);
        owned_uic = c;
     }
  } else {
     y2debug ("UI component already present: %s", c->name ().c_str ());
  }
  return PyBool_FromLong(1);
}

PyObject * Import_YCPNameSpace (PyObject *args) {

  PyObject* pResult = PyBool_FromLong(0);
  PyObject * pPythonValue;
  int number_args = PyTuple_Size(args);
  char * ns_name = new char[101];
  

  if (number_args == 1) {
     pPythonValue = PyTuple_GetItem(args, 0);
     if (pPythonValue) {
        if (PyString_Check(pPythonValue)) {
           ns_name = strcpy(ns_name, PyString_AsString(pPythonValue)); 

        } else {
           y2error ("Wrong type of name for namespace. String is necessary.");
           //printf("Wrong type of name for namespace. String is necessary.\n");
         
           return pResult;
        }
        Import import(ns_name);	// has a static cache
        Y2Namespace *ns = import.nameSpace();
        if (ns == NULL) {

           return pResult;
        } else {
           ns->initialize ();
        }


        //printf("List of function:\n");
        ns->table()->forEach (&HandleSymbolTable);
        //printf("End list\n");


        RegFunctions(ns_name, ycp_ListFunctions);
        delete [] ns_name;

        pResult = PyBool_FromLong(1);
     }

  } else {
     PyErr_SetString(PyExc_SyntaxError,"Wrong number of arguments");
     pResult = PyBool_FromLong(0);
  }

  
  return pResult;
  

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
         
           return PyExc_TypeError;
        }

     } else {
        y2error ("Missing name of namespace.");
        //printf("Missing name of namespace.\n");
        return PyExc_SyntaxError;

     }
     //obtain name of function (second argumet)
     pPythonValue = PyTuple_GetItem(args, 1);
     if (pPythonValue) {
        if (PyString_Check(pPythonValue)) {
           func_name = strcpy(func_name, PyString_AsString(pPythonValue)); 

        } else {
           y2error ("Wrong type of name for function. String is necessary.");
           //printf("Wrong type of name for function. String is necessary..\n");
           return PyExc_TypeError;
        }

     } else {
        y2error ("Missing name of function.");
        //printf("Missing name of function.\n");
        return PyExc_SyntaxError;

     }
     //printf("namespace: %s\n", ns_name);
     //printf("function: %s\n", func_name);
     // create namespace
     Y2Namespace *ns = getNs (ns_name, func_name);
     if (ns == NULL) {
        y2error ("Creating namespace fault.");
        //printf("Creating namespace fault..\n");
        return PyExc_RuntimeError;
     }
     // we want either a function or a variable
     // so find a symbol of an unspecified category
     TableEntry *sym_te = ns->table ()->find (func_name);
     if (sym_te == NULL) {
	y2error ("No such symbol %s::%s", ns_name, func_name);
        //printf("No such symbol %s::%s\n", ns_name, func_name);
	return PyExc_RuntimeError;
     }
     SymbolEntryPtr sym_entry = sym_te->sentry();
     constFunctionTypePtr fun_type = (constFunctionTypePtr)sym_entry->type();
     if (fun_type->parameterCount() >0 )
        cout << fun_type->parameters()->toString() << endl;
     Y2Function *func_call = ns->createFunctionCall (func_name, NULL);
     if (func_call == NULL) {
	y2error ("No such function %s::%s", ns_name, func_name);
        //printf("No such symbol %s::%s\n", ns_name, func_name);
        return PyExc_RuntimeError;
     }
     if (fun_type->parameterCount() > (number_args-2)) {
        y2error ("Too much arguments");
        return PyExc_SyntaxError;
     } else if (fun_type->parameterCount() < (number_args-2)){
        y2error ("Missing arguments");
        return PyExc_SyntaxError;
     }
     for (int i=2; i< number_args; i++) {
         pPythonValue = PyTuple_GetItem(args, i);
         if (pPythonValue) {
            if (!(ypython->PythonTypeToYCPSimpleType(pPythonValue,ycpArg))) {
               ycpArg = ypython->fromPythonListToYCPList (pPythonValue);
               if (ycpArg.isNull())
                  ycpArg = ypython->fromPythonDictToYCPMap (pPythonValue);
            }
	    if (fun_type->parameterType(i-2)->matchvalue(ycpArg) != 0) {
               y2error ("Wrong type of argumment %d",i-2);
               return PyExc_TypeError;

	    }
            bool ok = func_call->appendParameter (ycpArg);
	    if (!ok) {
               y2error ("Problem with adding arguments of function %s", func_name);
               //printf("Problem with adding arguments of function %s\n", func_name);
               return PyExc_RuntimeError;
	    }
         } else {
            y2error ("Missing argument of function.");
            //printf("Missing argument of function.\n");
            return  PyExc_SyntaxError;

         }
     }
     bool ok = func_call->finishParameters ();
     if (!ok) {
	y2error ("Problem with finishing arguments for adding arguments of function %s", func_name);
        //printf("Problem with finishing arguments for adding arguments of function %s\n", func_name);
        return  PyExc_RuntimeError;
     }
     ycpRetValue = func_call->evaluateCall ();
     delete func_call;
     if (ycpRetValue.isNull ()) {
	y2error ("Return value of function %s is NULL", func_name);
        //printf("Return value of function %s is NULL\n", func_name);
        return PyExc_RuntimeError;
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
     return PyExc_SyntaxError;
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
