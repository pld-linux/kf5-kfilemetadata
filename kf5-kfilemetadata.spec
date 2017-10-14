#
# Conditional build:
%bcond_without	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.39
%define		qtver		5.3.2
%define		kfname		kfilemetadata
Summary:	File metadata and extraction library
Name:		kf5-%{kfname}
Version:	5.39.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	1d3c50629123cf5eabf94fba87ff0be9
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	catdoc
BuildRequires:	cmake >= 2.8.12
BuildRequires:	ebook-tools-devel
BuildRequires:	exiv2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	poppler-qt5-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	taglib-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
File metadata and extraction library.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5FileMetaData.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5FileMetaData.so.3
%dir %{_libdir}/qt5/plugins/kf5/kfilemetadata
%dir %{_libdir}/qt5/plugins/kf5/kfilemetadata/writers
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/writers/kfilemetadata_taglibwriter.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_epubextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_exiv2extractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_ffmpegextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_odfextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_office2007extractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_officeextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_plaintextextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_poextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_popplerextractor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_taglibextractor.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5FileMetaData.so
%{_includedir}/KF5/KFileMetaData
%{_libdir}/cmake/KF5FileMetaData
