BUILT_SOURCES = ycp.py yast.py
ycp.py yast-core_wrap.cxx: yast-core.i ytypes.i ycp.i $(libpy2UI) YCPMap.h y2log.i yast.h ytypes.h y2log.h PythonLogger.h Y2PythonClientComponent.h YPythonCode.h Y2CCPythonClient.h
	$(SWIG) $(AX_SWIG_PYTHON_OPT) -c++ -I/usr/include/YaST2 -o $@ $<

yast.py: yast.py.in
	sed -e 's;[@]DATADIR[@];$(datadir);g' < $(srcdir)/yast.py.in > $(srcdir)/yast.py

# Remove non-standard syntax unrecognized by swig from YCPMap.h
YCPMap.h:
	sed 's/__attribute__ ((deprecated)) //g' /usr/include/YaST2/ycp/YCPMap.h > YCPMap.h

python_PYTHON = ycp.py yast.py ycpbuiltins.py

pyexec_LTLIBRARIES = _ycp.la

_ycp_la_SOURCES = yast-core_wrap.cxx yast.cpp yast-core.i ytypes.i ycp.i YPythonCode.cc PythonLogger.cc y2log.i
noinst_HEADERS = yast.h ytypes.h y2log.h PythonLogger.h Y2PythonClientComponent.h YPythonCode.h Y2CCPythonClient.h

_ycp_la_LDFLAGS = -module ${PYTHON_LDFLAGS} -Wl,-rpath=$(py2langdir)

_ycp_la_LIBADD = -L$(py2langdir) -lpy2UI

_ycp_la_CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate -Wno-format-security -Wno-format-nonliteral

py2lang_LTLIBRARIES = libpy2lang_python.la

libpy2lang_python_la_SOURCES = Y2PythonClientComponent.cc Y2CCPythonClient.cc

libpy2lang_python_la_LDFLAGS = ${PYTHON_LDFLAGS} -Wl,-rpath=$(pyexecdir)

libpy2lang_python_la_CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate

AM_CXXFLAGS = -DY2LOG=\"Python\"

CLEANFILES = ycp.py yast.py yast-core_wrap.cxx YCPMap.h
