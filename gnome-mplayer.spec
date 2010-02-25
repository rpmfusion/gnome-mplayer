Name:           gnome-mplayer
Version:        0.9.9.2
Release:        1%{?dist}
Summary:        An MPlayer GUI, a full-featured binary

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://kdekorte.googlepages.com/gnomemplayer
Source0:        http://gnome-mplayer.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  GConf2-devel
BuildRequires:  gettext
BuildRequires:  gnome-power-manager
BuildRequires:  gtk2-devel
BuildRequires:  libcurl-devel
BuildRequires:  libgpod-devel
BuildRequires:  libmusicbrainz3-devel
BuildRequires:  libnotify-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  nautilus-devel
BuildRequires:  pulseaudio

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

Requires(pre):  GConf2
Requires(post): GConf2
Requires(preun): GConf2

%description common
GNOME MPlayer is a simple GUI for MPlayer. It is intended to be a nice tight
player and provide a simple and clean interface to MPlayer. GNOME MPlayer has
a rich API that is exposed via DBus. Using DBus you can control a single or
multiple instances of GNOME MPlayer from a single command.
This package provides the common files.


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
tar -xzf %{SOURCE0}
mv %{name}-%{version} minimal


%build
pushd generic
%configure
make %{?_smp_mflags}
popd

pushd minimal
%configure --program-suffix=-minimal --without-gio --without-libnotify \
    --without-libgpod --without-libmusicbrainz3 --disable-nautilus
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd generic
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd minimal
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
popd

desktop-file-install --vendor=rpmfusion \
       --delete-original --dir $RPM_BUILD_ROOT%{_datadir}/applications \
       $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

#remove intrusive docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/gnome-mplayer

#kill the libtool archives
find $RPM_BUILD_ROOT -name *.la -exec rm -f {} \;


%pre common
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-mplayer.schemas >/dev/null || :
    # If the schema file has ever been renamed::
    #gconftool-2 --makefile-uninstall-rule \
    #  %{_sysconfdir}/gconf/schemas/[OLDNAME].schemas > /dev/null || :
fi


%post
update-desktop-database &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :


%post common
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/gnome-mplayer.schemas > /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun common
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans common
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%preun common
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/gnome-mplayer.schemas > /dev/null || :
fi


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
%{_sysconfdir}/gconf/schemas/gnome-mplayer.schemas
%{_datadir}/icons/hicolor/*/apps/gnome-mplayer.*
%{_mandir}/man1/gnome-mplayer.1*


%files minimal
%defattr(-,root,root,-)
%{_bindir}/gnome-mplayer-minimal


%files nautilus
%defattr(-,root,root,-)
%{_libdir}/nautilus/extensions-2.0/libgnome-mplayer-properties-page.so*


%changelog
* Thu Feb 25 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.9.2-1
- Updated to 0.9.9.2

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
