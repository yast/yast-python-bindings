if HAVE_PY3
PYTHON_VERS = python3
else
PYTHON_VERS = python
endif

BUILT_SOURCES = ycp.py yast.py

_ycp.so:
	if [ -h $(builddir)/_ycp.so ] ; then rm $(builddir)/_ycp.so ; fi; $(LN_S) .libs/libpy2lang_$(PYTHON_VERS).so $(builddir)/_ycp.so

ycp.py yast-core_wrap.cxx: yast-core.i ytypes.i ycp.i $(libpy2UI) YCPMap.h y2log.i
	$(SWIG) $(AX_SWIG_PYTHON_OPT) -c++ -I/usr/include/YaST2 -o $@ $<

yast.py: yast.py.in _ycp.so
	sed -e 's;[@]DATADIR[@];$(datadir);g' < $(srcdir)/yast.py.in > $(srcdir)/yast.py

# Remove non-standard syntax unrecognized by swig from YCPMap.h
YCPMap.h:
	sed 's/__attribute__ ((deprecated)) //g' /usr/include/YaST2/ycp/YCPMap.h > $(builddir)/YCPMap.h

python_PYTHON = ycp.py yast.py yast_help.py ycpbuiltins.py YCPDeclarations.py

noinst_HEADERS = PythonLogger.h y2log.h yast.h YPythonCode.h ytypes.h Y2CCPythonClient.h Y2PythonClientComponent.h YCPDeclarations.h YPython.h Y2CCPython.h Y2PythonComponent.h YCPMap.h YPythonNamespace.h

install-exec-hook:
	(mkdir -p $(DESTDIR)/${pyexecdir}; cd $(DESTDIR)/${pyexecdir}; $(LN_S) ${py2langdir}/libpy2lang_$(PYTHON_VERS).so _ycp.so || echo)
uninstall-hook:
	(cd $(DESTDIR)/${pyexecdir}; rm -f _ycp.so || echo)

SOURCES = Y2PythonComponent.cc Y2CCPython.cc YPython.cc YPythonNamespace.cc YCPDeclarations.cc yast.cpp yast-core_wrap.cxx Y2PythonClientComponent.cc Y2CCPythonClient.cc YPythonCode.cc PythonLogger.cc
LIBADD = -L$(py2langdir) -lpy2UI -lpy2wfm
LDFLAGS = -module ${PYTHON_LDFLAGS} -Wl,-rpath=$(pyexecdir)
CPPFLAGS = -std=c++11 -I/usr/include/YaST2 ${PYTHON_CPPFLAGS} -Wno-terminate -Wno-format-security -Wno-format-nonliteral

if HAVE_PY3
py2lang_LTLIBRARIES = libpy2lang_python3.la
libpy2lang_python3_la_SOURCES = $(SOURCES)
libpy2lang_python3_la_LIBADD = $(LIBADD)
libpy2lang_python3_la_LDFLAGS = $(LDFLAGS)
libpy2lang_python3_la_CPPFLAGS = $(CPPFLAGS)
else
py2lang_LTLIBRARIES = libpy2lang_python.la
libpy2lang_python_la_SOURCES = $(SOURCES)
libpy2lang_python_la_LIBADD = $(LIBADD)
libpy2lang_python_la_LDFLAGS = $(LDFLAGS)
libpy2lang_python_la_CPPFLAGS = $(CPPFLAGS)
endif

AM_CXXFLAGS = -DY2LOG=\"Python\"

CLEANFILES = ycp.py yast.py yast-core_wrap.cxx YCPMap.h _ycp.so
