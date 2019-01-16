// -*- c++ -*-
#include <Python.h>
#include <y2/Y2Namespace.h>
#include <y2/Y2Function.h>
#include <ycp/YStatement.h>

/**
 * YaST interface to a Python module
 */
class YPythonNamespace : public Y2Namespace
{
private:
    string m_name;		//! this namespace's name, eg. XML::Writer
public:

    /**
     * Construct an interface. The module must be already loaded
     * @param name eg "XML::Writer"
     */
    YPythonNamespace (string name);

    /**
     * Construct an interface. The module must be already loaded
     * special contruct for calling python function such as reference
     * @param name eg "XML::Writer"
     * @param function function defined in python
     */
    YPythonNamespace (string name, PyObject* function);

    /**
     * Add new function into namespace
     * @param Y2Namespace pointer to namespace for adding function
     * @param PyObject pointer to function
     * @return SymbolEntry pointer to added symbol entry else NULL (if failed)
     */
    SymbolEntry * AddFunction (PyObject* function);

    virtual ~YPythonNamespace ();

    //! what namespace do we implement
    virtual const string name () const { return m_name; }
    //! used for error reporting
    virtual const string filename () const;

    //! unparse. useful  only for YCP namespaces??
    virtual string toString () const;
    //! called when evaluating the import statement
    // constructor is handled separately
    virtual YCPValue evaluate (bool cse = false);

    virtual Y2Function* createFunctionCall (const string name, constFunctionTypePtr requiredType);
};
