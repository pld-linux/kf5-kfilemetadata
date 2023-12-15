#
# Conditional build:
%bcond_with	tests		# build with tests

# TODO:
# - runtime Requires if any

%define         kdeappsver      21.12.3
%define		kdeframever	5.113
%define		qtver		5.15.2
%define		kfname		kfilemetadata
Summary:	File metadata and extraction library
Summary(pl.UTF-8):	Biblioteka do obsługi i wydobywania metadanych plików
Name:		kf5-%{kfname}
Version:	5.113.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	709952cf04d6927d87f99aed9fc3d2b6
Patch0:		xattr.patch
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	attr-devel
BuildRequires:	catdoc
BuildRequires:	cmake >= 3.16
BuildRequires:	ebook-tools-devel
BuildRequires:	exiv2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	ka5-kdegraphics-mobipocket-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-karchive-devel >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	ninja
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
#%%patch0 -p1

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories5/kfilemetadata.categories
%attr(755,root,root) %{_libdir}/libKF5FileMetaData.so.*.*.*
%ghost %{_libdir}/libKF5FileMetaData.so.3
%dir %{_libdir}/qt5/plugins/kf5/kfilemetadata
%dir %{_libdir}/qt5/plugins/kf5/kfilemetadata/writers
%{_libdir}/qt5/plugins/kf5/kfilemetadata/writers/kfilemetadata_taglibwriter.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_epubextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_exiv2extractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_fb2extractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_ffmpegextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_odfextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_office2007extractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_officeextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_plaintextextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_poextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_popplerextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_postscriptdscextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_taglibextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_xmlextractor.so
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_mobiextractor.so
%{_datadir}/qlogging-categories5/kfilemetadata.renamecategories
%{_libdir}/qt5/plugins/kf5/kfilemetadata/kfilemetadata_pngextractor.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5FileMetaData.so
%{_includedir}/KF5/KFileMetaData
%{_libdir}/cmake/KF5FileMetaData
%{_libdir}/qt5/mkspecs/modules/qt_KFileMetaData.pri
