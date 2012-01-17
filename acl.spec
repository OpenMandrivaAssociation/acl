%define	libname_orig	lib%{name}
%define lib_major	1
%define libname	  %mklibname %{name} %{lib_major}
%define develname %mklibname -d %{name}

Summary:	Command for manipulating access control lists
Name:		acl
Version:	2.2.51
Release:	2
License:	GPLv2+ and LGPLv2
Group:		System/Kernel and hardware
URL:		http://savannah.nongnu.org/projects/acl
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz.sig
BuildRequires:	attr-devel
BuildRequires:	autoconf automake libtool

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n	%{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
This package contains the %{libname_orig} dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n	%{develname}
Summary:	Access control list static libraries and headers
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Provides:	libacl-devel = %{version}-%{release}
Obsoletes:	%mklibname -d acl 0
Obsoletes:	%mklibname -d acl 1

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
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make

%install
rm -rf %{buildroot}

make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

# cleanup
rm -rf %{buildroot}%{_docdir}/acl
rm -f %{buildroot}/%{_lib}/*.*a
rm -f %{buildroot}%{_libdir}/*.*a

%find_lang %{name}

%files -f %{name}.lang
%doc doc/CHANGES.gz doc/COPYING README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%doc doc/COPYING
/%{_lib}/*.so.*

%files -n %{develname}
%doc doc/extensions.txt doc/COPYING doc/libacl.txt
/%{_lib}/*.so
%{_libdir}/*.so
%{_mandir}/man3/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
