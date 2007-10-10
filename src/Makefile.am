#
# Makefile.am for python-bindings/src
#

AM_CXXFLAGS = -DY2LOG=\"Python\" -DMODULEDIR=\"$(moduledir)\"

MY_PYTHON_VENDORARCH = $(subst /usr,$(prefix),$(PYTHON_VENDORARCH))
#pythonpydir = $(MY_PYTHON_VENDORARCH)/YaST
pythonpydir = $(MY_PYTHON_VENDORARCH)/site-packages
pythonsodir = $(MY_PYTHON_VENDORARCH)/site-packages


pythonpy_DATA = YCPDeclarations.py

# plugin, libtool forces 'lib' prefix
plugin_LTLIBRARIES = libpy2lang_python.la
noinst_LTLIBRARIES = libYCPTypes.la liby2lang_python.la libYCPDeclarations.la
pythonso_LTLIBRARIES = libYCP.la

libYCPTypes_la_SOURCES = YCPTypes.cc YCPTypes.h \
                         YCPTypes/YCPTypesInternal.cc YCPTypes/YCPTypesInternal.h \
                         YCPTypes/Path.cc \
                         YCPTypes/Symbol.cc \
                         YCPTypes/Term.cc

libYCPDeclarations_la_SOURCES = YCPDeclarations.cc YCPDeclarations.h

# binary part of the python module
libYCP_la_SOURCES =				\
	$(liby2lang_python_la_SOURCES)		\
	YCP.cc					\
	PythonLogger.cc PythonLogger.h


install-data-hook:
	$(LN_S) -f libYCP.so $(DESTDIR)$(pythonsodir)/ycp.so


# are there enough yast libraries?
# check with y2base, integrate them like y2pm does
# Originally, of the py2* there was only py2plugin here
# with the assumption that it would bring in the other plugins.
# But it does not work.
libYCP_la_LDFLAGS = $(PYTHON_LDFLAGS)		\
		-L$(libdir) -L$(plugindir)	\
		-Xlinker --whole-archive	\
		-lpy2scr			\
		-lpy2wfm			\
		-lscr -lpy2UI			\
		-lycp -ly2			\
		-Xlinker --no-whole-archive	\
		-ly2util			\
		-version-info 2:0

libYCP_la_LIBADD = libYCPTypes.la #libYCPDeclarations.la


libpy2lang_python_la_LDFLAGS = -version-info 2:0

liby2lang_python_la_LDFLAGS = -version-info 2:0


# the yast libraries are apparently necessary when we're loaded by python.
libpy2lang_python_la_LDFLAGS = $(PYTHON_LDFLAGS)	\
		-L$(libdir) -L$(plugindir)	\
		-lycp -ly2 -ly2util

libpy2lang_python_la_LIBADD = libYCPTypes.la libYCPDeclarations.la


liby2lang_python_la_LIBADD  = $(PYTHON_LDFLAGS)


liby2lang_python_la_SOURCES =				\
	YPython.cc YPython.h

# Auto-generated stub for dynamic loading of python modules.
# And also register the interface to the YCP module
## which is linked in already and won't be in the standard python location.
#
# This results in a linker warning:
# *** Warning: Linking the shared library libpy2lang_python.la against the
# *** static library /usr/lib/python5/.../DynaLoader.a is not portable!
#
# According to mls@suse.de this warning can safely be disregarded:
# The SuSE DynaLoader is compiled with -fPIC for just this situation.
#
# -- sh@suse.de 2003-07-24
#pythonxsi.c:
#	python -MExtUtils::Embed -e xsinit -- -o pythonxsi.c -std
# See "man pythonembed"


# the plugin adds the liby2 component interface

libpy2lang_python_la_SOURCES =				\
	$(liby2lang_python_la_SOURCES)			\
	Y2CCPython.cc Y2CCPython.h			\
	YPythonNamespace.cc YPythonNamespace.h		\
	Y2PythonComponent.cc Y2PythonComponent.h	

# CLEANFILES = \
#	pythonxsi.c

INCLUDES = -I$(srcdir)/include -I$(includedir) ${ZYPP_CFLAGS} -I/usr/include/python

# generated from YaPI.pm.in by configure
# nodist_module_DATA = YaPI.pm

#EXTRA_DIST = $(pythonpy_DATA) $(module_DATA)
EXTRA_DIST = $(pythonpy_DATA)

