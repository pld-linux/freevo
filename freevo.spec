%define geometry 800x600
%define display  x11
%define tv_norm  pal
%define chanlist europe-west
Summary:        Freevo
Name: 		freevo
Version: 	1.5.0
Release: 	1
Source0:	http://dl.sourceforge.net/freevo/freevo-1.5.0.tar.gz
Source1: 	freevo-boot_config
License: 	GPL
Group: 		Applications/Multimedia
BuildArch: 	noarch
BuildRequires:  docbook-utils
Requires: 	SDL_image >= 1.2.3
Requires:	SDL_ttf >= 2.0.6
Requires:	SDL_mixer >= 1.2.5
Requires: 	smpeg >= 0.4.4
Requires:	util-linux
Requires: 	python-game >= 1.5.6
Requires:	python-imaging >= 1.1.4
BuildRequires:	python-PyXML
BuildRequires: 	python-mmpython >= 0.4.4
Requires:	mx >= 2.0.5
Requires:	python-numeric >= 23.1
Requires: 	aumix >= 2.8 
Requires:	libjpeg >= 6b
Requires:	libexif >= 0.5.10
Requires: 	python-Twisted >= 1.1.0
Requires: 	lsdvd
URL:            http://freevo.sourceforge.net/
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as xine, mplayer, tvtime and mencoder to play
and record video and audio.

%package boot
Summary: Files to enable a standalone Freevo system (started from initscript)
Group: Applications/Multimedia
Requires:       %{name}

%description boot
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as mplayer and mencoder to play and record
video and audio.

Note: This installs the initscripts necessary for a standalone Freevo system.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q 

%build
find . -name CVS | xargs rm -rf
find . -name ".cvsignore" |xargs rm -f
find . -name "*.pyc" |xargs rm -f
find . -name "*.pyo" |xargs rm -f
find . -name "*.py" |xargs chmod 644

#./autogen.sh

env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

mkdir -p %{buildroot}%{_sysconfdir}/freevo
# The following is needed to let RPM know that the files should be backed up
touch %{buildroot}%{_sysconfdir}/freevo/freevo.conf

# boot scripts
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_bindir}
install -m 755 boot/freevo %{buildroot}%{_sysconfdir}/rc.d/init.d
#install -m 755 boot/freevo_dep %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 boot/recordserver %{buildroot}%{_sysconfdir}/rc.d/init.d/freevo_recordserver
install -m 755 boot/webserver %{buildroot}%{_sysconfdir}/rc.d/init.d/freevo_webserver
install -m 755 boot/recordserver_init %{buildroot}%{_bindir}/freevo_recordserver_init
install -m 755 boot/webserver_init %{buildroot}%{_bindir}/freevo_webserver_init
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/freevo/boot_config


mkdir -p %{buildroot}%{_logdir}/freevo
mkdir -p %{buildroot}%{_cachedir}/freevo
mkdir -p %{buildroot}%{_cachedir}/freevo/{thumbnails,audio}
mkdir -p %{buildroot}%{_cachedir}/xmltv/logos
chmod 777 %{buildroot}%{_cachedir}/{freevo,freevo/thumbnails,freevo/audio,xmltv,xmltv/logos}
chmod 777 %{buildroot}%{_logdir}/freevo

%install
python setup.py install \
		--root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

install -m 644 local_conf.py.example %{buildroot}%{_docdir}

mkdir -p %{buildroot}%{_contribdir}/lirc
cp -av contrib/lirc %{buildroot}%{_contribdir}

#%doc BUGS COPYING ChangeLog FAQ INSTALL README TODO Docs local_conf.py.example
#%doc contrib/lirc 
%attr(644,root,root) %{_docdir}/local_conf.py.example
%attr(755,root,root) %dir %{_docdir}/installation
%attr(755,root,root) %dir %{_docdir}/plugin_writing
%attr(755,root,root) %dir %{_contribdir}/fbcon
%attr(755,root,root) %dir %{_contribdir}/lirc
%attr(644,root,root) %{_contribdir}/lirc/*
%attr(755,root,root) %dir %{_sysconfdir}/freevo
%attr(777,root,root) %dir %{_logdir}/freevo
%attr(777,root,root) %dir %{_cachedir}/freevo
%attr(777,root,root) %dir %{_cachedir}/freevo/audio
%attr(777,root,root) %dir %{_cachedir}/freevo/thumbnails
%attr(777,root,root) %dir %{_cachedir}/xmltv
%attr(777,root,root) %dir %{_cachedir}/xmltv/logos
%attr(644,root,root) %config %{_sysconfdir}/freevo/freevo.conf
#%attr(644,root,root) %config %{_sysconfdir}/freevo/record_config.py

%post

# Copy old local_conf.py to replace dummy file
%{_bindir}/freevo setup --geometry=%{geometry} --display=%{display} \
        --tv=%{tv_norm} --chanlist=%{chanlist} 

%preun

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%doc BUGS COPYING ChangeLog FAQ INSTALL README TODO Docs local_conf.py.example
%doc contrib/lirc 
%attr(644,root,root) %{_docdir}/local_conf.py.example
%attr(755,root,root) %dir %{_docdir}/installation
%attr(755,root,root) %dir %{_docdir}/plugin_writing
%attr(755,root,root) %dir %{_contribdir}/fbcon
%attr(755,root,root) %dir %{_contribdir}/lirc
%attr(644,root,root) %{_contribdir}/lirc/*
%attr(755,root,root) %dir %{_sysconfdir}/freevo
%attr(777,root,root) %dir %{_logdir}/freevo
%attr(777,root,root) %dir %{_cachedir}/freevo
%attr(777,root,root) %dir %{_cachedir}/freevo/audio
%attr(777,root,root) %dir %{_cachedir}/freevo/thumbnails
%attr(777,root,root) %dir %{_cachedir}/xmltv
%attr(777,root,root) %dir %{_cachedir}/xmltv/logos
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/freevo/freevo.conf
#%attr(644,root,root) %config(noreplace) %{_sysconfdir}/freevo/record_config.py

%files boot
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d
%attr(755,root,root) %{_bindir}/freevo_*
%attr(755,root,root) %dir %{_sysconfdir}/freevo
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/freevo/boot_config

%post boot
# Add the service, but don't automatically invoke it
# user has to enable it via ntsysv
if [ -x /sbin/chkconfig ]; then
     chkconfig --add freevo
     chkconfig --levels 234 freevo off
#     chkconfig --add freevo_dep
     chkconfig --add freevo_recordserver
     chkconfig --levels 234 freevo_recordserver off
     chkconfig --add freevo_webserver
     chkconfig --levels 234 freevo_webserver off
fi
depmod -a

%preun boot
if [ "$1" = 0 ] ; then
  if [ -x /sbin/chkconfig ]; then
     chkconfig --del freevo
#     chkconfig --del freevo_dep
     chkconfig --del freevo_recordserver
     chkconfig --del freevo_webserver
  fi
fi
