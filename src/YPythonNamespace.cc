/**
 * 
 *
 * This is the path from YCP to Python.
 */

#include <Python.h>
#include "YPythonNamespace.h"

#define y2log_component "Y2PythonNamespace"
#include <ycp/y2log.h>
#include <ycp/pathsearch.h>

#include <ycp/YCPElement.h>
#include <ycp/Type.h>
#include <ycp/YCPVoid.h>

#include <YPython.h>
#include <stdio.h>



/**
 * The definition of a function that is implemented in Perl
 */
class Y2PythonFunctionCall : public Y2Function
{
    //! module name
    string m_module_name;
    //! function name, excluding module name
    string m_local_name;
    //! function type
    constFunctionTypePtr m_type;
    //! data prepared for the inner call
    YCPList m_call;

public:
    Y2PythonFunctionCall (const string &module_name,
			 const string &local_name,
                         constFunctionTypePtr function_type
	) :
	m_module_name (module_name),
	m_local_name (local_name),
	m_type (function_type)
	{
	    // placeholder, formerly function name
	    m_call->add (YCPVoid ());
	}

    //! if true, the perl function is passed the module name
    virtual bool isMethod () = 0;

    //! called by YEFunction::evaluate
    virtual YCPValue evaluateCall ()
    {
	return YPython::yPython()->callInner (
	    m_module_name, m_local_name, isMethod (),
	    m_call);
    }
    
       /**
     * Attaches a parameter to a given position to the call.
     * @return false if there was a type mismatch
     */
    virtual bool attachParameter (const YCPValue& arg, const int position)
    {
	m_call->set (position+1, arg);
	return true;
    }

    /**
     * What type is expected for the next appendParameter (val) ?
     * (Used when calling from Perl, to be able to convert from the
     * simple type system of Perl to the elaborate type system of YCP)
     * @return Type::Any if number of parameters exceeded
     */
    virtual constTypePtr wantedParameterType () const
    {
	// -1 for the function name
	int params_so_far = m_call->size ()-1;
	return m_type->parameterType (params_so_far);
    }
     
    /**
     * Appends a parameter to the call.
     * @return false if there was a type mismatch
     */
    virtual bool appendParameter (const YCPValue& arg)
    {
	m_call->add (arg);
	return true;
    }

    /**
     * Signal that we're done adding parameters.
     * @return false if there was a parameter missing
     */
    virtual bool finishParameters () { return true; }


    virtual bool reset ()
    {
	m_call = YCPList ();
	// placeholder, formerly function name
	m_call->add (YCPVoid ());
	return true;
    }

    /**
     * Something for remote namespaces
     */
    virtual string name () const { return m_local_name; }
};

class Y2PythonSubCall : public Y2PythonFunctionCall {
public:
    Y2PythonSubCall (const string &module_name,
		     const string &local_name,
		     constFunctionTypePtr function_type 
	) :
	Y2PythonFunctionCall (module_name, local_name, function_type)
	{}
    virtual bool isMethod () { return false; }
};

class Y2PythonMethodCall : public Y2PythonFunctionCall {
public:
    Y2PythonMethodCall (const string &module_name,
			const string &local_name,
                        constFunctionTypePtr function_type
	) :
	Y2PythonFunctionCall (module_name, local_name, function_type)
	{}
    virtual bool isMethod () { return true; }
};



YPythonNamespace::YPythonNamespace (string name)
    : m_name (name),
      m_all_methods (true)
{

  const char * c_name = m_name.c_str ();

  //Objects for Python API
  PyObject* pMain;        //main module
  PyObject* pMainDict;    //global dictionary of variables from __main__
  PyObject* pFunc;        //pionter for function from python
  PyObject* item;         //item from list of globals symbols from __main__
  PyObject* num_args;     //number of function argumets in python
  PyObject * fun_names;   //list of globals symbols from __main__
  string module;
  FILE*     file;

  int num_fun_names = 0;
  int count = 0;  
  long num = 0;
  // args = inspect.getargs(name_function.func_code)
  char * command = new char[201]; //command for obtain arguments of function

  //add __main__ module
  pMain = PyImport_AddModule("__main__");
  PyRun_SimpleString("import __main__");
  //PyRun_SimpleString("import ycp");
  //import inspect module - necessary for number of function arguments
  PyRun_SimpleString("import inspect");
  //obtain main dictionary of globals variables
  pMainDict = PyModule_GetDict(pMain);

  //Open file and his running in main module

  module = YCPPathSearch::find (YCPPathSearch::Module, name + ".py");
  
  
  file = fopen(module.c_str(), "r");
  if (file) {
     y2milestone("module name %s", module.c_str());
     PyRun_SimpleFile(file, module.c_str());
  }
  //symbols from __main__
  PyRun_SimpleString("fun_names = dir(__main__)");
  fun_names = PyDict_GetItemString(pMainDict, "fun_names");
  //number of symbols
  num_fun_names = PyList_Size(fun_names);
  
  //check each symbol and try to find function names
  for (int i = 0; i < num_fun_names; i++) {
    //y2milestone ("YPythonNamespace iteration %d from all %d", i, num_fun_names);
    item = PyList_GetItem(fun_names, i); /* Can’t fail */
    //y2milestone ("YPythonNamespace item: %s", PyString_AsString(item));
    if (!PyString_Check(item)) continue; /* Skip non-string */
    //y2milestone ("item: %s", PyString_AsString(item));
    pFunc = PyDict_GetItemString(pMainDict,PyString_AsString(item));    
    //check if symbol is callable    

    if (PyFunction_Check(pFunc)) {
       FunctionTypePtr  sym_tp = new FunctionType (Type::Any);
       
       //build command for obtaining number of function
       strcpy(command, "");
       strcpy(command, "args = inspect.getargs(");
       command = strcat(command, PyString_AsString(item));
       command = strcat(command, ".func_code)");
       //run the command: args = inspect.getargs(name_function.func_code)
       PyRun_SimpleString(command);
       PyRun_SimpleString("num_args = len(args[0])");
       num_args = PyDict_GetItemString(pMainDict, "num_args");
       num = PyInt_AsLong(num_args);
       //y2milestone ("Number of parameters: %d", num);
       //add types and number of arguments into SymbolEntry table
       for (long j = 0; j < num; j++) {
           sym_tp->concat(Type::Any);    
       }
       //y2milestone ("Callable function %s", PyString_AsString(item));
       // symbol entry for the function
       SymbolEntry *fun_se = new SymbolEntry (
		this,
		count++,	         // position. arbitrary numbering. must stay consistent when?
		PyString_AsString(item), // passed to Ustring, no need to strdup
		SymbolEntry::c_function, 
		sym_tp);
       fun_se->setGlobal (true);

       // enter it to the symbol table
       enterSymbol (fun_se, 0);
    }
  } // end of for (int i = 0; i < num_fun_names; i++) 

  delete []command;
  //Py_CLEAR(fun_names);


  
  y2milestone ("YPythonNamespace finish");
  
}

YPythonNamespace::~YPythonNamespace ()
{
}

const string YPythonNamespace::filename () const
{
    // TODO improve
    return ".../" + m_name;
}

// this is for error reporting only?
string YPythonNamespace::toString () const
{
    y2error ("TODO");
    return "{\n"
	"/* this namespace is provided in Python */\n"
	"}\n";
}

// called when running and the import statement is encountered
// does initialization of variables
// constructor is handled separately after this
YCPValue YPythonNamespace::evaluate (bool cse)
{
    // so we don't need to do anything
    y2debug ("Doing nothing");
    return YCPNull ();
}

// It seems that this is the standard implementation. why would we
// ever want it to be different?
Y2Function* YPythonNamespace::createFunctionCall (const string name, constFunctionTypePtr required_type)
{
    y2debug ("Python creating function call for %s", name.c_str ());
    TableEntry *func_te = table ()->find (name.c_str (), SymbolEntry::c_function);
    if (func_te)
    {
	constTypePtr t = required_type ? required_type : (constFunctionTypePtr)func_te->sentry()->type ();
	if (m_all_methods)
	{
	    return new Y2PythonMethodCall (m_name, name, t);
	}
	else
	{
	    return new Y2PythonSubCall (m_name, name, t);
	}
    }
    y2error ("No such function %s", name.c_str ());
    return NULL;
}
