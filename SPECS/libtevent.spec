%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

%global talloc_version 2.3.4

Name: libtevent
Version: 0.14.1
Release: 3%{?dist}
Summary: The tevent library
License: LGPL-3.0-or-later
URL: http://tevent.samba.org/
Source0: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
Source1: http://samba.org/ftp/tevent/tevent-%{version}.tar.asc
# gpg2 --no-default-keyring --keyring ./tevent.keyring --recv-keys 9147A339719518EE9011BCB54793916113084025
Source2: tevent.keyring

# Patches

BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: libcmocka-devel >= 1.1.3
BuildRequires: libtalloc-devel >= %{talloc_version}
BuildRequires: libxslt
BuildRequires: make
%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-talloc-devel >= %{talloc_version}
#endif with python
%endif

Provides: bundled(libreplace)
Obsoletes: python2-tevent < 0.10.0-1

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Summary: Developer tools for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}
Requires: libtalloc-devel%{?_isa} >= %{talloc_version}

%description devel
Header files needed to develop programs that link against the Tevent library.


%if %{with python3}
%package -n python3-tevent
Summary: Python 3 bindings for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}

%{?python_provide:%python_provide python3-tevent}

%description -n python3-tevent
Python 3 bindings for libtevent
#endif with python
%endif

%prep
zcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
%autosetup -n tevent-%{version} -p1

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

%make_build

doxygen doxy.config

%check
%make_build check

%install
%make_install

# Install API docs
rm -f doc/man/man3/todo*
install -d -m0755 %{buildroot}%{_mandir}
cp -a doc/man/man3 %{buildroot}%{_mandir}

%files
%{_libdir}/libtevent.so.*

%files devel
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%{_mandir}/man3/tevent*.gz

%if %{with python3}
%files -n python3-tevent
%{python3_sitearch}/tevent.py
%{python3_sitearch}/__pycache__/tevent.*
%{python3_sitearch}/_tevent.cpython*.so
%endif

%ldconfig_scriptlets

%changelog
* Tue Jun 06 2023 Pavel Filipenský <pfilipen@redhat.com> - 0.14.1-3
- resolves: rhbz#2190425 - Rebuild to trigger distrobaker sync

* Wed May 24 2023 Pavel Filipenský <pfilipen@redhat.com> - 0.14.1-2
- resolves: rhbz#2190425 -  Add missing tests to fix osci.brew-build.tier0.functional

* Thu May 18 2023 Pavel Filipenský <pfilipen@redhat.com> - 0.14.1-1
- resolves: rhbz#2190425 Update to version 0.14.1

* Mon Oct 24 2022 Andreas Schneider <asn@redhat.com> - 0.13.0-1
- resolves: rhbz#2132055 - Update to version 0.13.0

* Mon May 02 2022 Pavel Filipenský <pfilipen@redhat.com> - 0.12.0-0
- resolves: rhbz#2077485 - Update to version 0.12.0

* Fri Jul 09 2021 Andreas Schneider <asn@redhat.com> - 0.11.0-0
- resolves: rhbz#1980346 - Update to version 0.11.0

* Tue Jun 2 2020 Isaac Boukris <iboukris@redhat.com> - 0.10.2-2
- Resolves: #1817563 - Upgrade tevent to 0.10.2 version for samba

* Tue Nov 26 2019 Isaac Boukris <iboukris@redhat.com> - 0.10.0-2
- Resolves: #1754421 - Upgrade tevent to 0.10.0 version for samba
- Related: #1754421 - Fix sssd tests (tevent)

* Tue Apr 30 2019 Jakub Hrozek <jhrozek@redhat.com>
- Remove the python2 subpackages on upgrade
- Resolves: #1567139 - libtevent: Drop Python 2 subpackage from RHEL 8

* Wed Apr 24 2019 Jakub Hrozek <jhrozek@redhat.com> - 0.9.39-1
- Resolves: #1684580 - Rebase libtevent to version 0.9.36 for Samba
- Resolves: #1597318 - libtevent uses Python 2 to build
- Resolves: #1567139 - libtevent: Drop Python 2 subpackage from RHEL 8

* Thu Sep 20 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.37-2
- Resolves: #1624138 - Review annocheck distro flag failures in libtevent

* Thu Jul 12 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.37-1
- New upstream release 0.9.37
- Use RHEL_ALLOW_PYTHON2_FOR_BUILD=1 for build
- Use %%{__python2}, not "python", as the Python2 interpreter

* Mon Feb 26 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 0.9.36-1
- rhbz#1548613 New upstream release 0.9.36

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.9.35-2
- Rebuilt for switch to libxcrypt

* Sat Jan 13 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 0.9.35-1
- rhbz#1534134 New upstream release 0.9.35

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.34-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Nov 30 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.9.34-3
- Cleanup spec file conditionals

* Thu Nov 30 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 0.9.34-2
- Update spec file conditionals

* Tue Nov 14 2017 Lukas Slebodnik <lslebodn@redhat.com> - 0.9.34-1
- New upstream release 0.9.34

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Lukas Slebodnik <lslebodn@redhat.com> - 0.9.33-1
- New upstream release 0.9.33

* Fri Jun 23 2017 Lukas Slebodnik <lslebodn@redhat.com> - 0.9.32-1
- New upstream release 0.9.32

* Fri Mar 10 2017 Lukas Slebodnik <lslebodn@redhat.org> - 0.9.31-4
- Fix configure detection with strict CFLAGS - rhbz#1401231
- Fix few fedora packaging violations - rhbz#1401226

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.31-2
- Rebuild for Python 3.6

* Fri Oct  7 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.31-1
- New upstream release 0.9.31

* Mon Aug 29 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.30-1
- New upstream release 0.9.30

* Thu Jul 28 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.29-1
- New upstream release 0.9.29

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.28-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 21 2016 Petr Viktorin <pviktori@redhat.com> - 0.9.28-2
- Build Python 3 package
- Resolves: rhbz#1298250 - libtevent: Provide a Python 3 subpackage

* Mon Feb 22 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.28-1
- New upstream release 0.9.28

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.26-1
- New upstream release 0.9.26

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.25-1
- New upstream release 0.9.25

* Thu Mar  5 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.24-1
- New upstream release 0.9.24

* Mon Mar  2 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.23-1
- New upstream release 0.9.23

* Thu Oct  9 2014 Jakub Hrozek <jhrozek@redhat.com> - 0.9.22-1
- New upstream release 0.9.22

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Jakub Hrozek <jhrozek@redhat.com> - 0.9.21-1
- New upstream release 0.9.21

* Sun Dec 15 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.20-1
- New upstream release 0.9.20

* Fri Aug 02 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.19-1
- New upstream release 0.9.19
- Drop upstreamed patch

* Mon Jul 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.18-3
- Make the dependency requirements arch-specific
- Remove ancient, unused patches
- Remove python variables that are not needed on modern systems

* Wed Jun 19 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.18-2
- Apply a patch from upstream to fix tevent_poll's additional_flags
  on 32bit architectures
- Resolves: rhbz#975490

* Mon Mar 18 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.18-1
- New upstream release 0.9.18

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-3
- Dropping the workaround dropped even the doxygen command itself..

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-2
- Drop the workaround for building man pages, it has already been
  included upstream

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-1
- New upstream release 0.9.17

* Fri Aug 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-3
- Own the individual manual pages, not the top-level directory

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.16-1
- New upstream release 0.9.16
- Adds tevent_*_trace_*() and tevent_context_init_ops()
- Move tevent.py to the arch-specific directory

* Fri Feb 10 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.15-1
- New upstream release 0.9.15
- Properly re-sets the nested.level flag in the ev.ctx when reinitializing
  after a fork()
- Allow tevent_signal events to be freed during their handler

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-4
- Include missing patch file

* Tue Dec 06 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-4
- Build pytevent properly

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-3
- Add patch to ignore --disable-silent-rules
- Include API documentation

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-2
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120

* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-1
- New upstream release
- Required for building more recent versions of samba4

* Tue Aug  2 2011 Simo Sorce <ssorce@redhat.com> - 0.9.13-1
- New upstream release

* Tue Mar 15 2011 Simo Sorce <ssorce@redhat.com> - 0.9.11-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-3
- Add missing Buildrequires for pytalloc-devel

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-2
- Let rpmbuild strip binaries, make build more verbose.
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-1
- New upstream release
- Convert to new WAF build-system

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7.1
- Bump revision to chain-build libtevent, samba4 and sssd

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7
- Drop ABI compatibility patch (no longer needed)

* Wed Sep 23 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-5
- Add patch to fix a segfault case

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-2
- Fix abi compatibility with 0.9.3

* Tue Sep 8 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-1
- First independent release for tevent 0.9.8
