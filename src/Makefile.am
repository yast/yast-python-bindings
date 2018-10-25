BUILT_SOURCES = ycp.py yast.py
ycp.py yast-core_wrap.cxx: yast-core.i ytypes.i ycp.i $(libpy2UI) YCPMap.h y2log.i
	$(SWIG) $(AX_SWIG_PYTHON_OPT) -c++ -I/usr/include/YaST2 -o $@ $<

yast.py: yast.py.in
	sed -e 's;[@]DATADIR[@];$(datadir);g' < $(srcdir)/yast.py.in > $(srcdir)/yast.py

# Remove non-standard syntax unrecognized by swig from YCPMap.h
YCPMap.h:
	sed 's/__attribute__ ((deprecated)) //g' /usr/include/YaST2/ycp/YCPMap.h > YCPMap.h

python_PYTHON = ycp.py yast.py ycpbuiltins.py YCPDeclarations.py

noinst_HEADERS = PythonLogger.h y2log.h yast.h YPythonCode.h ytypes.h Y2CCPythonClient.h Y2PythonClientComponent.h YCPDeclarations.h YPython.h Y2CCPython.h Y2PythonComponent.h YCPMap.h YPythonNamespace.h

install-exec-hook:
	(cd ${pyexecdir}; $(LN_S) ${py2langdir}/libpy2lang_python.so _ycp.so || echo)
uninstall-hook:
	(cd ${pyexecdir}; rm -f _ycp.so || echo)

py2lang_LTLIBRARIES = libpy2lang_python.la

libpy2lang_python_la_SOURCES = Y2PythonComponent.cc Y2CCPython.cc YPython.cc YPythonNamespace.cc YCPDeclarations.cc yast.cpp yast-core_wrap.cxx Y2PythonClientComponent.cc Y2CCPythonClient.cc YPythonCode.cc PythonLogger.cc

libpy2lang_python_la_LIBADD = -L$(py2langdir) -lpy2UI -lpy2wfm

libpy2lang_python_la_LDFLAGS = -module ${PYTHON_LDFLAGS} -Wl,-rpath=$(pyexecdir)

libpy2lang_python_la_CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate -Wno-format-security -Wno-format-nonliteral

AM_CXXFLAGS = -DY2LOG=\"Python\"

CLEANFILES = ycp.py yast.py yast-core_wrap.cxx YCPMap.h
