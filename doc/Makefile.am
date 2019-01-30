#
# Makefile.am for python-bindings/doc
#

txtdir = $(docdir)

if HAVE_PY3
PYDOC = pydoc3
else
PYDOC = pydoc
endif

yast.html ycpbuiltins.html YCPDeclarations.html:
	HTMLFILE=$@; PYFILE=$${HTMLFILE/.html/.py}; PYTHONPATH=$(top_srcdir)/src:$(top_builddir)/src:$$PYTHONPATH $(PYDOC) -w $(top_srcdir)/src/$$PYFILE

txt_DATA = yast.html ycpbuiltins.html YCPDeclarations.html

EXTRA_DIST = $(txt_DATA)
CLEANFILES = $(txt_DATA)
