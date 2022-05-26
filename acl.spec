%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Command for manipulating access control lists
Name:		acl
Version:	2.3.1
Release:	3
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://savannah.nongnu.org/projects/acl
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source2:	%{name}.rpmlintrc
Patch0:		acl-2.2.51-l10n-ru.patch
BuildRequires:	pkgconfig(libattr)
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n %{libname}
Summary:	Main library for libacl
Group:		System/Libraries
License:	LGPLv2

%description -n %{libname}
This package contains the libacl dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n %{devname}
Summary:	Access control list static libraries and headers
Group:		Development/C
License:	LGPLv2
Requires:	%{libname} >= %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d acl 0} < 2.2.52-16
Obsoletes:	%{mklibname -d acl 1} < 2.2.52-16

%description -n %{devname}
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

You should install %{devname} if you want to develop programs
which make use of ACLs.  If you install %{devname}, you will
also want to install %{libname}.

%prep
%autosetup -p1

find -type f|xargs chmod o+r

%build
%configure
%make_build

%install
%make_install

# get rid of these
rm -rf %{buildroot}%{_docdir}/acl
rm -f %{buildroot}%{_libdir}/libacl.a
rm -f %{buildroot}%{_libdir}/libacl.la
chmod 0755 %{buildroot}/%{_libdir}/libacl.so.*.*.*

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*

%files -n %{libname}
%{_libdir}/libacl.so.%{major}*

%files -n %{devname}
%doc doc/extensions.txt doc/libacl.txt
%{_libdir}/libacl.so
%doc %{_mandir}/man3/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
%{_libdir}/pkgconfig/*.pc
