%bcond_without minimal

Name:           gnome-mplayer
Version:        1.0.4
Release:        2%{?dist}
Summary:        An MPlayer GUI, a full-featured binary

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://kdekorte.googlepages.com/gnomemplayer
Source0:        http://gnome-mplayer.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:         %{name}-applefix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
%if 0%{?fedora} < 15
BuildRequires:  GConf2-devel
%endif
BuildRequires:  gettext
BuildRequires:  gnome-power-manager
%if 0%{?fedora} >= 15
BuildRequires:  gtk3-devel
%else
BuildRequires:  gtk2-devel
%endif
BuildRequires:  libcurl-devel
BuildRequires:  libgpod-devel
BuildRequires:  libmusicbrainz3-devel
BuildRequires:  libnotify-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  nautilus-devel
BuildRequires:  pulseaudio-libs-devel

Requires:       control-center-filesystem
Requires:       gvfs-fuse
Requires:       mencoder
Requires:       %{name}-common = %{version}-%{release}

Provides:       %{name}-binary = %{version}-%{release}

%description
GNOME MPlayer is a simple GUI for MPlayer. It is intended to be a nice tight
player and provide a simple and clean interface to MPlayer. GNOME MPlayer has
a rich API that is exposed via DBus. Using DBus you can control a single or
multiple instances of GNOME MPlayer from a single command.
This package provides a full-featured binary.


%package common
Summary:        An MPlayer GUI, common files
Group:          Applications/Multimedia
Requires:       mplayer

%if 0%{?fedora} < 15
Requires(pre):  GConf2
Requires(post): GConf2
Requires(preun): GConf2
%endif

%description common
GNOME MPlayer is a simple GUI for MPlayer. It is intended to be a nice tight
player and provide a simple and clean interface to MPlayer. GNOME MPlayer has
a rich API that is exposed via DBus. Using DBus you can control a single or
multiple instances of GNOME MPlayer from a single command.
This package provides the common files.


%if %{with minimal}
%package minimal
Summary:        An MPlayer GUI, a minimal version
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Provides:       %{name}-binary = %{version}-%{release}

%description minimal
GNOME MPlayer is a simple GUI for MPlayer. It is intended to be a nice tight
player and provide a simple and clean interface to MPlayer. GNOME MPlayer has
a rich API that is exposed via DBus. Using DBus you can control a single or
multiple instances of GNOME MPlayer from a single command.
This package provides a version with reduced requirements, targeted at users
who want browser plugin functionality only.
%endif


%package nautilus
Summary:        An MPlayer GUI, nautilus extension
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       nautilus-extensions

%description nautilus
GNOME MPlayer is a simple GUI for MPlayer. It is intended to be a nice tight
player and provide a simple and clean interface to MPlayer. GNOME MPlayer has
a rich API that is exposed via DBus. Using DBus you can control a single or
multiple instances of GNOME MPlayer from a single command.
This package provides a nautilus extension, which shows properties of audio and
video files in the properties dialogue.


%prep
%setup -qcT
tar -xzf %{SOURCE0}
mv %{name}-%{version} generic
%patch0 -p0 -d generic -b .applefix
%if %{with minimal}
tar -xzf %{SOURCE0}
mv %{name}-%{version} minimal
%patch0 -p0 -d minimal -b .applefix
%endif


%build
pushd generic
%if 0%{?fedora} >= 15
%configure --enable-gtk3
%else
%if 0%{?fedora} == 14
%configure --with-gconf
%else
%configure
%endif
%endif
make %{?_smp_mflags}
popd

%if %{with minimal}
pushd minimal
%configure --program-suffix=-minimal --without-gio --without-libnotify \
%if 0%{?fedora} >= 15
    --enable-gtk3 \
%else
%if 0%{?fedora} == 14
    --with-gconf \
%endif
%endif
    --without-libgpod --without-libmusicbrainz3 --disable-nautilus
make %{?_smp_mflags}
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

pushd generic
%if 0%{?fedora} < 15
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%endif
make install DESTDIR=$RPM_BUILD_ROOT
popd

%if %{with minimal}
pushd minimal
%if 0%{?fedora} < 15
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%endif
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

desktop-file-install --vendor=rpmfusion \
       --delete-original --dir $RPM_BUILD_ROOT%{_datadir}/applications \
       $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

#remove intrusive docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/gnome-mplayer

#kill the libtool archives
find $RPM_BUILD_ROOT -name *.la -exec rm -f {} \;


%pre common
%if 0%{?fedora} < 15
%gconf_schema_prepare gnome-mplayer
%endif

%post
update-desktop-database &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :


%post common
%if 0%{?fedora} < 15
%gconf_schema_upgrade gnome-mplayer
%endif


%postun common
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%if 0%{?fedora} >= 15
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
%endif


%posttrans common
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?fedora} >= 15
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%endif


%preun common
%if 0%{?fedora} < 15
%gconf_schema_remove gnome-mplayer
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/gnome-mplayer
%{_datadir}/applications/rpmfusion-gnome-mplayer.desktop
%{_datadir}/gnome-control-center/default-apps/gnome-mplayer.xml


%files common -f %{name}.lang
%defattr(-,root,root,-)
%doc generic/COPYING generic/ChangeLog generic/README generic/DOCS/keyboard_shortcuts.txt generic/DOCS/tech/*
%if 0%{?fedora} < 15
%{_sysconfdir}/gconf/schemas/gnome-mplayer.schemas
%else
%{_datadir}/glib-2.0/schemas/apps.gecko-mediaplayer.preferences.gschema.xml
%{_datadir}/glib-2.0/schemas/apps.gnome-mplayer.preferences.*
%endif
%{_datadir}/icons/hicolor/*/apps/gnome-mplayer.*
%{_mandir}/man1/gnome-mplayer.1*


%if %{with minimal}
%files minimal
%defattr(-,root,root,-)
%{_bindir}/gnome-mplayer-minimal
%endif


%files nautilus
%defattr(-,root,root,-)
%{_libdir}/nautilus/extensions-?.0/libgnome-mplayer-properties-page.so*


%changelog
* Fri Jul 08 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.4-2
- Fixed apple.com regression using a patch from SVN

* Fri Jul 01 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.4-1
- Updated to 1.0.4
- Enabled gtk3 on Fedora 15 and above

* Mon Apr 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.3-1
- Dropped included patches
- Added logic to support gsettings/GConf
- Updated GConf scriptlets to the latest spec

* Fri Mar 04 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.2-1
- Updated to 1.0.2
- Dropped included patches
- Updated BuildRequires to pulseaudio-libs-devel

* Sun Feb 20 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.0-2
- Fixed intrusive error popup for vdpau (RF #1633)
- Added a conditional for building without the minimal player
- Added support for libnotify-0.7 from SVN
- Fixed rawhide build failure

* Sat Nov 06 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.0-1
- Updated to 1.0.0
- Dropped upstreamed patch

* Thu Feb 25 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.9.2-1
- Updated to 0.9.9.2
- Added bits necessary for https://fedoraproject.org/wiki/Features/ChangeInImplicitDSOLinking

* Sat Feb 06 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.9-1
- Updated to 0.9.9
- Dropped included patch
- Added libXScrnSaver-devel to BuildRequires

* Sat Sep 19 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.8-1
- Updated to 0.9.8

* Fri Aug 21 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.7-1
- Updated to 0.9.7
- Dropped upstreamed patches
- Added icon cache scriptlets
- Added pulseaudio and gnome-power-manager to BuildRequires

* Wed Jul 01 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.6-2
- Fixed screensaver inhibition

* Sun Jun 05 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.6-1
- Updated to 0.9.6
- Dropped upstreamed patches
- Enabled flat volumes by default in Fedora 11 and above

* Tue Apr 21 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.5-3
- Added patch fixing breaking nautilus translation from SVN

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.5-2
- rebuild for new F11 features

* Fri Mar 13 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.5-1
- Updated to 0.9.5
- Added nautilus-devel to BuildRequires
- Packaged nautilus extension separately
- Adjusted whitespaces
- Added keyboard shortcuts to documentation

* Sun Mar 01 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.4-2
- Rebuilt for new libgpod

* Wed Feb  4 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.4-1
- Updated to 0.9.4
- Dropped the upsteamed patch
- Updated the URL

* Thu Jan  8 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.3-2
- Added patch fixing rpmfusion bug #238 from SVN
- Made the dependencies between packages stricter (%%{version} → %%{version}-%%{release})

* Sat Jan  3 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.3-1
- Updated to 0.9.3

* Mon Nov 24 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.2-2
- Refactored the spec to allow building both minimal and full-featured versions
- s/gnome-mplayer-core-functionality/gnome-mplayer-binary

* Sat Nov 22 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.2-1
- Updated to 0.9.2
- Added libcurl-devel, libgpod-devel and libmusicbrainz3-devel to BuildRequires
- Provide gnome-mplayer-core-functionality

* Sun Nov  2 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.1-1
- Updated to 0.9.1

* Fri Oct 31 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.0-1
- Updated to 0.9.0
- Added libnotify-devel to BuildRequires
- Added gvfs-fuse to Requires

* Mon Sep 29 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.0-1.1
- Updated to 0.8.0

* Sat Sep  6 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.7.0-2.1
- Added alsa-lib-devel to BuildRequires (livna bug #2084)

* Sun Aug 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.7.0-1.1
- Updated to 0.7.0

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.6.3-2
- rebuild for buildsys cflags issue

* Sun Jul  6 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.3-1
- Updated to 0.6.3

* Tue Jun 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.2-2
- Added mencoder to Requires (bug #1991)

* Wed May 28 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.2-1
- Updated to 0.6.2

* Thu Apr 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.1-1
- Updated to 0.6.1
- Updated URL and Source0

* Wed Feb 13 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.6.0-1
- Initial rpmfusion release
