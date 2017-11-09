#include <Python.h>
#include <ycp/YCode.h>
#include <ycp/YCPCode.h>
#include <ycp/y2log.h>
#include "ytypes.h"

class YPythonCode : public YCode
{

public:
     YPythonCode (PyObject *pFunc);

     YCode::ykind kind() const;

     std::ostream & toStream (std::ostream & str) const;

     std::ostream & toXml (std::ostream & str, int indent ) const;
     /**
     * Evaluates the code.
     */
    YCPValue evaluate (bool cse = false);

private:
     ykind m_kind;
     PyObject *_pFunc;

};

