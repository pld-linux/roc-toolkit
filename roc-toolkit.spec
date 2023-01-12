# TODO: pulseaudio modules (require internal headers, may require update for pulseaudio>5)
#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	ROC: real-time audio streaming over the network
Summary(pl.UTF-8):	ROC: strumienie audio po sieci w czasie rzeczywistym
Name:		roc-toolkit
Version:	0.2.1
Release:	1
License:	MPL v2.0
Group:		Libraries
#Source0Download: https://github.com/roc-streaming/roc-toolkit/releases
Source0:	https://github.com/roc-streaming/roc-toolkit/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	645ef0eaf17e7fdad360730e498014e5
URL:		https://github.com/roc-streaming/roc-toolkit
BuildRequires:	alsa-lib-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gengetopt
BuildRequires:	libunwind-devel
BuildRequires:	libuv-devel
BuildRequires:	openfec-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
%{?with_apidocs:BuildRequires:	python3-breathe}
BuildRequires:	ragel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	scons
BuildRequires:	sox-devel >= 14.4.0
BuildRequires:	speexdsp-devel
%{?with_apidocs:BuildRequires:	sphinx-pdg}
Requires:	sox >= 14.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ROC toolkit consists of:
- a C library;
- a set of command-line tools;
- a set of PulseAudio modules.

Key features:
- real-time streaming with guaranteed latency;
- restoring lost packets using Forward Erasure Correction codes;
- converting between the sender and receiver clock domains;
- CD-quality audio;
- multiple profiles for different CPU and latency requirements;
- portability;
- relying on open, standard protocols.

%description -l pl.UTF-8
Narzędzia ROC składają się z:
- biblioteki C
- zestawu narzędzi linii poleceń
- zestawu modułów PulseAudio

Główne możliwości:
- strumienie w czasie rzeczywistym z gwarantowanym opóźnieniem
- odtwarzanie zgubionych pakietów przy użyciu kodów korekcyjnych
- konwersja między czasem u nadawcy i odbierającego
- jakość dźwięku CD
- wiele profili dla różnych wymagań CPU i opóźnień
- przenośność
- wykorzystywanie otwartych, standardowych protokołów

%package devel
Summary:	Header files for ROC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ROC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libunwind-devel
Requires:	libuv-devel
Requires:	openfec-devel
Requires:	pulseaudio-devel
Requires:	sox-devel >= 14.4.0
Requires:	speexdsp-devel

%description devel
Header files for ROC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ROC.

%package apidocs
Summary:	API documentation for ROC library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ROC
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for ROC library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ROC.

%prep
%setup -q

%build
# docs build seems racy, use -j1
%scons -j1 \
	STRIP=: \
	%{?with_apidocs:--enable-doxygen} \
	%{?with_apidocs:--enable-sphinx} \
	--with-openfec-includes=/usr/include/openfec \
	--libdir=%{_libdir}

# TODO: --enable-pulseaudio-modules

%install
rm -rf $RPM_BUILD_ROOT

%scons -j1 \
	PKG_CONFIG_PATH=$RPM_BUILD_ROOT%{_pkgconfigdir} \
	STRIP=: \
	%{?with_apidocs:--enable-doxygen} \
	%{?with_apidocs:--enable-sphinx} \
	--with-openfec-includes=/usr/include/openfec \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	install

# useless symlink, soname is libroc.so.0.2
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libroc.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/roc-conv
%attr(755,root,root) %{_bindir}/roc-recv
%attr(755,root,root) %{_bindir}/roc-send
%attr(755,root,root) %{_libdir}/libroc.so.0.2
%if %{with apidocs}
%{_mandir}/man1/roc-conv.1*
%{_mandir}/man1/roc-recv.1*
%{_mandir}/man1/roc-send.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libroc.so
%{_includedir}/roc
%{_pkgconfigdir}/roc.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/docs/{_images,_static,about_project,api,internals,manuals,portability,*.html,*.js}
%endif
