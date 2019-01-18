#include "yast.h"

bool widget_names()
{
    PyObject *global = PyEval_GetGlobals();
    PyObject *ret = PyRun_String("from yast import *", Py_file_input, global, global);
    if (!ret)
        return false;
    Py_XDECREF(ret);
    return true;
}

Y2Namespace * getNs(const char * ns_name)
{
    Import import(ns_name); // has a static cache
    Y2Namespace *ns = import.nameSpace();
    if (ns != NULL)
        ns->initialize();
    return ns;
}

void SetYCPVariable(const string & namespace_name, const string & variable_name, YCPValue value)
{
    Y2Namespace *ns = getNs(namespace_name.c_str());

    if (ns == NULL) {
        y2error ("Creating namespace fault.");
        return;
    }

    TableEntry *sym_te = ns->table ()->find (variable_name.c_str());

    if (sym_te == NULL) {
        y2error ("No such symbol %s::%s", namespace_name.c_str(), variable_name.c_str());
        return;
    }

    SymbolEntryPtr sym_entry = sym_te->sentry();
    sym_entry->setValue(value);
}

YCPValue GetYCPVariable(const string & namespace_name, const string & variable_name)
{
    Y2Namespace *ns = getNs(namespace_name.c_str());

    if (ns == NULL) {
        y2error ("Creating namespace fault.");
        return YCPNull();
    }

    TableEntry *sym_te = ns->table ()->find (variable_name.c_str());

    if (sym_te == NULL) {
        y2error ("No such symbol %s::%s", namespace_name.c_str(), variable_name.c_str());
        return YCPNull();
    }

    SymbolEntryPtr sym_entry = sym_te->sentry();
    return sym_entry->value();
}

YCPList * list_functions;
YCPList * list_variables;

/**
 * Function check SymbolEntry and add name
 * to list_functions if it is function or
 * add it to list_variables if it is variable
 * @param const SymbolEntry for analyse
 * @return bool always return true
 */
static bool HandleSymbolTable (const SymbolEntry & se)
{
    if (se.isFunction ()) {
        list_functions->add(YCPString(se.name()));
    } else if (se.isVariable ()) {
        list_variables->add(YCPString(se.name()));
    }
    return true;
}

/**
 * Function import module written in YCP.
 * It means that create module into namespace of python module ycp
 * @param PyObject *args - string - include name of module written in YCP 
 * @return PyObject * true on success
 */
PyObject* import_module(const string & ns_name)
{
    Y2Namespace *ns = getNs(ns_name.c_str());
    if (!ns) return Py_None;

    // Init new module with name NameSpace and method __run (see new_module_methods)
    PyObject *new_module = PyModule_New(ns_name.c_str());
    if (new_module == NULL) return Py_None;

    // Dictionary of new_module - there will be registered all functions
    PyObject *new_module_dict = PyModule_GetDict(new_module);
    if (new_module_dict == NULL) return Py_None;

    PyObject *code;
    auto g = PyDict_New();
    if (!g) return Py_None;
    PyDict_SetItemString(g, "__builtins__", PyEval_GetBuiltins());

    list_functions = new YCPList();
    list_variables = new YCPList();
    ns->table()->forEach(&HandleSymbolTable);

    // register functions from ycp to python module 
    for (int i = 0; i < list_functions->size(); i++) {
        string function = list_functions->value(i)->asString()->value();
        stringstream func_def;
        func_def << "def " << function << "(*args):" << endl;
        TableEntry *sym_te = ns->table()->find(function.c_str());
        if (sym_te != NULL) {
            SymbolEntryPtr sym_entry = sym_te->sentry();
            constFunctionTypePtr fun_type = (constFunctionTypePtr)sym_entry->type();

            func_def << "\t\"\"\"" << endl;
            func_def << "\t" << function << "(";
            for (int i = 0; i < fun_type->parameterCount(); i++) {
                func_def << fun_type->parameterType(i)->toString();
                if (i != fun_type->parameterCount()-1)
                    func_def << ", ";
            }
            func_def << ")" << endl;
            func_def << "\t\"\"\"" << endl;
        }
        func_def << "\tfrom ycp import CallYCPFunction" << endl;
        func_def << "\treturn CallYCPFunction(\"" + ns_name + "\", \"" + function + "\", args)" << endl;

        // Register function into dictionary of new module. Returns new reference - must be decremented
        code = PyRun_String(func_def.str().c_str(), Py_single_input, g, new_module_dict);
        Py_XDECREF(code);
    }

    // adding variables like function from ycp to module
    for (int i = 0; i < list_variables->size(); i++) {
        string function = list_variables->value(i)->asString()->value();
        stringstream func_def;
        func_def << "def " << function << "(val=None):" << endl;
        func_def << "\tfrom ycp import GetYCPVariable, SetYCPVariable" << endl;
        func_def << "\tif val:" << endl;
        func_def << "\t\tSetYCPVariable(\"" + ns_name + "\", \"" + function + "\", val)" << endl;
        func_def << "\telse:" << endl;
        func_def << "\t\treturn GetYCPVariable(\"" + ns_name + "\", \"" + function + "\")" << endl;

        // Register function into dictionary of new module. Returns new reference - must be decremented
        code = PyRun_String(func_def.str().c_str(), Py_single_input, g, new_module_dict);
        Py_XDECREF(code);
    }

    delete list_functions;
    delete list_variables;

    return new_module;
}

/**
 * Function handles calling ycp function from python
 * @param const string & namespace
 * @param const string & name of function
 * @param ... args for function
 * @return YCPValue return result of running function
 */
YCPValue CallYCPFunction(const char * namespace_name, const char * function_name, YCPList args)
{
    YCPValue ycpArg = YCPNull ();
	YCPValue ycpRetValue = YCPNull ();


    // create namespace
    Y2Namespace *ns = getNs(namespace_name);

    if (ns == NULL) {
        y2error ("Creating namespace fault.");
        return YCPNull();
    }

    TableEntry *sym_te = ns->table ()->find (function_name);

    if (sym_te == NULL) {
        y2error ("No such symbol %s::%s", namespace_name, function_name);
        return YCPNull();
    }

    SymbolEntryPtr sym_entry = sym_te->sentry();
    if (sym_entry->isVariable()) {
        y2error("Cannot execute a variable");
        return YCPNull();
    }
    constFunctionTypePtr fun_type = (constFunctionTypePtr)sym_entry->type();
    Y2Function *func_call = ns->createFunctionCall (function_name, NULL);

    if (func_call == NULL) {
        y2error ("No such function %s::%s", namespace_name, function_name);
        return YCPNull();
    }

    for (int i = 0; i < args.size(); i++) {
        ycpArg = args->value(i);

        if (fun_type->parameterType(i)->isSymbol() && ycpArg->isString()) {
            ycpArg = YCPSymbol(ycpArg->asString()->value());
        }
        if (ycpArg.isNull())
            ycpArg = YCPVoid();

        if (!func_call->appendParameter(ycpArg)) {
            y2error ("Problem with adding arguments of function %s", function_name);
            return YCPNull();
        }
    }
    if (!func_call->finishParameters()) {
        y2error ("Problem with finishing arguments for adding arguments of function %s", function_name);
        return YCPNull();
    }


    ycpRetValue = func_call->evaluateCall();
    delete func_call;
    if (ycpRetValue.isNull()) {
        y2error ("Return value of function %s is NULL", function_name);
        return YCPNull();
    }
    return ycpRetValue;
}

/**
 * General function handles running SCR command
 * @param char * - Name of SCR function to call
 * @param YCPList - arguments to the function call
 * @return YCPValue result of running SCR
 */
YCPValue _SCR_Run(char *function, YCPList args)
{
	// access directly the statically declared builtins
	extern StaticDeclaration static_declarations;
	YCPValue ycpArg = YCPNull();
	YCPValue ycpRetValue = YCPNull();
	YCPValue ycpPath = YCPNull();

	declaration_t *bi_dt = static_declarations.findDeclaration(function);

	if (bi_dt == NULL) {
		y2error("No such builtin '%s'", function);
		return YCPNull();
	}

	YEBuiltin *bi_call = new YEBuiltin(bi_dt);

	for (int i = 0; i < args.size(); i++) {
		ycpArg = args->value(i);

		// Such YConsts without a specific type produce invalid
		// bytecode. (Which is OK here)
		// The actual parameter's YCode becomes owned by the function call?
		YConst *param_c = new YConst(YCode::ycConstant, ycpArg);

		// for attaching the parameter, must get the real type so that it matches
		constTypePtr act_param_tp = Type::vt2type(ycpArg->valuetype());

		// Attach the parameter
		// Returns NULL if OK, Type::Error if excessive argument
		// Other errors (bad code, bad type) shouldn't happen
		constTypePtr err_tp = bi_call->attachParameter(param_c, act_param_tp);

		if (err_tp != NULL) {
			if (err_tp->isError()) {
				// where we were called from.
				y2error("Excessive parameter to builtin %s", function);
			} else {
				y2internal("attachParameter returned %s",
				err_tp->toString().c_str());
			}
			return YCPNull();
		}
	}

	// now must check if we got fewer parameters than needed
	// or there was another error while resolving the overload
	constTypePtr err_tp = bi_call->finalize(PythonLogger::instance());
	if (err_tp != NULL) {
		// apparently the error was already reported?
		y2error("Error type %s when finalizing builtin %s", err_tp->toString().c_str(), function);
		return YCPNull();
	}

	// go call it now!
	y2debug("Python is calling builtin %s", function);

	ycpRetValue = YCPNull();
	ycpRetValue = bi_call->evaluate(false /* no const subexpr elim */);

	delete bi_call;

	return ycpRetValue;
}

