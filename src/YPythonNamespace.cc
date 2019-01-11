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

#include "YCPDeclarations.h"

#include "compat.h"

#define DBG(str) \
    std::cerr << __FILE__ << ": " << __LINE__ << ": " << str << std::endl; \
    std::cerr.flush()



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

    //! if true, the python function is passed the module name
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

  //Objects for Python API
  PyObject* pMainDict;    //global dictionary of imported module
  PyObject* pFunc;        //pionter for function from python
  const char* pFunc_name;
  PyObject* item;         //item from dictionary
  PyObject * fun_names;   //list of keys from dictionary (YPython::yPython()->pMain())
  PyObject * fun_code;    //code of function

  //Declarations (using YPCDelcarations python module)
  YCPDeclarations *decl = YCPDeclarations::instance();
  //YCPDeclarations *decl = new YCPDeclarations();
  
  FunctionTypePtr sym_tp;
  std::vector<constTypePtr> list_of_types;
  int tmp;


  int num_fun_names = 0; //number of keys from dictionary
  int count = 0;         // position. arbitrary numbering
  long num = 0;          //number of function arguments

  //obtain main dictionary of globals variables
  pMainDict = PyDict_GetItemString(YPython::yPython()->pMainDicts(),name.c_str());
  if (pMainDict == NULL){
      y2error("Can't load module %s", name.c_str());
      return;
  }

  //keys from dictionary
  fun_names = PyDict_Keys(pMainDict);

  //number of symbols
  num_fun_names = PyList_Size(fun_names);
  //check each symbol and try to find function names
  for (int i = 0; i < num_fun_names; i++) {
    //y2milestone ("YPythonNamespace iteration %d from all %d", i, num_fun_names);
    item = PyList_GetItem(fun_names, i); /* Can’t fail */
    //y2milestone ("YPythonNamespace item: %s", PyString_AsString(item));
    if (!PyStr_Check(item)){
      continue;
    }
    pFunc_name = PyStr_AsString(item);
    //y2milestone ("item: %s", PyString_AsString(item));
    pFunc = PyDict_GetItemString(pMainDict, pFunc_name);
    //check if symbol is callable    

    if (PyFunction_Check(pFunc)) {
       fun_code = PyFunction_GetCode(pFunc);
       num = ((PyCodeObject *) fun_code)->co_argcount;

         
       if (decl->exists((PyFunctionObject *)pFunc) 
           && decl->numParams((PyFunctionObject *)pFunc) == num){

           sym_tp = new FunctionType(decl->returnType((PyFunctionObject *)pFunc));

           list_of_types = decl->params((PyFunctionObject *)pFunc);
           tmp = list_of_types.size();
           for (int i=0; i < tmp; i++){
               sym_tp->concat(list_of_types[i]);
           }
       }else{
           sym_tp = new FunctionType(Type::Any);
           //y2milestone ("Number of parameters: %d", num);
           //add types and number of arguments into SymbolEntry table
           for (long j = 0; j < num; j++) {
               sym_tp->concat(Type::Any);    
           }
       }
       //y2milestone ("Callable function %s", PyString_AsString(item));
       // symbol entry for the function
       SymbolEntry *fun_se = new SymbolEntry (
		this,
		count++,	         // position. arbitrary numbering. must stay consistent when?
		pFunc_name,              // passed to Ustring, no need to strdup
		SymbolEntry::c_function, 
		sym_tp);
       fun_se->setGlobal (true);

       // enter it to the symbol table
       enterSymbol (fun_se, 0);
    }
  } // end of for (int i = 0; i < num_fun_names; i++)

  y2milestone ("YPythonNamespace finish");
  
}


YPythonNamespace::YPythonNamespace (string name, PyObject* function)
      : m_name (name),
        m_all_methods (true) {


  PyObject * fun_code;    //code of function

  //Declarations (using YPCDelcarations python module)
  YCPDeclarations *decl = YCPDeclarations::instance();
  //YCPDeclarations *decl = new YCPDeclarations();
  
  FunctionTypePtr sym_tp;
  std::vector<constTypePtr> list_of_types;
  int tmp;

  int count = 0;         // position. arbitrary numbering
  long num = 0;          //number of function arguments


  fun_code = PyFunction_GetCode(function);
  num = ((PyCodeObject *) fun_code)->co_argcount;
  string fun_name = PyString_AsString(((PyCodeObject *) fun_code)->co_name);
         
  if (decl->exists((PyFunctionObject *)function) 
      && decl->numParams((PyFunctionObject *)function) == num){

     sym_tp = new FunctionType(decl->returnType((PyFunctionObject *)function));

     list_of_types = decl->params((PyFunctionObject *)function);
     tmp = list_of_types.size();
     for (int i=0; i < tmp; i++){
         sym_tp->concat(list_of_types[i]);
     }
  } else {
     sym_tp = new FunctionType(Type::Any);
     //y2milestone ("Number of parameters: %d", num);
     //add types and number of arguments into SymbolEntry table
     for (long j = 0; j < num; j++) {
         sym_tp->concat(Type::Any);    
     }
  }
  //y2milestone ("Callable function %s", PyString_AsString(item));
  // symbol entry for the function
  SymbolEntry *fun_se = new SymbolEntry (
	this,
	count++,	         // position. arbitrary numbering. must stay consistent when?
	fun_name.c_str(), // passed to Ustring, no need to strdup
	SymbolEntry::c_function, 
	sym_tp);
  fun_se->setGlobal (true);

  // enter it to the symbol table
  enterSymbol (fun_se, 0);


  y2milestone ("(special) YPythonNamespace finish");

}

SymbolEntry * YPythonNamespace::AddFunction (PyObject* function) {

  //Declarations (using YPCDelcarations python module)
  YCPDeclarations *decl = YCPDeclarations::instance();
  int tmp;
  std::vector<constTypePtr> list_of_types;
  FunctionTypePtr sym_tp;
  PyObject *fun_code = PyFunction_GetCode(function);
  int num = ((PyCodeObject *) fun_code)->co_argcount;
  string fun_name = PyString_AsString(((PyCodeObject *) fun_code)->co_name);
         
  if (decl->exists((PyFunctionObject *)function) 
      && decl->numParams((PyFunctionObject *)function) == num){

     sym_tp = new FunctionType(decl->returnType((PyFunctionObject *)function));

     list_of_types = decl->params((PyFunctionObject *)function);
     tmp = list_of_types.size();
     for (int i=0; i < tmp; i++){
         sym_tp->concat(list_of_types[i]);
     }
  } else {
     sym_tp = new FunctionType(Type::Any);
     //y2milestone ("Number of parameters: %d", num);
     //add types and number of arguments into SymbolEntry table
     for (long j = 0; j < num; j++) {
         sym_tp->concat(Type::Any);    
     }
  }
  // symbol entry for the function
  SymbolEntry *fun_se = new SymbolEntry (
	this,
	0,	        // position. arbitrary numbering. must stay consistent when?
	fun_name.c_str(),       // passed to Ustring, no need to strdup
	SymbolEntry::c_function, 
	sym_tp);

  fun_se->setGlobal (true);

  enterSymbol (fun_se, 0);

  return fun_se;
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
    //TableEntry *func_te = table ()->find (name.c_str (), SymbolEntry::c_function);
    TableEntry *func_te = table ()->find (name.c_str ());

    if (func_te)
    {
        //cout << "namespace: " << m_name << " function: " << name << endl;
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
    
    //cout << "namespace: " << m_name << " function: " << name << endl;
    y2error ("No such function %s", name.c_str ());
    return NULL;
}
