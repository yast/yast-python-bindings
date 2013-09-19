#
# spec file for package yast2-python-bindings
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           yast2-python-bindings
Version:        3.1.0
Release:        0

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2

Group:	        System/YaST
License:        GPL-2.0
BuildRequires:	curl-devel gcc-c++ yast2-core-devel python-devel yast2-ycp-ui-bindings-devel libtool
BuildRequires:  yast2-devtools >= 3.0.6

# YCPValue::valuetype_str()
Requires:	yast2-core       >= 2.16.37
BuildRequires:	yast2-core-devel >= 2.16.37
BuildRequires:  yast2-ycp-ui-bindings-devel >= 2.16.37
Requires:       yast2-ycp-ui-bindings       >= 2.16.37
Requires:	python
%if 0%{?suse_version} < 1220
BuildRequires:  libxcrypt-devel
%endif

Summary:	Python bindings for the YaST platform.

%description
The bindings allow YaST modules to be written using the Python language
and also Python scripts can use YaST agents, APIs and modules.

%prep
%setup -n %{name}-%{version}

%build
%yast_build

%install
%yast_install

rm $RPM_BUILD_ROOT/%{yast_plugindir}/libpy2lang_python.la
rm $RPM_BUILD_ROOT/%{python_sitearch}/libYCP.la


%files
%defattr (-, root, root)
%{yast_plugindir}/libpy2lang_python.so.*
%{yast_plugindir}/libpy2lang_python.so

# libYCP goes elsewhere
# %dir %{_libdir}/python
%{python_sitearch}/*
%doc %{yast_docdir}
