%define _disable_ld_no_undefined 1

%define libver		0.92.3
%define repver		0.90.7

Summary:	An extensible window manager for the X Window System
Name:		sawfish
Version:	1.10
Release:	2
Epoch:		2
License:	GPLv2+
Group:		Graphical desktop/Sawfish
Url:		http://sawmill.sourceforge.net/
Source0:	http://download.tuxfamily.org/%name/%{name}-%{version}.tar.bz2
BuildRequires:	kdelibs4-core
Buildrequires:	texinfo
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(librep) >= %{libver}
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pangox)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(rep-gtk) >= %{repver}
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xtst)

Requires:	librep >= %{libver}
Requires:	rep-gtk >= %{repver}
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
personal .sawfishrc file, or using a GTK+ interface. Sawfish is mostly
GNOME compliant.

%files -f %{name}.lang
%doc COPYING INSTALL README* NEWS TODO
%{_bindir}/sawfish
%{_bindir}/sawfish-about
%{_bindir}/sawfish-client
%{_bindir}/sawfish-config
%{_libexecdir}/%{name}
%{_libexecdir}/rep/*
%{_datadir}/applications/*.desktop
%{_datadir}/apps/ksmserver/windowmanagers/sawfish.desktop
%{_datadir}/gnome/wm-properties/sawfish-wm.desktop
%{_datadir}/sawfish
%{_datadir}/xsessions/sawfish.desktop
%{_iconsdir}/hicolor/*/apps/sawfish*
%{_mandir}/man1/sawfish.1*
%{_mandir}/man1/sawfish-client.1*
%{_mandir}/man1/sawfish-config.1*
%{_infodir}/sawfish*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for Sawfish
Group:		Graphical desktop/Sawfish
Requires:	%{name} = %{EVRD}

%description devel
This package contains development files for sawfish.

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sawfish/

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x
%make

%install
%makeinstall_std

%find_lang %{name}

