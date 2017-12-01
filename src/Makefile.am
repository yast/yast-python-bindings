BUILT_SOURCES = ycp.py
ycp.py yast-core_wrap.cxx: yast-core.i ytypes.i ycp.i $(libpy2UI) YCPMap.h
	$(SWIG) $(AX_SWIG_PYTHON_OPT) -py3 -c++ -I/usr/include/YaST2 -o $@ $<

# Remove non-standard syntax unrecognized by swig from YCPMap.h
YCPMap.h:
	sed 's/__attribute__ ((deprecated)) //g' /usr/include/YaST2/ycp/YCPMap.h > YCPMap.h

python_PYTHON = ycp.py yast.py ycpbuiltins.py

pyexec_LTLIBRARIES = _ycp.la

_ycp_la_SOURCES = yast-core_wrap.cxx yast.cpp yast-core.i ytypes.i ycp.i YPythonCode.cc PythonLogger.cc

_ycp_la_LDFLAGS = -module ${PYTHON_LDFLAGS} -Wl,-rpath=$(py2langdir)

_ycp_la_LIBADD = -L$(py2langdir) -lpy2UI

_ycp_la_CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate

py2lang_LTLIBRARIES = libpy2lang_python.la

libpy2lang_python_la_SOURCES = Y2PythonClientComponent.cc Y2CCPythonClient.cc

libpy2lang_python_la_LDFLAGS = -lpython3 ${PYTHON_LDFLAGS} -Wl,-rpath=$(pyexecdir)

libpy2lang_python_la_CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate

AM_CXXFLAGS = -DY2LOG=\"Python\"

CLEANFILES = ycp.py yast-core_wrap.cxx YCPMap.h
