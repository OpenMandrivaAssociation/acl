%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	Command for manipulating access control lists
Name:		acl
Version:	2.2.51
Release:	4
License:	GPLv2+
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
Summary:	Main library for libacl
Group:		System/Libraries
License:	LGPLv2

%description -n	%{libname}
This package contains the libacl dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n	%{devname}
Summary:	Access control list static libraries and headers
Group:		Development/C
License:	LGPLv2
Requires:	%{libname} >= %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	%mklibname -d acl 0
Obsoletes:	%mklibname -d acl 1

%description -n	%{devname}
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

You should install %{devname} if you want to develop programs
which make use of ACLs.  If you install %{devname}, you will
also want to install %{libname}.

%prep
%setup -q
find -type f|xargs chmod o+r

%build
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make

%install
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

chmod 755 %{buildroot}/%{_lib}/libacl.so.%{major}.*

# cleanup
rm -rf %{buildroot}%{_docdir}/acl
rm -f %{buildroot}%{_libdir}/*.*a
rm -f %{buildroot}/%{_lib}/*.*a

%find_lang %{name}

%files -f %{name}.lang
%doc doc/CHANGES.gz README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%attr(755,root,root) /%{_lib}/libacl.so.%{major}*

%files -n %{devname}
%doc doc/extensions.txt doc/libacl.txt
/%{_lib}/libacl.so
%{_libdir}/*.so
%{_mandir}/man3/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
