# TODO:
# - package systemd user target unit

Summary:	Shared functions for Ayatana indicators (GTK+ 2.x version)
Summary(pl.UTF-8):	Funkcje współdzielone dla wskaźników Ayatana (wersja dla GTK+ 2.x)
Name:		libayatana-indicator
Version:	0.9.1
Release:	1
License:	GPL v3
Group:		Libraries
#Source0Download: https://github.com/AyatanaIndicators/libayatana-indicator/releases
Source0:	https://github.com/AyatanaIndicators/libayatana-indicator/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b7a7fd24a749cb384431b8309db65a58
Patch0:		build-type.patch
URL:		https://github.com/AyatanaIndicators/libayatana-indicator
BuildRequires:	ayatana-ido-devel >= 0.8.2
BuildRequires:	cmake >= 3.13
BuildRequires:	glib2-devel >= 1:2.37
BuildRequires:	gtk+2-devel >= 2:2.18
BuildRequires:	gtk+3-devel >= 3.24
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	which
Requires:	glib2 >= 1:2.37
Requires:	gtk+2 >= 2:2.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This package contains GTK+ 2.x version.

%description -l pl.UTF-8
Zbiór symboli i wygodnych funkcji, które mogą być używane przez
wszystkie wskaźniki Ayatana. Ten pakiet zawiera wersję dla GTK+ 2.x.

%package devel
Summary:	Development files for libayatana-indicator (GTK+ 2.x version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libayatana-indicator (wersja dla GTK+ 2.x)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.37
Requires:	gtk+2-devel >= 2:2.18

%description devel
This package contains the header files for developing applications
that use libayatana-indicator (GTK+ 2.x version).

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libayatana-indicator (w wersji dla GTK+
2.x).

%package gtk3
Summary:	Shared functions for Ayatana indicators (GTK+ 3.x version)
Summary(pl.UTF-8):	Funkcje współdzielone dla wskaźników Ayatana (wersja dla GTK+ 3.x)
Group:		Libraries
Requires:	glib2 >= 1:2.37
Requires:	gtk+3 >= 3.24

%description gtk3
A set of symbols and convenience functions that all Ayatana indicators
are likely to use. This package contains GTK+ 3.x version.

%description gtk3 -l pl.UTF-8
Zbiór symboli i wygodnych funkcji, które mogą być używane przez
wszystkie wskaźniki Ayatana. Ten pakiet zawiera wersję dla GTK+ 3.x.

%package gtk3-devel
Summary:	Development files for libayatana-indicator (GTK+ 3.x version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libayatana-indicator (wersja dla GTK+ 3.x)
Group:		Development/Libraries
Requires:	%{name}-gtk3 = %{version}-%{release}
Requires:	glib2-devel >= 1:2.37
Requires:	gtk+3-devel >= 3.24

%description gtk3-devel
This package contains the header files for developing applications
that use libayatana-indicator (GTK+ 3.x version).

%description gtk3-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libayatana-indicator (w wersji dla GTK+
3.x).

%prep
%setup -q
%patch0 -p1

%build
# we build it twice, once against GTK+ 3 and once against GTK+ 2, so
# both GTK+ 2 and GTK+ 3 apps can use it; the GTK+ 3 build is
# libayatana-indicator-gtk3. When we have no need for the GTK+ 2 build any more
# we can drop the -gtk3 package and have the main package build against
# GTK+ 3.
install -d build-gtk{2,3}
cd build-gtk2
%cmake \
	-DFLAVOUR_GTK2:BOOL=ON \
	..
%{__make}

cd ../build-gtk3
%cmake \
	-DFLAVOUR_GTK3:BOOL=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-gtk2 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C build-gtk3 install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# dirs for library users, see .pc files for paths
install -d $RPM_BUILD_ROOT%{_libdir}/ayatana-{indicators,indicators3}/7
install -d $RPM_BUILD_ROOT%{_datadir}/libayatana-indicator/icons

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	gtk3 -p /sbin/ldconfig
%postun	gtk3 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libayatana-indicator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libayatana-indicator.so.7
%dir %{_libdir}/ayatana-indicators
%dir %{_libdir}/ayatana-indicators/7
%dir %{_datadir}/libayatana-indicator
%dir %{_datadir}/libayatana-indicator/icons

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libayatana-indicator.so
%{_includedir}/libayatana-indicator-0.4
%{_pkgconfigdir}/ayatana-indicator-0.4.pc
# This is marked as 'for development use only'
%{_datadir}/libayatana-indicator/80indicator-debugging

%files gtk3
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libayatana-indicator3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libayatana-indicator3.so.7
%dir %{_libexecdir}/libayatana-indicator
%attr(755,root,root) %{_libexecdir}/libayatana-indicator/ayatana-indicator-loader3
%dir %{_libdir}/ayatana-indicators3
%dir %{_libdir}/ayatana-indicators3/7
%dir %{_datadir}/libayatana-indicator
%dir %{_datadir}/libayatana-indicator/icons

%files gtk3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libayatana-indicator3.so
%{_includedir}/libayatana-indicator3-0.4
%{_pkgconfigdir}/ayatana-indicator3-0.4.pc
