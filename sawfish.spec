%define libver		0.92.1
%define repver		0.90.7

Name:		sawfish
Summary:	An extensible window manager for the X Window System
Version:	1.8.91
Release:	2
Epoch:		2
License:	GPLv2+
Group:		Graphical desktop/Sawfish
BuildRequires:	gmp-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	kdelibs4-core
BuildRequires:	librep-devel >= %{libver}
Buildrequires:	texinfo
BuildRequires:	rep-gtk-devel >= %{repver}
BuildRequires:	libgtk+2.0-devel
BuildRequires:	esound-devel
BuildRequires:	libice-devel
BuildRequires:	libsm-devel
BuildRequires:	libxtst-devel
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(pangox)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	libxft-devel
URL:		http://sawmill.sourceforge.net/
Source:		http://download.tuxfamily.org/%name/%{name}-%{version}.tar.xz
Source1:	HeliX.tar.bz2
Source2:	sawfish-site-init-mdk.jl.bz2
Source3:	http://www.acemake.com/hagbard/archives/sawfish.el.bz2
Source5:	%{name}.png.bz2
Source6:	%{name}-32.png.bz2
Source8:	%{name}-icons.tar.bz2
Source9:	startsawfish.bz2
Source10:	%{name}-48.png.bz2
Source11:	ws-background.jl.bz2
Source13:	sawfish-defaults.jl.bz2
Patch0:		sawfish-1.6.0~rc1-xterm.patch
# (fc) 1.0.1-4mdk custom-default settings for sawfish (previously as source7)
Patch3:		sawfish-1.6.0~rc1-custom-defaults.patch
Patch4:		sawfish-1.5.0-xdg.patch
Requires:	librep >= %{libver}
Provides:	rep-gtk >= %{repver}
Requires:	xsetroot
Provides:	windowmanager
Provides:	sawmill
Provides:	sawmill-gnome
Provides:	sawfish-gnome
Provides:	sawfish-themer

%description
Sawfish is an extensible window manager which uses a Lisp-based scripting
language. All window decorations are configurable and the basic idea is to
have as much user-interface policy as possible controlled through the Lisp
language. Configuration can be accomplished by writing Lisp code in a
personal .sawfishrc file, or using a GTK+ interface.  Sawfish is mostly
GNOME compliant.

%package devel
Summary:	Development files for Sawfish
Group:		Graphical desktop/Sawfish
Requires:	%{name} = %{EVRD}

%description devel
This package contains development files for sawfish.

%prep
%setup -q
%patch0 -p1 -b .xterm
%patch3 -p1 -b .defaults

%build
%configure2_5x

# don't use make macro, parallel compilation is broken
make host_type=%{_target_platform}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/gnome/wm-properties
mkdir -p %{buildroot}%{_bindir}

%makeinstall_std host_type=%{_target_platform}

mkdir -p %{buildroot}%{_datadir}/{emacs,sawfish}/site-lisp/ %{buildroot}%{_sysconfdir}/X11/sawfish/site-init.d
bzcat %{SOURCE2} > %{buildroot}%{_datadir}/sawfish/site-lisp/site-init.jl
bzcat %{SOURCE3} > %{buildroot}%{_datadir}/emacs/site-lisp/sawfish.el
bzcat %{SOURCE11} > %{buildroot}%{_datadir}/sawfish/site-lisp/ws-background.jl
bzcat %{SOURCE13} > %{buildroot}%{_sysconfdir}/X11/sawfish/site-init.d/00defaults.jl

mkdir -p %{buildroot}%{_sysconfdir}/X11/%{name}
mkdir -p %{buildroot}%{_datadir}/{pixmaps,sawfish/themes}
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/sawfish/themes/
bzcat %{SOURCE8} | tar xvf - -C %{buildroot}%{_datadir}/pixmaps

mv %{buildroot}%{_datadir}/gnome/wm-properties/ %{buildroot}%{_datadir}/applications/
mv %{buildroot}%{_datadir}/applications/wm-properties/*.desktop %{buildroot}%{_datadir}/applications/
rm -f %{buildroot}%{_datadir}/xsessions/sawfish.desktop

# icon
mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_liconsdir}
bzcat %{SOURCE5} > %{buildroot}%{_miconsdir}/%{name}.png
bzcat %{SOURCE6} > %{buildroot}%{_iconsdir}/%{name}.png
bzcat %{SOURCE10} > %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/08Sawfish
NAME=Sawfish
ICON=sawfish.png
DESC=The Sawfish Window Manager
EXEC=%{_bindir}/startsawfish
SCRIPT:
exec %{_bindir}/startsawfish
EOF

bzcat %{SOURCE9} > %{buildroot}/%{_bindir}/start%{name}

%find_lang %{name}

%post
#gpw: create the menu file to make rpmlint shut up
#touch %{_sysconfdir}/X11/%{name}/mandrake-menu.jl
%make_session

%postun
%make_session

%files -f %{name}.lang
%doc COPYING INSTALL README* NEWS FAQ TODO 
%{_bindir}/sawfish
%{_bindir}/sawfish-about
%{_bindir}/sawfish-client
%{_bindir}/sawfish-config
%attr(755,root,root) %{_bindir}/startsawfish
%{_libexecdir}/%{name}
%{_libexecdir}/rep/*
%{_datadir}/applications/*.desktop
%{_datadir}/sawfish
%{_datadir}/emacs/site-lisp/*
%{_datadir}/pixmaps/*
%{_datadir}/apps/ksmserver/windowmanagers/sawfish.desktop
%{_datadir}/icons/hicolor/*/apps/sawfish*
%{_iconsdir}/sawfish.png
%{_liconsdir}/sawfish.png
%{_miconsdir}/sawfish.png
%{_mandir}/man1/sawfish.1*
%{_mandir}/man1/sawfish-client.1*
%{_mandir}/man1/sawfish-config.1*
%{_infodir}/sawfish*
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%dir %{_sysconfdir}/X11/%{name}
%dir %{_sysconfdir}/X11/%{name}/site-init.d
%config(noreplace) %{_sysconfdir}/X11/%{name}/site-init.d/*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sawfish/


%changelog
* Mon Jun 04 2012 Andrey Bondrov <abondrov@mandriva.org> 2:1.8.91-2
+ Revision: 802252
- Drop some legacy junk

* Fri Jan 06 2012 Götz Waschk <waschk@mandriva.org> 2:1.8.91-1
+ Revision: 758189
- new version
- update build deps

* Tue Aug 30 2011 Götz Waschk <waschk@mandriva.org> 2:1.8.90-1
+ Revision: 697439
- update file list
- update build deps
- new version
- bump deps

* Mon May 02 2011 Götz Waschk <waschk@mandriva.org> 2:1.8.1-1
+ Revision: 661794
- new version
- bump librep dep
- update file list

* Sat Mar 26 2011 Götz Waschk <waschk@mandriva.org> 2:1.8.0-1
+ Revision: 648563
- new version
- update source URL

* Thu Dec 16 2010 Götz Waschk <waschk@mandriva.org> 2:1.7.1-1mdv2011.0
+ Revision: 622300
- update build deps
- new version
- bump deps
- update file list

* Sun Jul 11 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.3.1-1mdv2011.0
+ Revision: 550672
- update to new version 1.6.3.1

* Tue Feb 16 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.2-1mdv2010.1
+ Revision: 506612
- new version
- fix source URL

* Tue Jan 19 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.1-3mdv2010.1
+ Revision: 493543
- remove old mandrake menu

* Sat Jan 09 2010 Götz Waschk <waschk@mandriva.org> 2:1.6.1-1mdv2010.1
+ Revision: 488072
- new version
- bump librep and rep-gtk deps
- fix build deps for KDE4 window manager support
- update file list

* Tue Dec 22 2009 Götz Waschk <waschk@mandriva.org> 2:1.6.0-1mdv2010.1
+ Revision: 481601
- new version

* Sat Dec 19 2009 Götz Waschk <waschk@mandriva.org> 2:1.6.0-0.rc1.1mdv2010.1
+ Revision: 480108
- new version
- update file list
- bump librep dep
- rediff patches 0,3
- drop patch 1

* Fri Nov 13 2009 Götz Waschk <waschk@mandriva.org> 2:1.5.3-1mdv2010.1
+ Revision: 465680
- update to new version 1.5.3

* Sun Sep 20 2009 Götz Waschk <waschk@mandriva.org> 2:1.5.2-1mdv2010.0
+ Revision: 445291
- update to new version 1.5.2

* Tue Sep 01 2009 Götz Waschk <waschk@mandriva.org> 2:1.5.1-1mdv2010.0
+ Revision: 423659
- new version
- update file list

* Tue Jul 07 2009 Götz Waschk <waschk@mandriva.org> 2:1.5.0-2mdv2010.0
+ Revision: 393353
- fix devel dep

* Sun Jul 05 2009 Funda Wang <fwang@mandriva.org> 2:1.5.0-1mdv2010.0
+ Revision: 392586
- add devel sub package
- fix file list
- drop x11bindir
- rediff xterm patch
- new version 1.5.0

* Mon Jun 08 2009 Götz Waschk <waschk@mandriva.org> 2:1.3.5.3-1mdv2010.0
+ Revision: 384076
- update to new version 1.3.5.3

* Thu Mar 05 2009 Götz Waschk <waschk@mandriva.org> 2:1.3.5.2-2mdv2009.1
+ Revision: 348835
- new version
- bump deps
- update license
- spec cleanup

* Tue Dec 23 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.5.1-1mdv2009.1
+ Revision: 317822
- new version

* Sat Dec 20 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.5-1mdv2009.1
+ Revision: 316404
- new version
- bump deps
- update patch 1
- fix the patch again

* Wed Sep 03 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.4-2mdv2009.0
+ Revision: 279721
- fix desktop entry for new gnome-session

* Fri Aug 29 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.4-1mdv2009.0
+ Revision: 277326
- new version
- rediff patch 4
- update file list

* Mon Aug 04 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.4-0.rc1.1mdv2009.0
+ Revision: 263572
- new version
- rediff patches 0,4
- update file list

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 2:1.3.3-4mdv2009.0
+ Revision: 260500
- rebuild
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.3-1mdv2008.1
+ Revision: 172204
- new version

* Sun Jan 20 2008 Götz Waschk <waschk@mandriva.org> 2:1.3.2-1mdv2008.1
+ Revision: 155369
- new version
- update patch 4

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Jul 28 2007 Götz Waschk <waschk@mandriva.org> 2:1.3.1-1mdv2008.0
+ Revision: 56469
- new version
- drop patch 2
- unpack patches
- Import sawfish




* Thu Aug 24 2006 G�tz Waschk <waschk@mandriva.org> 1.3-9mdv2007.0
- remove rpath

* Wed Aug  9 2006 G�tz Waschk <waschk@mandriva.org> 1.3-8mdv2007.0
- depend on xsetroot
- fix path in startsawfish

* Wed Aug  2 2006 G�tz Waschk <waschk@mandriva.org> 1.3-7mdv2007.0
- xdg menu
- drop menu method

* Tue Jan 10 2006 Götz Waschk <waschk@mandriva.org> 1.3-6mdk
- Rebuild
- use mkrel

* Thu Jun  2 2005 G�tz Waschk <waschk@mandriva.org> 1.3-5mdk
- patch for gcc 4

* Wed Dec  8 2004 G�tz Waschk <waschk@linux-mandrake.com> 1.3-4mdk
- rebuild for libgdbm3

* Sun Jan 25 2004 G�tz Waschk <waschk@linux-mandrake.com> 1.3-3mdk
- patch to use the mdk gnome menu

* Wed Mar 26 2003 G�tz Waschk <waschk@linux-mandrake.com> 1.3-2mdk
- fix the rpmlint warning about the ghost file
- spec cleanup
- build for i586 instead of i686

* Tue Mar 25 2003 G�tz Waschk <waschk@linux-mandrake.com> 1.3-1mdk
- update file list
- drop the merged patches 1 and 4
- new version

* Wed Mar 12 2003 G�tz Waschk <waschk@linux-mandrake.com> 1.2-4mdk
- fix buildrequires

* Thu Feb 27 2003 G�tz Waschk <waschk@linux-mandrake.com> 1.2-3mdk
- patch to build with gtk+2.2
- new librep

* Mon Nov 18 2002 Levi Ramsey <leviramsey@linux-mandrake.com> 1.2-2mdk
- add patch from Sawfish CVS to fix issues with some fullscreen apps
    (mplayer et al)
- change icons to pngs

* Fri Nov 15 2002 G�tz Waschk <waschk@linux-mandrake.com> 1.2-1mdk
- provide sawfish-themer for rpmlint
- fix build with libXft2
- buildrequires libgdk_pixbuf2.0-devel, libXft2-devel, libgtk+2.0-devel
- requires rep-gtk 0.17
- new version

* Fri Aug  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.1a-2mdk
- Recompiled against latest librep/rep-gtk

* Mon Jul  1 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.1a-1mdk
- Release 1.1a (which is greater than 2.0 :((

* Mon Jun 24 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-1mdk
- Release 2.0

* Wed Jun 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-9.20020611.1mdk
- new snapshot

* Tue Jun  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-9.20020524.1mdk
- new snapshot
- put ws-background back
- Remove patch 4 (merged upstream)

* Fri May  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-9.20020502.1mdk
- GNOME 2 cvs snapshot
- Remove patches 1, 2 (merged upstream), 4 (no longer needed)
- Remove source 14 (merged upstream)
- Regenerate patch 0
- Obsoletes sawfish-themer now, it has not been updated to GNOME 2 yet

* Fri May  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-8mdk
- Switch back to 1.0.1
- Remove patch 1 & 4 (merged upstream)


* Tue Mar 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-9mdk
- Reverting to 1.0 version, too many things are broken in 1.0.1
- Readd patch 1 & 4

* Wed Feb 27 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.1-7mdk
- integrated Basque translation

* Wed Feb 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-6mdk
- Update patch3: fix default focus to be click focus with autoraise

* Mon Feb 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-5mdk
- Patch3 : replace Source7 and disable tooltips, they are more annoying than helpful

* Thu Jan  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-4mdk
- Recompiled against latest libcapplet

* Mon Dec 24 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0.1-3mdk
- BuildRequires

* Mon Dec  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-2mdk
- Patch 1 (CVS): fix dock in GNOME

* Thu Oct 25 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.1-1mdk
- Release 1.0.1
- Remove patches 1 & 2 (merged upstream)

* Tue Oct 23 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-8mdk
- Fix sawfish-themer dependency (thanks to Michael Reinsch)
- Fix rpmlint errors

* Tue Oct 16 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0-7mdk
- rebuilt with libpng3

* Wed Sep 19 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-6mdk
- Fix startsawfish to use correct color

* Fri Sep 14 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0-5mdk
- rebuild including latest translations

* Fri Sep 14 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-4mdk
- Patch2: fixes various bugs

* Fri Aug 10 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-2mdk
- Disable gdk-pixbuf (seems to be unstable ..)

* Sat Jul 14 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0-2mdk
- BuildRequires:      db1-devel
- Removed BuildRequires:      ORBit-devel
- Removed BuildRequires:      XFree86-devel
- Removed BuildRequires:      audiofile-devel
- Removed BuildRequires:      esound-devel
- Removed BuildRequires:      gdk-pixbuf-xlib
- Removed BuildRequires:      gnome-libs-devel
- Removed BuildRequires:      imlib-devel
- Removed BuildRequires:      libjpeg-devel
- Removed BuildRequires:      libpng-devel
- Removed BuildRequires:      librep
- Removed BuildRequires:      libtiff-devel
- Removed BuildRequires:      libungif-devel
- Removed BuildRequires:      rep-gtk
- Removed BuildRequires:      zlib-devel

* Wed Jul 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-1mdk
- Release 1.0

* Tue Jul  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.99-1mdk
- Release 0.99
- Regenerate patch 1

* Wed Jun 20 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.38-4mdk
- Patch1: fix multibyte for some translation (from GNOME CVS)
- Move config files to /etc/X11/sawfish (sync with Debian)
- Fix menu method (sync with Debian)

* Fri Mar 23 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.38-3mdk
- explicitly require gdk-pixbuf-xlib

* Fri Mar 23 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.38-2mdk
- Recompiled against gdk-pixbuf instead of imlib
- Correct shortcuts and default theme settings
- Don't remove rpm build dir at clean stage, it is up to --clean option

* Wed Mar 14 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.38-1mdk
- 0.38
- remove obsolete nill patch

* Wed Mar  7 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.37.3-3mdk
- Remove dependency against libgmp.so.2

* Fri Mar  2 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.37.3-2mdk
- change all instances of xterm to xvt for alternatives

* Wed Feb 20 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.37.3-1mdk
- 0.37.3

* Fri Feb 16 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.37.2-1mdk
- 0.37.2

* Sun Jan 21 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.36-1mdk
- 0.36
- added Provides: windowmanager
- update custom-defaults.jl for 0.36 syntax

* Sun Jan 07 2001 Vincent Danen <vdanen@mandrakesoft.com> 0.35-1mdk
- 0.35

* Mon Dec 11 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.34-2mdk
- fix ws-background.jl so background switching works again

* Fri Dec  8 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.34-1mdk
- 0.34

* Mon   Nov 13 2000 Daouda Lo <daouda@mandrakesoft.com> 0.33-2mdk
- sawfish shouldn't be owner of  /usr/share/icons

* Thu Nov 09 2000 Daouda Lo <daouda@mandrakesoft.com> 0.33-1mdk
- release

* Mon Nov  6 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.32-3mdk
- rebuild for new libstdc++
- dependency for librep-0.13.2

* Sat Nov 04 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.32-2mdk
- add longtitle to menu

* Fri Oct 20 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.32-1mdk
- 0.32
- add find_lang macro

* Sun Oct 15 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.31.1-4mdk
- syntax error in ws-backgrounds.jl 'workspace -> 'sawfish.wm.workspace

* Wed Oct 11 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.31.1-3mdk
- fix custom defaults placement (was in wrong dir)
- re-generated custom defaults due to lisp changes
- remove old buildroot during %%build instead of %%install

* Tue Oct 10 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.31.1-2mdk
- fix improper ownership of /usr/share/icons

* Mon Oct 09 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.31.1-1mdk
- 0.31.1

* Sun Oct 08 2000 David BAUDENS <baudens@mandrakesoft.com> 0.30.3-17mdk
- Fix move window with mouse (Linux-Mandrake UI charter compliant)

* Wed Oct  4 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-16mdk
- Update for more backgrounds

* Tue Oct  3 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-15mdk
- Add background change on workspace

* Mon Sep 25 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.30.3-14mdk
- added requirement for rep-gtk-gnome (without it sawfish capplet is 
  broken)

* Fri Sep  8 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-13mdk
- Change font and time for tooltips
- use more macros

* Thu Aug 31 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-12mdk
- Fix wmsession again

* Thu Aug 30 2000 David BAUDENS <baudens@mandrakesoft.com> 0.30.3-11mdk
- Fix wmsession

* Wed Aug 30 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-10mdk
- Change default settings (keybinding, number of desktop)

* Tue Aug 29 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.30.3-9mdk
- Move binaries to /usr/X11R6/bin
- Correct menu load when gnome is not started

* Wed Aug 16 2000 David BAUDENS <baudens@mandrakesoft.com> 0.30.3-8mdk
- Fix menu entry

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.30.3-7mdk
- automatically added BuildRequires

* Sat Aug  5 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-6mdk
- fix site-init-mdk.jl
- merge with author's specfile
- custom-defaults were causing problems so created entirely new one based
  on 0.30.3 (previous was 0.24?!?)

* Thu Aug  3 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-5mdk
- force version requirements for librep and rep-gtk

* Thu Aug  3 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-5mdk
- add some default shortcuts

* Tue Aug  1 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-4mdk
- 6Sawfish to 6sawfish

* Sun Jul 30 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-3mdk
- put 6Sawfish back in (ooops)

* Thu Jul 27 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-2mdk
- remove capplet package since sawfish includes it's own
- remove 6Sawfish from package

* Thu Jul 27 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.3-1mdk
- 0.30.3
- add BuildPreReq: texinfo
- please use rep-gtk-0.13a-3mdk and librep-0.12.4-2mdk due to some
  rpm problems in the previous builds

* Wed Jul 19 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.2-2mdk
- rebuild for directory changes

* Sat Jul 15 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30.2-1mdk
- 0.30.2

* Wed Jul 12 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30-2mdk
- add /etc/X11/wmsession.d/6Sawfish
- more macroization

* Tue Jul 11 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.30-1mdk
- 0.30
- make themer a seperate package again
- merge gnome support into main package (this makes it like author's)

* Mon Jul 10 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.29-1mdk
- 0.29
- macroization
- many other specfile cleanups

* Tue May 23 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.27.2-2mdk
- update BuildPreReq to include rep-gtk and rep-gtk-gnome

* Thu May 11 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.27.2-1mdk
- 0.27.2

* Thu May 11 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.27.1-1mdk
- added BuildPreReq
- change name from Sawmill to Sawfish
- change Group
- replace sawmill.el with sawfish.el
- renamed sawmill-menu-method to sawfish-menu-method and fixed
- renamed icons
- updated desktop menus
- remove nobeep, capplet and foobar patches (code fixed)
- Obsoletes sawmill
- 0.27.1

* Thu May 11 2000 Daouda Lo <daouda@mandrakesoft.com> 0.26-5mdk
- fix the silly window no value bug ! no beep at all !
- sawmill icons in control center finally appear!
- Many cleanups !

* Mon May  1 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.26-4mdk
- added icons to menu entry

* Fri Apr 28 2000 dam's <damien@mandrakesoft.com> 0.26-3mdk
- added fndSession call.

* Wed Apr 19 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.26-2mdk
- re-include sawmill themer in the main package since its light
- fix filelist

* Tue Apr 18 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.26-1mdk 
- fix group
- applied helixcode gnome patches and mandrake optimization
- remove sawmill-themer component (obsoletes it, is included in main sawmill
  package)

* Mon Apr 10 2000 Vincent Danen <vdanen@linux-mandrake.com>
- fix prefix

* Sun Mar 19 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.25.2

* Sat Mar 11 2000 Vincent Danen <vdanen@linux-mandrake.com>
- requires new versions of librep and rep-gtk
- included the Sawmill settings in gnome/apps

* Sat Mar 11 2000 Vincent Danen <vdanen@linux-mandrake.com>
- specfile cleanups
- 0.25.1

* Mon Feb 14 2000 Vincent Danen <vdanen@linux-mandrake.com>
- 0.24

* Fri Feb 04 2000 Lenny Cartier <lenny@mandrakesoft.com>
- new in contribs
- used another great srpm provided by Vincent Danen <vdanen@linux-mandrake.com>

* Sun Jan 30 2000 Vincent Danen <vdanen@linux-mandrake.com>
- initial specfile
- bzip sources
