%define	name	acl
%define	version	2.2.45
%define	release	%mkrel 1

%define	libname_orig	lib%{name}
%define lib_major	1
%define libname	  %mklibname %{name} %{lib_major}
%define develname %mklibname -d %{name}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Command for manipulating access control lists
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.bz2
BuildRequires:	attr-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n	%{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
This package contains the l%{libname_orig} dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n	%{develname}
Summary:	Access control list static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	%{develname} %mklibname -d %{name} 0

%description -n	%{develname}
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

You should install %{develname} if you want to develop programs
which make use of ACLs.  If you install %{develname}, you will
also want to install %{libname}.

%prep
%setup -q

%build
aclocal && autoconf
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make

%install
rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

perl -pi -e 's,\s(/%{_lib})(.*attr\.la),%{_libdir}/$2,g' %{buildroot}/%{_libdir}/%{_lib}acl.la

rm -rf %{buildroot}%{_docdir}/acl
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING README
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc doc/COPYING
/%{_lib}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/extensions.txt doc/COPYING doc/libacl.txt
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man[235]/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h


