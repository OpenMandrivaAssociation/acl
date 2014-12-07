%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%bcond_without	uclibc

Summary:	Command for manipulating access control lists
Name:		acl
Version:	2.2.52
Release:	9
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://savannah.nongnu.org/projects/acl
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz.sig
Patch0:		acl-2.2.51-l10n-ru.patch
BuildRequires:	attr-devel
BuildRequires:	autoconf automake libtool
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif

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

%package -n	uclibc-%{libname}
Summary:	Main library for libacl (uClibc linked)
Group:		System/Libraries
License:	LGPLv2

%description -n	uclibc-%{libname}
This package contains the libacl dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n	%{devname}
Summary:	Access control list static libraries and headers
Group:		Development/C
License:	LGPLv2
Requires:	%{libname} >= %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}-%{release}
%endif
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
%apply_patches

find -type f|xargs chmod o+r

%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

mkdir .system
pushd .system
cp -a ../* .
popd

%build
%if %{with uclibc}
pushd .uclibc
# upstream has a weird idea about what libexecdir is
%uclibc_configure \
		OPTIMIZER="%{uclibc_cflags}" \
		--prefix=%{uclibc_root} \
		--exec-prefix=%{uclibc_root} \
		--libdir=%{uclibc_root}/%{_lib} \
		--libexecdir=%{uclibc_root}/%{_lib} \
		--enable-shared \
		--enable-gettext \
		--with-sysroot=%{uclibc_root}
popd
%endif

pushd .system
# upstream has a weird idea about what libexecdir is
CFLAGS="%{optflags}" \
%configure --libdir=/%{_lib} --libexecdir=/%{_lib} --sbindir=/bin
%make
popd

%install
%if %{with uclibc}
make -C .uclibc install-lib DIST_ROOT=%{buildroot}
make -C .uclibc install-dev DIST_ROOT=%{buildroot}
install -d %{buildroot}%{uclibc_root}%{_libdir}
rm  %{buildroot}%{uclibc_root}/%{_lib}/libacl.{la,so}
ln -sr %{buildroot}/%{uclibc_root}/%{_lib}/libacl.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libacl.so
chmod 755 %{buildroot}/%{uclibc_root}/%{_lib}/libacl.so.%{major}*
%endif

make -C .system install DIST_ROOT=%{buildroot}/
make -C .system install-dev DIST_ROOT=%{buildroot}/
make -C .system install-lib DIST_ROOT=%{buildroot}/


# Remove unpackaged symlinks
# TODO: finish up spec-helper script to automatically deal with this
mkdir -p %{buildroot}%{_libdir}
ln -sr %{buildroot}/%{_lib}/libacl.so.%{major}.* %{buildroot}%{_libdir}/libacl.so
chmod 755 %{buildroot}/%{_lib}/libacl.so.%{major}*

rm -rf %{buildroot}%{_docdir}/acl %{buildroot}/%{_lib}/*.a

%find_lang %{name}

%files -f %{name}.lang
%if %{with uclibc}
%doc .uclibc/doc/CHANGES.gz README
%endif
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
/%{_lib}/libacl.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libacl.so.%{major}*
%endif

%files -n %{devname}
%doc doc/extensions.txt doc/libacl.txt
/%{_lib}/libacl.so
%{_libdir}/libacl.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libacl.so
%endif
%{_mandir}/man3/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
