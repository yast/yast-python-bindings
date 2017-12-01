#
# spec file for package yast2-python-bindings
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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
Version:        4.0.0
Release:        0

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  libyui-devel
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  yast2-core-devel
BuildRequires:  yast2-ycp-ui-bindings
BuildRequires:  yast2-ycp-ui-bindings-devel

Requires:       python3
Requires:       yast2-core
Requires:       yast2-ycp-ui-bindings

Summary:        Python bindings for the YaST platform
License:        GPL-2.0
Group:          System/YaST

%description
The bindings allow YaST modules to be written using the Python language
and also Python scripts can use YaST agents, APIs and modules.

%prep
%setup -n %{name}-%{version}

%build
%yast_build

%install
%yast_install

rm %{buildroot}/%{python_sitelib}/*.pyc
rm %{buildroot}/%{python_sitelib}/*.pyo
rm %{buildroot}/%{python_sitearch}/*.la
rm %{buildroot}/%{yast_plugindir}/libpy2lang_python.la

%files
%defattr (-, root, root)
%doc %{yast_docdir}
%{python_sitelib}/*.py
%{python_sitearch}/_ycp.*
%{yast_plugindir}/libpy2lang_python.so.*
%{yast_plugindir}/libpy2lang_python.so

%changelog
