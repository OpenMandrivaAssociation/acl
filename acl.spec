%define	name	acl
%define	version	2.2.44
%define	release	%mkrel 2

%define	lib_name_orig	lib%{name}
%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}

Summary:	Command for manipulating access control lists
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.bz2
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Requires:	%{lib_name} = %{version}-%{release}
BuildRequires:	attr-devel
BuildRequires:	libtool

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n	%{lib_name}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the l%{lib_name_orig} dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n	%{lib_name}-devel
Summary:	Access control list static libraries and headers
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	acl-devel

%description -n	%{lib_name}-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

You should install %{lib_name}-devel if you want to develop programs
which make use of ACLs.  If you install %{lib_name}-devel, you will
also want to install %{lib_name}.

%prep
%setup -q

%build
aclocal && autoconf
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make

%install
rm -rf $RPM_BUILD_ROOT
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

perl -pi -e 's,\s(/%{_lib})(.*attr\.la),%{_libdir}/$2,g' %{buildroot}/%{_libdir}/%{_lib}acl.la

rm -rf %{buildroot}%{_docdir}/acl
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING README
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc doc/COPYING
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
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


