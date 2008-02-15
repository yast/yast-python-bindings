/**
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
#include <ycp/Parser.h>
#include <ycp/YCPMap.h>
#include <ycp/YCPList.h>
#include <ycp/YCPPath.h>
#include <ycp/YCPTerm.h>
#include <ycp/YCPString.h>
#include <ycp/YCPVoid.h>
#include <ycp/SymbolTable.h>

#include "YPython.h"
#include "PythonLogger.h"


#include "YCPTypes.h"
#include "YCPDeclarations.h"

/**
 * Store pointer to ycp module itself.
 */


static PyObject *Self;

YCPList * ycpListFunctions;

YCPList * ycpTermList;

PyObject * CallYCPFunction (PyObject *args);

PyObject * ImportYCPNameSpace (PyObject *args);

PyObject * InitUI (PyObject *args);

PyObject * _SCR_Run (PyObject *args);

PyObject * InitTerm(PyObject *args);

PyObject * ChangeWidgetName(PyObject *args);

void PyY2logger(PyObject *args);

void init_wfm ();

bool RegSCR();

void InitYCPTermList();

static bool HandleSymbolTable (const SymbolEntry & se) 
{
	if (se.isFunction ()) {

		ycpListFunctions->add(YCPString(se.name()));
		/*
		cout << se.name() << endl;
		constFunctionTypePtr type = (constFunctionTypePtr)se.type();
		if (type->parameters())
			cout << type->parameters()->toString() << endl;
     		*/

	}
	return true;
}



/**
 * init namespace
 * @param char * name of module
 * @param char * name of function
 * @return namespace of YCP
 */

static Y2Namespace * getNs (const char * ns_name, const char * func_name) 
{
	Import import(ns_name);	// has a static cache
	Y2Namespace *ns = import.nameSpace();
	if (ns == NULL) {
		y2error ("... for a Python call of %s", func_name);
	} else {
		ns->initialize ();
	}
	return ns;
}


static PyObject * ycp_handle_function(PyObject *self, PyObject *args) 
{
	return CallYCPFunction (args);
}


static PyObject * ycp_import_namespace(PyObject *self, PyObject *args) 
{
	return ImportYCPNameSpace (args);
}

static PyObject * ycp_init_ui(PyObject *self, PyObject *args) 
{
	return InitUI (args);
}


static PyObject * ycp_scr_handle(PyObject *self, PyObject *args) 
{
	return _SCR_Run(args);
}


static PyObject * ycp_y2logger (PyObject *self, PyObject *args) 
{
	PyY2logger(args);
	return Py_None;
}


static PyObject * ycp_init_term(PyObject *self, PyObject *args) 
{
	return InitTerm(args);
}

static PyObject * ycp_change_widget_name(PyObject *self, PyObject *args)
{
	return ChangeWidgetName(args);
}


/**
 * This is needed for importing new module from ycp.
 */
static PyMethodDef new_module_methods[] = 
{
	{"__run", ycp_handle_function, METH_VARARGS, "Calling YCP from Python"},
	{NULL, NULL, 0, NULL}
};


/**
 * This is necessary for regulat (python style) calling SCR from python
 */
static PyMethodDef scr_methods[] = 
{
	{"__scr_run", ycp_scr_handle, METH_VARARGS, "Calling SCR from python"},
	{NULL, NULL, 0, NULL}
};


/**
 * This is default specific "modul" for creating term namespace
 */
static PyMethodDef term_methods[] = 
{
	{NULL, NULL, 0, NULL}
};

static PyMethodDef YCPMethods[] = 
{
	{"run",  ycp_handle_function, METH_VARARGS, "Calling YCP from Python"},
	{"import_module",  ycp_import_namespace, METH_VARARGS, "Import namespace from YCP module"},
	{"init_ui",  ycp_init_ui, METH_VARARGS, "Initialization of UI for YCP"},
	{"y2logger", ycp_y2logger, METH_VARARGS, "Logging error, debug messages and milestones in python"},
	{"widget_names", ycp_init_term, METH_VARARGS, "Init known terms from YCP e.g. VBox, CheckBox into main dictionary"},
	{"__change_widget_name", ycp_change_widget_name, METH_VARARGS, "Function for changing widget name"},
	{NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initycp(void) 
{	

	char func_y2internal[] =
		"def y2internal(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(5, file, line, func, message)";

	char func_y2security[] =
		"def y2security(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(4, file, line, func, message)";

	char func_y2error[] =
		"def y2error(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(3, file, line, func, message)";

	char func_y2warning[] =
		"def y2warning(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(2, file, line, func, message)";

	char func_y2milestone[] =
		"def y2milestone(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(1, file, line, func, message)";

	char func_y2debug[] =
		"def y2debug(message):\n\t\
		file, line, func, txt = traceback.extract_stack(None, 2)[0]\n\t\
		y2logger(0, file, line, func, message)";

	string textdomain =
		"def textdomain(domain):\n\t\
		gettext.bindtextdomain(domain, '";

	textdomain +=LOCALEDIR;
	textdomain +="')\n\t\
		gettext.textdomain(domain)";

	// added space - important for checking texdomain during make package
	string _fun = 
		"def _" "(str): \n\t\
		return gettext.gettext(str)";

	PyRun_SimpleString("import sys, traceback");
	PyRun_SimpleString(_fun.c_str());
	Self = Py_InitModule("ycp", YCPMethods);

	initYCPTypes(Self);

	PyObject * traceback = PyImport_AddModule("traceback");
	PyModule_AddObject(Self,"traceback",traceback);

	PyRun_SimpleString("import gettext");
	PyObject * gettext = PyImport_AddModule("gettext");

	PyModule_AddObject(Self,"gettext",gettext);
	init_wfm ();
  
	//cout <<"local dir" <<LOCALEDIR << endl;

	PyObject *dict = PyModule_GetDict(Self);
	PyObject *code;

	code = PyRun_String(func_y2internal, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(func_y2security, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(func_y2error, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(func_y2warning, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(func_y2milestone, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(func_y2debug, Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(textdomain.c_str(), Py_single_input, dict, dict);
	Py_XDECREF(code);

	code = PyRun_String(_fun.c_str(), Py_single_input, dict, dict);
	Py_XDECREF(code);

	RegSCR();

	// Initialization of YCPDeclarations module
	YCPDeclarations::instance()->init();

    //InitTerm(NULL);
}


void InitYCPTermList()
{
	// adding terms   
	ycpTermList = new YCPList();

	ycpTermList->add(YCPString("BarGraph"));
	ycpTermList->add(YCPString("Bottom"));
	ycpTermList->add(YCPString("CheckBox"));
	ycpTermList->add(YCPString("CheckBoxFrame"));
	ycpTermList->add(YCPString("ComboBox"));
	ycpTermList->add(YCPString("ColoredLabel"));
	ycpTermList->add(YCPString("Date"));
	ycpTermList->add(YCPString("DownloadProgress"));
	ycpTermList->add(YCPString("DumbTab"));
	ycpTermList->add(YCPString("Empty"));
	ycpTermList->add(YCPString("Frame"));
	ycpTermList->add(YCPString("HBox"));
	ycpTermList->add(YCPString("HasSpecialWidget"));
	ycpTermList->add(YCPString("HCenter"));
	ycpTermList->add(YCPString("Heading"));
	ycpTermList->add(YCPString("HSpacing"));
	ycpTermList->add(YCPString("HSquash"));
	ycpTermList->add(YCPString("HStretch"));
	ycpTermList->add(YCPString("HVCenter"));
	ycpTermList->add(YCPString("HVMultiProgressMeter"));
	ycpTermList->add(YCPString("HVSquash"));
	ycpTermList->add(YCPString("HVStretch"));
	ycpTermList->add(YCPString("HWeight"));
	ycpTermList->add(YCPString("IconButton"));
	ycpTermList->add(YCPString("Image"));
	ycpTermList->add(YCPString("IntField"));
	ycpTermList->add(YCPString("Label"));
	ycpTermList->add(YCPString("Left"));
	ycpTermList->add(YCPString("LogView"));
	ycpTermList->add(YCPString("MarginBox"));
	ycpTermList->add(YCPString("MenuButton"));
	ycpTermList->add(YCPString("MinHeight"));
	ycpTermList->add(YCPString("MinSize"));
	ycpTermList->add(YCPString("MinWidth"));
	ycpTermList->add(YCPString("MultiLineEdit"));
	ycpTermList->add(YCPString("MultiSelectionBox"));
	ycpTermList->add(YCPString("PackageSelector"));
	ycpTermList->add(YCPString("PartitionSplitter"));
	ycpTermList->add(YCPString("Password"));
	ycpTermList->add(YCPString("PatternSelector"));
	ycpTermList->add(YCPString("PkgSpecial"));
	ycpTermList->add(YCPString("ProgressBar"));
	ycpTermList->add(YCPString("PushButton"));
	ycpTermList->add(YCPString("RadioButton"));
	ycpTermList->add(YCPString("RadioButtonGroup"));
	ycpTermList->add(YCPString("ReplacePoint"));
	ycpTermList->add(YCPString("Right"));
	ycpTermList->add(YCPString("RichText"));
	ycpTermList->add(YCPString("SelectionBox"));
	ycpTermList->add(YCPString("SimplePatchSelector"));
	ycpTermList->add(YCPString("Slider"));
	ycpTermList->add(YCPString("Table"));
	ycpTermList->add(YCPString("TextEntry"));
	ycpTermList->add(YCPString("Time"));
	ycpTermList->add(YCPString("Top"));
	ycpTermList->add(YCPString("Tree"));
	ycpTermList->add(YCPString("VBox"));
	ycpTermList->add(YCPString("VCente"));
	ycpTermList->add(YCPString("VMultiProgressMeter"));
	ycpTermList->add(YCPString("VSpacing"));
	ycpTermList->add(YCPString("VSquash"));
	ycpTermList->add(YCPString("VStretch"));
	ycpTermList->add(YCPString("VWeight"));
	ycpTermList->add(YCPString("Wizard"));

}



PyObject * InitTerm(PyObject *args)
{
	int number_args = PyTuple_Size(args);
    // adding false into pResult
	PyObject *pResult = PyBool_FromLong(0);

	PyObject *dict = PyModule_GetDict(Self);
	string func_def;
	string term;
	PyObject *code;

	// initialize list of terms
	InitYCPTermList();

	if (number_args != 0)
	{
		
		PyObject *pPythonValue = PyTuple_GetItem(args, 0);
        string widget_ns = "term";

		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
			{
				widget_ns = PyString_AsString(pPythonValue); 

			} else {
				y2error ("Wrong type of function argument. String is necessary.");
				return pResult;
			}
		} else {
			y2error ("Transfering arguments for InitTerm() failed.");
			return pResult;			
		}

		// Init new module with name NameSpace and method __run (see new_module_methods)
		PyObject *new_module = Py_InitModule(widget_ns.c_str(), term_methods);
		if (new_module == NULL) return false;

    	initYCPTermType(new_module);

		
		// Add new initialized module into ycp dictionary
		PyDict_SetItemString(dict, widget_ns.c_str(), new_module);

		PyObject *new_module_dict = PyModule_GetDict(new_module);
		if (new_module_dict == NULL) return false;

		for (int i=0; i<ycpTermList->size(); i++) 
		{
			term = ycpTermList->value(i)->asString()->value(); 
			func_def = "def " + term + "(*args):";
			func_def += "\n\treturn Term(\"" + term + "\", *args)";

			// Register function into dictionary of new module. Returns new reference - must be decremented
			code = PyRun_String(func_def.c_str(), Py_single_input, new_module_dict, new_module_dict);
			Py_XDECREF(code);
		}

	} else {
		for (int i=0; i<ycpTermList->size(); i++) 
		{
			term = ycpTermList->value(i)->asString()->value(); 
			func_def = "def " + term + "(*args):";
			func_def += "\n\treturn Term(\"" + term + "\", *args)";

			// Register function into dictionary of new module. Returns new reference - must be decremented
			code = PyRun_String(func_def.c_str(), Py_single_input, dict, dict);
			Py_XDECREF(code);
		}
	} // end if (number_args != 0)


	delete ycpTermList;
	return Py_True;
}

/**
 * Returns Py_True if name of widget was successful changed
 * @param string actual name of widget
 * @param string real name of widget from YCP (it is not neccessary 
 *  if actual name is same than real name)
 * @param string new name of widget
 * @return pointer to PyObject (Py_True) on success or Py_False
 */
PyObject * ChangeWidgetName(PyObject *args)
{
	int number_args = PyTuple_Size(args);
	// adding false into pResult
	PyObject *pResult = PyBool_FromLong(0);
	string actual_name;
	string new_name;
	string real_name;
	PyObject *pPythonValue;
	PyObject *dict = PyModule_GetDict(Self);
	string command;
	PyObject *code;
	int in_dict =0;
	PyObject * main_module = PyImport_AddModule("__main__");
	PyObject * main_dict = PyModule_GetDict(main_module);

	switch(number_args)
	{
	case 2:
		// adding 1st argument (actual name)
		pPythonValue = PyTuple_GetItem(args, 0);
		if (PyString_Check(pPythonValue)) 
		{
			actual_name = PyString_AsString(pPythonValue); 

		} else {
			y2error ("Wrong type of the 1st argument. String is necessary.");
			return pResult;
		}

 		in_dict = PyDict_Contains(dict, pPythonValue);

		//in_dict = PyDict_Contains(dict, PyString_FromString("__dict__"));

		if (in_dict == 0) 
		{
			y2error ("Main dictionary doesn't include widget %s", actual_name.c_str());
			return pResult;
		} else if (in_dict == -1)
		{
			y2error ("Checking of main dictionary for widget %s failed.", actual_name.c_str());
			return pResult;
			
		}

		y2debug("Widget %s was found in main dictionary", actual_name.c_str());

		// initialize list of terms
		InitYCPTermList();

		if (!ycpTermList->contains(YCPString(actual_name.c_str())))
		{
			delete ycpTermList;
			y2error ("Checking of list widget names for widget %s failed.", actual_name.c_str());
			return pResult;
		}

		delete ycpTermList;
		
		// adding 2nd argument (new name)
		pPythonValue = PyTuple_GetItem(args, 1);
		if (PyString_Check(pPythonValue)) 
		{
			new_name = PyString_AsString(pPythonValue); 

		} else {
			y2error ("Wrong type of the 2nd argument. String is necessary.");
			return pResult;
		}
		
		y2milestone("Renaming widget name %s", actual_name.c_str());
		// deleting widget name
		command = "del ycp.__dict__['" + actual_name + "']";
		y2milestone("Command for deleting widget: %s",command.c_str());
			
		code = PyRun_String(command.c_str(), Py_single_input, main_dict, dict);
		Py_XDECREF(code);			

		// adding new name
		command = "def " + new_name + "(*args):";
		command += "\n\treturn Term('" + actual_name + "', *args)";
		y2milestone("Command for adding widget: %s",command.c_str());

		code = PyRun_String(command.c_str(), Py_single_input, dict, dict);
		Py_XDECREF(code);
		pResult = PyBool_FromLong(1);
		
		return pResult;

	case 3:

		// adding 1st argument (actual name)
		pPythonValue = PyTuple_GetItem(args, 0);
		if (PyString_Check(pPythonValue)) 
		{
			actual_name = PyString_AsString(pPythonValue); 

		} else {
			y2error ("Wrong type of the 1st argument. String is necessary.");
			return pResult;
		}

 		in_dict = PyDict_Contains(dict, pPythonValue);

		if (in_dict == 0) 
		{
			y2error ("Main dictionary doesn't include widget %s", actual_name.c_str());
			return pResult;
		} else if (in_dict == -1)
		{
			y2error ("Checking of main dictionary for widget %s failed.", actual_name.c_str());
			return pResult;
			
		}

		y2debug("Widget %s was found in main dictionary", actual_name.c_str());

		// adding 2nd argument (original widget name)
		pPythonValue = PyTuple_GetItem(args, 1);
		if (PyString_Check(pPythonValue)) 
		{
			real_name = PyString_AsString(pPythonValue); 

		} else {
			y2error ("Wrong type of the 2nd argument. String is necessary.");
			return pResult;
		}

		// initialize list of terms
		InitYCPTermList();

		if (!ycpTermList->contains(YCPString(real_name.c_str())))
		{
			delete ycpTermList;
			y2error ("Checking of list widget names for widget %s failed.", real_name.c_str());
			return pResult;
		}

		delete ycpTermList;

		// adding 3rd argument (new name)
		pPythonValue = PyTuple_GetItem(args, 2);
		if (PyString_Check(pPythonValue)) 
		{
			new_name = PyString_AsString(pPythonValue); 

		} else {
			y2error ("Wrong type of the 3rd argument. String is necessary.");
			return pResult;
		}
		
		y2milestone("Renaming widget name %s", actual_name.c_str());
		// deleting widget name
		command = "del ycp.__dict__['" + actual_name + "']";
		y2milestone("Command for deleting widget: %s",command.c_str());
			
		code = PyRun_String(command.c_str(), Py_single_input, main_dict, dict);
		Py_XDECREF(code);			

		// adding new name
		command = "def " + new_name + "(*args):";
		command += "\n\treturn Term('" + real_name + "', *args)";
		y2milestone("Command for adding widget: %s",command.c_str());

		code = PyRun_String(command.c_str(), Py_single_input, dict, dict);
		Py_XDECREF(code);
		pResult = PyBool_FromLong(1);
		
		return pResult;

	case 0:
	case 1:
	default:
		y2error ("Wrong number of arguments for ChangeWidgetName()");
		return pResult;

	}


}

/**
 * Returns true if NameSpace is registered (is key) in dictionary dict.
 * Otherwise returns false;
 */
bool isRegistered(PyObject *dict, const char *NameSpace)
{
	bool ret = false;
	PyObject *name_space = PyString_FromString(NameSpace);

	if (PyDict_Contains(dict, name_space) == 1)
		ret = true;

	Py_XDECREF(name_space);

	return ret;
}

bool RegFunctions(char *NameSpace, YCPList list_functions) 
{

	// Dictionary of ycp module
	PyObject *ycp_dict = PyModule_GetDict(Self);
	if (ycp_dict == NULL) return false;

	// If already registered return true
    if (isRegistered(ycp_dict, NameSpace)) return true;


	// Init new module with name NameSpace and method __run (see new_module_methods)
	PyObject *new_module = Py_InitModule(NameSpace, new_module_methods);
	if (new_module == NULL) return false;

	// Add new initialized module into ycp dictionary (can be accessed via ycp.NameSpace)
	PyDict_SetItemString(ycp_dict, NameSpace, new_module);

	// Dictionary of new_module - there will be registered all functions
	PyObject *new_module_dict = PyModule_GetDict(new_module);
	if (new_module_dict == NULL) return false;

	PyObject *code;
	string func_def;
	string function;
	for (int i=0; i<list_functions.size();i++) {
		function = list_functions->value(i)->asString()->value(); 
		func_def = "def " + function + "(*args):";
		func_def += "\n\treturn __run(\"" + string(NameSpace) + "\", \"" + function + "\", *args)";

		// Register function into dictionary of new module. Returns new reference - must be decremented
		code = PyRun_String(func_def.c_str(), Py_single_input, new_module_dict, new_module_dict);
		Py_XDECREF(code);
	}
	return true;

}


bool RegSCR() 
{
    string func_read =
		"def Read(*args):\n\t\
		return __scr_run(0, *args)";

	string func_write =
		"def Write(*args):\n\t\
		return __scr_run(1, *args)";

	string func_dir =
		"def Dir(*args):\n\t\
		return __scr_run(2, *args)";

	string func_execute =
		"def Execute(*args):\n\t\
		return __scr_run(3, *args)";


	// Dictionary of ycp module
	PyObject *ycp_dict = PyModule_GetDict(Self);
	if (ycp_dict == NULL) return false;

	// Init new module with name NameSpace and method __run (see new_module_methods)
	PyObject *new_module = Py_InitModule("SCR", scr_methods);
	if (new_module == NULL) return false;

	// Add new initialized module into ycp dictionary (can be accessed via ycp.NameSpace)
	PyDict_SetItemString(ycp_dict, "SCR", new_module);

	// Dictionary of new_module - there will be registered all functions
	PyObject *new_module_dict = PyModule_GetDict(new_module);
	if (new_module_dict == NULL) return false;

	PyObject *code;
  
	// Register function into dictionary of new module. Returns new reference - must be decremented
	code = PyRun_String(func_read.c_str(), Py_single_input, new_module_dict, new_module_dict);
	Py_XDECREF(code);

	code = PyRun_String(func_write.c_str(), Py_single_input, new_module_dict, new_module_dict);
	Py_XDECREF(code);

	code = PyRun_String(func_dir.c_str(), Py_single_input, new_module_dict, new_module_dict);
	Py_XDECREF(code);

	code = PyRun_String(func_execute.c_str(), Py_single_input, new_module_dict, new_module_dict);
	Py_XDECREF(code);

	return true;

}

Y2Component *owned_wfmc = 0;

void init_wfm () 
{

	//printf("Calling init_wfm ()\n");
	if (Y2WFMComponent::instance () == 0) 
	{
		owned_wfmc = Y2ComponentBroker::createClient ("wfm");
		if (owned_wfmc == 0) {
			y2error ("Cannot create WFM component");
		}
	}
}

Y2Component *owned_uic = 0;

PyObject * InitUI (PyObject *args) 
{

	PyObject * pPythonValue;
	PyObject* pResult = PyBool_FromLong(0);
	int number_args = PyTuple_Size(args);
	string ui_name = "ncurses";

	if (number_args == 1) 
	{
		pPythonValue = PyTuple_GetItem(args, 0);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
			{
				ui_name = PyString_AsString(pPythonValue); 

			} else {
				y2error ("Wrong type of function argument. String is necessary.");
				return pResult;
			}
		}
	} else if (number_args != 0) 
	{
		y2error ("Zero or one arguments required (ui name, default %s", ui_name.c_str());
		return pResult;
	}

	Y2Component *c = YUIComponent::uiComponent ();

	if (c == 0) 
	{
		y2debug ("UI component not created yet, creating %s", ui_name.c_str());
		c = Y2ComponentBroker::createServer (ui_name.c_str());

		if (c == 0) 
		{
			y2error ("Cannot create component %s", ui_name.c_str());
			return pResult;
		}

		if (YUIComponent::uiComponent () == 0) 
		{
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


PyObject * ImportYCPNameSpace (PyObject *args) 
{
	PyObject* pResult = PyBool_FromLong(0);
	PyObject * pPythonValue;
	int number_args = PyTuple_Size(args);
	char * ns_name = new char[101];
  
	if (number_args == 1) 
	{
		pPythonValue = PyTuple_GetItem(args, 0);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
			{
				ns_name = strcpy(ns_name, PyString_AsString(pPythonValue)); 

			} else {
				y2error ("Wrong type of name for namespace. String is necessary.");         
				return pResult;
			}
			Import import(ns_name);	// has a static cache
			Y2Namespace *ns = import.nameSpace();
			if (ns == NULL) 
				return pResult;
			else
				ns->initialize ();
			ycpListFunctions = new YCPList();
			ns->table()->forEach (&HandleSymbolTable);	
			RegFunctions(ns_name, *ycpListFunctions);

			delete [] ns_name;
			delete ycpListFunctions;

			pResult = PyBool_FromLong(1);
		}

	} else {
		PyErr_SetString(PyExc_SyntaxError,"Wrong number of arguments");
		pResult = PyBool_FromLong(0);
	}

	return pResult;
}

PyObject * _SCR_Run (PyObject *args) 
{
	// access directly the statically declared builtins
  	extern StaticDeclaration static_declarations;
	int number_args = PyTuple_Size(args);
	YCPValue ycpArg = YCPNull ();
	YCPValue ycpRetValue = YCPNull ();
	YCPValue ycpPath = YCPNull ();
	PyObject * pPythonValue;
	PyObject * pReturnValue;

	//-1 - error
	// 0 - SCR::Read
	// 1 - SCR::Write
	// 2 - SCR::Dir
	// 3 - SCR::Execute
	int type_scr = -1;
    
	YPython *ypython = YPython::yPython ();
	char *temp; 
	temp = (char *) malloc(20);


	if (number_args>0) 
	{		
		pPythonValue = PyTuple_GetItem(args, 0);
		if (PyInt_Check(pPythonValue))
			type_scr = PyInt_AsLong(pPythonValue);
		else 
		{
			y2error("The first argument must be integer...");
			return Py_None;
		}

	} else {
		y2error("At least 2 arguments are necessary...");
		return Py_None;
	}

	switch (type_scr) 
	{
	case 0:
		temp = strcpy(temp, "SCR::Read");
		break;

	case 1:
		temp = strcpy(temp, "SCR::Write");
		break;

	case 2:
		temp = strcpy(temp, "SCR::Dir");
		break;

	case 3:
		temp = strcpy(temp, "SCR::Execute");
		break;

	default:
		temp = strcpy(temp, "NONE");
	}

	declaration_t *bi_dt = static_declarations.findDeclaration(temp);

	if (bi_dt == NULL) 
	{
		y2error ("No such builtin '%s'", temp);
		return PyExc_RuntimeError;
	}

	YEBuiltin *bi_call = new YEBuiltin (bi_dt);
	if (number_args < 1) 
	{
		y2error ("Missing argument of function.");
		return  PyExc_SyntaxError;
	}

	for (int i=1; i< number_args; i++) 
	{
		pPythonValue = PyTuple_GetItem(args, i);
		if (pPythonValue) 
		{
			if (pPythonValue != Py_None)
				ycpArg = ypython->PythonTypeToYCPType(pPythonValue);
			else 
				ycpArg = YCPVoid();
	
			if (ycpArg.isNull ()) 
			{
				// an error has already been reported, now refine it.
				// Can't know parameter name?
				y2error ("... when passing parameter %d to builtin %s",i, temp);
				return  PyExc_RuntimeError;
			}


			// Such YConsts without a specific type produce invalid
			// bytecode. (Which is OK here)
			// The actual parameter's YCode becomes owned by the function call?
			YConst *param_c = new YConst (YCode::ycConstant, ycpArg);

			// for attaching the parameter, must get the real type so that it matches
			constTypePtr act_param_tp = Type::vt2type (ycpArg->valuetype());
            
            

			// Attach the parameter
			// Returns NULL if OK, Type::Error if excessive argument
			// Other errors (bad code, bad type) shouldn't happen
			constTypePtr err_tp = bi_call->attachParameter (param_c, act_param_tp);

			if (err_tp != NULL) 
			{
				if (err_tp->isError ()) 
				{
					// where we were called from.
					y2error ("Excessive parameter to builtin %s",temp);
				} else {
					y2internal ("attachParameter returned %s",
					err_tp->toString ().c_str ());
				}
				return PyExc_RuntimeError;
			}


		} else {
			y2error ("Missing argument of function.");
			return  PyExc_SyntaxError;
		}
	}
  
	// now must check if we got fewer parameters than needed
	// or there was another error while resolving the overload
  	constTypePtr err_tp = bi_call->finalize (PythonLogger::instance ());
	if (err_tp != NULL) 
	{
		// apparently the error was already reported?
		y2error ("Error type %s when finalizing builtin %s",err_tp->toString ().c_str (), temp);
		return PyExc_RuntimeError;
	}
 
	// go call it now!
	y2debug ("Python is calling builtin %s", temp);

	ycpRetValue = YCPNull();
	ycpRetValue = bi_call->evaluate (false /* no const subexpr elim */);

	delete bi_call;
	free(temp);

	pReturnValue = ypython->YCPTypeToPythonType(ycpRetValue);

	if (pReturnValue)
		return pReturnValue;
	else 
		return Py_None;
}



PyObject * CallYCPFunction (PyObject *args) 
{
	int number_args = PyTuple_Size(args);
	char * ns_name = new char[101];
	char * func_name = new char[101];
	PyObject * pPythonValue;
	PyObject * pReturnValue;
	YCPValue ycpArg = YCPNull ();
	YCPValue ycpRetValue = YCPNull ();
  	YPython *ypython = YPython::yPython ();

	if (number_args >= 2) 
	{
		// obtain name of namespace (first argument)
		pPythonValue = PyTuple_GetItem(args, 0);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
				ns_name = strcpy(ns_name, PyString_AsString(pPythonValue)); 
			else 
			{
				y2error ("Wrong type of name for namespace. String is necessary.");
				return PyExc_TypeError;
			}
		} else {
			y2error ("Missing name of namespace.");
			return PyExc_SyntaxError;
		}

		// obtain name of function (second argumet)
		pPythonValue = PyTuple_GetItem(args, 1);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
			{
				func_name = strcpy(func_name, PyString_AsString(pPythonValue)); 
				//y2milestone("Call_YCPFunction: NS: %s FUN: %s",ns_name, func_name);
			} else {
				y2error ("Wrong type of name for function. String is necessary.");
				return PyExc_TypeError;
			}

		} else {
			y2error ("Missing name of function.");
			return PyExc_SyntaxError;
     	}

		// create namespace
		Y2Namespace *ns = getNs (ns_name, func_name);

		if (ns == NULL) 
		{
			y2error ("Creating namespace fault.");
			return PyExc_RuntimeError;
		}
		// we want either a function or a variable
		// so find a symbol of an unspecified category
		TableEntry *sym_te = ns->table ()->find (func_name);

		if (sym_te == NULL) 
		{
			y2error ("No such symbol %s::%s", ns_name, func_name);
			return PyExc_RuntimeError;
		}
		SymbolEntryPtr sym_entry = sym_te->sentry();
		constFunctionTypePtr fun_type = (constFunctionTypePtr)sym_entry->type();
		Y2Function *func_call = ns->createFunctionCall (func_name, NULL);
     
		if (func_call == NULL) 
		{
			y2error ("No such function %s::%s", ns_name, func_name);
			return PyExc_RuntimeError;
		}     
		if (fun_type->parameterCount() > (number_args-2)) 
		{
			y2error ("Too much arguments");
			return PyExc_SyntaxError;
		} else if (fun_type->parameterCount() < (number_args-2))
		{
			y2error ("Missing arguments");
			return PyExc_SyntaxError;
		}
     
		for (int i=2; i< number_args; i++) 
		{
			pPythonValue = PyTuple_GetItem(args, i);
			if (pPythonValue) 
			{
				ycpArg = ypython->PythonTypeToYCPType(pPythonValue);
				//transform YCPNull to YCPVoid
				if (ycpArg.isNull())
					ycpArg = YCPVoid();

         		/* checking type of arguments
	    		if (fun_type->parameterType(i-2)->matchvalue(ycpArg) != 0) 
				{
               		y2error ("Wrong type of argumment %d",i-2);
					return PyExc_TypeError;
				}*/
				bool ok = func_call->appendParameter (ycpArg);
				if (!ok) 
				{
					y2error ("Problem with adding arguments of function %s", func_name);
					return PyExc_RuntimeError;
				}
			} else {
				y2error ("Missing argument of function.");
				return  PyExc_SyntaxError;
			}
		}
		bool ok = func_call->finishParameters ();
		if (!ok) 
		{
			y2error ("Problem with finishing arguments for adding arguments of function %s", func_name);
			return  PyExc_RuntimeError;
		}
     
		ycpRetValue = func_call->evaluateCall ();
		delete func_call;
		if (ycpRetValue.isNull ()) 
		{
			y2error ("Return value of function %s is NULL", func_name);
			return PyExc_RuntimeError;
		}
		delete []ns_name;
		delete []func_name;

		pReturnValue = ypython->YCPTypeToPythonType(ycpRetValue);

		Py_INCREF(pReturnValue);
		return pReturnValue;
     
	} else {
		y2error ("Number of arguments is not enough.");
		return PyExc_SyntaxError;
	}    
}

void PyY2logger(PyObject *args) 
{
  	int number_args = PyTuple_Size(args);
	PyObject * pPythonValue;
	loglevel_t level = LOG_DEBUG;
	string file;
	int line = 0;
	string function;
	string message;
	if (number_args == 5) 
	{
		// obtain name of namespace (first argument)
		pPythonValue = PyTuple_GetItem(args, 0);
		if (pPythonValue) 
		{
			if (PyInt_Check(pPythonValue)) 
				level = (loglevel_t)PyInt_AsLong(pPythonValue); 
			else
				y2error("Wrong type of argument"); 
     	}
		pPythonValue = PyTuple_GetItem(args, 1);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue))
				file = PyString_AsString(pPythonValue); 
			else
				y2error("Wrong type of argument"); 
		}

		pPythonValue = PyTuple_GetItem(args, 2);
		if (pPythonValue) 
		{
			if (PyInt_Check(pPythonValue))
				line = (int)PyInt_AsLong(pPythonValue); 
			else
				y2error("Wrong type of argument"); 
		}

		pPythonValue = PyTuple_GetItem(args, 3);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue))
				function = PyString_AsString(pPythonValue); 
			else
				y2error("Wrong type of argument"); 
		}

		pPythonValue = PyTuple_GetItem(args, 4);
		if (pPythonValue) 
		{
			if (PyString_Check(pPythonValue)) 
				message = PyString_AsString(pPythonValue); 
			else
				y2error("Wrong type of argument"); 
		}

		y2_logger_function(level, Y2LOG, file.c_str(), line, function.c_str(),"%s", message.c_str());
	} else {
		y2error("Wrong number of arguments");
	}
}




void delete_all () 
{
	if (owned_uic != 0) 
	{
		delete owned_uic;
		owned_uic = 0;
	}

	if (owned_wfmc != 0) 
	{
		delete owned_wfmc;
		owned_wfmc = 0;
	}
}


int main(int argc, char *argv[])
{
	/* Pass argv[0] to the Python interpreter */
	Py_SetProgramName(argv[0]);

	/* Initialize the Python interpreter.  Required. */
	Py_Initialize();

	/* Add a static module */
	initycp();

	delete_all ();
	Py_Finalize();
}
