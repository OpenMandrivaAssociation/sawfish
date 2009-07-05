%define libver		0.90.0
%define repver		0.18.4

Name:		sawfish
Summary:	An extensible window manager for the X Window System
Version:	1.5.0
Release: %mkrel 1
Epoch:      	2
License:	GPLv2+
Group:		Graphical desktop/Sawfish
BuildRequires:	gmp-devel gpm-devel ncurses-devel 
BuildRequires:  readline-devel 
BuildRequires:  librep-devel >= %{libver} 
Buildrequires:  texinfo
BuildRequires:  rep-gtk >= %{repver}
BuildRequires:  libgtk+2.0-devel
BuildRequires:  libesound-devel
BuildRequires:  chrpath
URL:		http://sawmill.sourceforge.net/
Source:		http://downloads.sourceforge.net/sawmill/%{name}-%{version}.tar.bz2
Source1:	HeliX.tar.bz2
Source2:	sawfish-site-init-mdk.jl.bz2
Source3:	http://www.acemake.com/hagbard/archives/sawfish.el.bz2
Source5:	%{name}.png.bz2
Source6:	%{name}-32.png.bz2
Source8:	%{name}-icons.tar.bz2
Source9:	startsawfish.bz2
Source10:	%{name}-48.png.bz2
Source11:   ws-background.jl.bz2
Source12:	sawfish-menu.jl.bz2
Source13:   sawfish-defaults.jl.bz2
Patch0:		sawfish-1.5.0-xterm.patch
#gw use the mdk menu under gnome2
Patch1:		sawfish-1.5.0-gnome2-menu.patch
# (fc) 1.0.1-4mdk custom-default settings for sawfish (previously as source7)
Patch3:     sawfish-1.0.1-custom-defaults.patch
Patch4:	sawfish-1.5.0-xdg.patch
Requires:	librep >= %{libver}, rep-gtk >= %{repver}
Requires: xsetroot
Requires(post): info-install
Requires(preun): info-install
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Obsoletes:	sawmill, sawmill-gnome, sawfish-gnome
Provides:   sawmill, sawmill-gnome, sawfish-gnome
Provides:	windowmanager
Obsoletes: sawfish-themer
Provides: sawfish-themer


%description
Sawfish is an extensible window manager which uses a Lisp-based scripting
language.  All window decorations are configurable and the basic idea is to
have as much user-interface policy as possible controlled through the Lisp
language.  Configuration can be accomplished by writing Lisp code in a
personal .sawfishrc file, or using a GTK+ interface.  Sawfish is mostly
GNOME compliant.

%prep
%setup -q -n %name-%version
%patch0 -p1 -b .xterm
%patch1 -p1 -b .menu
%patch3 -p1 -b .defaults
#patch4 -p1 -b .xdg
./autogen.sh

%build
%configure2_5x --bindir=%{x11bindir} 

# don't use make macro, parallel compilation is broken
make host_type=%{_target_platform}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/gnome/wm-properties
mkdir -p %{buildroot}%{x11bindir}

%makeinstall_std host_type=%{_target_platform}

mkdir -p %{buildroot}%{_datadir}/{emacs,sawfish}/site-lisp/ %{buildroot}%{_sysconfdir}/X11/sawfish/site-init.d
bzcat %{SOURCE2} > %{buildroot}%{_datadir}/sawfish/site-lisp/site-init.jl
bzcat %{SOURCE3} > %{buildroot}%{_datadir}/emacs/site-lisp/sawfish.el
bzcat %{SOURCE11} > %{buildroot}%{_datadir}/sawfish/site-lisp/ws-background.jl
bzcat %{SOURCE12} > %{buildroot}%{_sysconfdir}/X11/sawfish/site-init.d/00menu.jl
bzcat %{SOURCE13} > %{buildroot}%{_sysconfdir}/X11/sawfish/site-init.d/00defaults.jl
touch %{buildroot}%{_sysconfdir}/X11/%{name}/mandrake-menu.jl

mkdir -p %{buildroot}%{_sysconfdir}/X11/%{name}
mkdir -p %{buildroot}%{_datadir}/{pixmaps,sawfish/themes}
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/sawfish/themes/
bzcat %{SOURCE8} | tar xvf - -C %{buildroot}%{_datadir}/pixmaps

mv %buildroot%{_datadir}/gnome/wm-properties/ %buildroot%{_datadir}/applications/

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
EXEC=%{x11bindir}/startsawfish
SCRIPT:
exec %{x11bindir}/startsawfish
EOF

bzcat %{SOURCE9} > %{buildroot}/%{x11bindir}/start%{name}

%{find_lang} %{name}
chrpath -d %buildroot%_bindir/sawfish %buildroot%_libdir/rep/*/sawfish/client.so

%post
#gpw: create the menu file to make rpmlint shut up
touch %{_sysconfdir}/X11/%{name}/mandrake-menu.jl
%if %mdkversion < 200900
%update_menus
%endif
%_install_info sawfish.info
%make_session
%if %mdkversion < 200900
/sbin/ldconfig
%endif


%preun
%_remove_install_info sawfish.info

%postun
%if %mdkversion < 200900
%clean_menus
%endif
%make_session
%if %mdkversion < 200900
/sbin/ldconfig
%endif


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS COPYING INSTALL README NEWS FAQ THANKS TODO 
%doc lisp/sawfish/ui/WIDGETS* lisp/sawfish/ui/WISHLIST
%{x11bindir}/sawfish
%{x11bindir}/sawfish-client
%{x11bindir}/sawfish-ui
%attr(755,root,root) %{x11bindir}/startsawfish
%{_libexecdir}/%{name}
%{_libexecdir}/rep/*/%{name}
%{_datadir}/applications/sawfish.desktop
%{_datadir}/sawfish
%{_datadir}/emacs/site-lisp/*
%{_datadir}/pixmaps/*
%{_iconsdir}/sawfish.png
%{_liconsdir}/sawfish.png
%{_miconsdir}/sawfish.png
%{_infodir}/sawfish*
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%dir %{_sysconfdir}/X11/%{name}
%dir %{_sysconfdir}/X11/%{name}/site-init.d
%config(noreplace) %{_sysconfdir}/X11/%{name}/site-init.d/*
%ghost %{_sysconfdir}/X11/%{name}/mandrake-menu.jl
