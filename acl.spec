%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%bcond_without	uclibc

Summary:	Command for manipulating access control lists
Name:		acl
Version:	2.2.51
Release:	9
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://savannah.nongnu.org/projects/acl
Source0:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.src.tar.gz.sig
Patch0:		acl-2.2.51-l10n-ru.patch
Patch1:		acl-aarch64.patch
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
%patch0 -p1
%patch1 -p1

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
%uclibc_configure \
		OPTIMIZER="%{uclibc_cflags}" \
		--prefix=%{uclibc_root} \
		--exec-prefix=%{uclibc_root} \
		--libdir=%{uclibc_root}/%{_lib} \
		--enable-shared \
		--enable-gettext \
		--with-sysroot=%{uclibc_root}
popd
%endif

pushd .system
CFLAGS="%{optflags}" \
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make
popd

%install
%if %{with uclibc}
make -C .uclibc install-lib DIST_ROOT=%{buildroot}
make -C .uclibc install-dev DIST_ROOT=%{buildroot}
install -d %{buildroot}%{uclibc_root}%{_libdir}
rm %{buildroot}%{uclibc_root}/%{_lib}/libacl.{a,la,so}
ln -sr %{buildroot}/%{uclibc_root}/%{_lib}/libacl.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libacl.so
mv %{buildroot}%{_libdir}/libacl.a %{buildroot}%{uclibc_root}%{_libdir}/libacl.a
chmod 755 %{buildroot}/%{uclibc_root}/%{_lib}/libacl.so.%{major}*
%endif

make -C .system install DIST_ROOT=%{buildroot}/
make -C .system install-dev DIST_ROOT=%{buildroot}/
make -C .system install-lib DIST_ROOT=%{buildroot}/


# Remove unpackaged symlinks
# TOdO: finish up spec-helper script ot automatically deal with
rm %{buildroot}%{_libdir}/libacl.so
ln -sr %{buildroot}/%{_lib}/libacl.so.%{major}.* %{buildroot}%{_libdir}/libacl.so
chmod 755 %{buildroot}/%{_lib}/libacl.so.%{major}*

rm -rf %{buildroot}%{_docdir}/acl
rm %{buildroot}{/%{_lib},%{_libdir}}/*.a

%find_lang %{name}

%files -f %{name}.lang
%doc .uclibc/doc/CHANGES.gz README
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
%{uclibc_root}%{_libdir}/libacl.a
%{uclibc_root}%{_libdir}/libacl.so
%endif
%{_mandir}/man3/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.51-9
- rebuild on ABF

* Sun Oct 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.51-5
+ Revision: 820211
- drop libintl patch, uclibc libc.so linker script now automatically pulls it in
- fix uClibc build
- fix symlinkng of libacl.so
- do uClibc build
- fix file permissions
- cleanup a bit
- be more explicit about license and ditch shipping COPYING

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.51-3
+ Revision: 782648
- drop excessive provides

* Tue Jan 17 2012 Oden Eriksson <oeriksson@mandriva.com> 2.2.51-2
+ Revision: 761886
- various fixes

* Thu May 12 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.51-1
+ Revision: 673746
- 2.2.51

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.49-5
+ Revision: 662749
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.49-4mdv2011.0
+ Revision: 603167
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - ship acl(5) man page in main package, instead of the devel package

* Mon Dec 28 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.49-2mdv2010.1
+ Revision: 483156
- P0: security fix for CVE-2009-4411

* Sun Dec 27 2009 Frederik Himpe <fhimpe@mandriva.org> 2.2.49-1mdv2010.1
+ Revision: 482850
- update to new version 2.2.49

* Tue Aug 25 2009 Frederik Himpe <fhimpe@mandriva.org> 2.2.48-1mdv2010.0
+ Revision: 421234
- Update to new version 2.48
- Remove symlinks patch integrated upstream

  + Eugeni Dodonov <eugeni@mandriva.com>
    - Added patch0 to prevent following symlinks when not needed (#43741).

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.47-6mdv2010.0
+ Revision: 413019
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.47-5mdv2009.1
+ Revision: 316459
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.2.47-4mdv2009.0
+ Revision: 220325
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 11 2008 Frederik Himpe <fhimpe@mandriva.org> 2.2.47-3mdv2008.1
+ Revision: 165429
- New upstream version

* Mon Jan 28 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.45-3mdv2008.1
+ Revision: 159089
- make it provide libacl-devel again

* Sun Jan 27 2008 Funda Wang <fwang@mandriva.org> 2.2.45-2mdv2008.1
+ Revision: 158752
- fix upgrading by obsoleting correct pacakage

* Sun Jan 27 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.45-1mdv2008.1
+ Revision: 158654
- new devel policy
- update to new version 2.2.45

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.2.44-3mdv2008.1
+ Revision: 148405
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild with correct optflags

  + Christiaan Welvaart <spturtle@mandriva.org>
    - 2.2.44


* Sat Mar 03 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 2.2.39-2mdv2007.0
+ Revision: 131825
- Rebuilt.
- Import acl

* Sun Jul 09 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.2.39-1mdv2007.0
- 2.2.39.

* Fri May 05 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.2.34-1mdk
- 2.2.34

* Wed Jan 11 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.2.31-3mdk
- add BuildRequires: libtool

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.2.31-2mdk
- Rebuild

* Wed Aug 03 2005 Giuseppe Ghibò <ghibo@mandriva.com> 2.2.31-1mdk
- 2.2.31.

* Wed Jul 21 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.23-2mdk
- if we list the libattr libtool file in our libtool file, at least
  ensure the location is right

* Fri Apr 30 2004 Juan Quintela <quintela@mandrakesoft.com> 2.2.23-1mdk
- 2.2.23.

