Summary:	Freevo - open-source home theatre PC platform
Summary(pl):	Freevo - zestaw kina domowego oparty na platformie PC i otwartych ¼ród³ach
Name:		freevo
Version:	1.5.3
Release:	1
License:	GPL
Group:		Applications/Multimedia
Source0:	http://dl.sourceforge.net/freevo/%{name}-%{version}.tar.gz
# Source0-md5:	20263d2a4de1fc5948391c6b2ca04b0d
Source1:	%{name}-boot_config
URL:		http://freevo.sourceforge.net/
BuildRequires:	SDL_image >= 1.2.3
BuildRequires:	SDL_mixer >= 1.2.5
BuildRequires:	SDL_ttf >= 2.0.6
BuildRequires:	docbook-utils
BuildRequires:	libexif-devel >= 0.5.10
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	python-Imaging >= 1.1.4
BuildRequires:	python-PyXML
BuildRequires:	python-Twisted >= 1.1.0
BuildRequires:	python-mmpython >= 0.4.4
BuildRequires:	python-mx-Tools >= 2.0.5
BuildRequires:	python-numpy >= 23.1
BuildRequires:	python-pygame >= 1.5.6
Requires:	aumix >= 2.8
Requires:	lsdvd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as xine, mplayer, tvtime and mencoder to play
and record video and audio.

%description -l pl
Freevo to linuksowa aplikacja zamieniaj±ca PC z kart± telewizyjn±
i/lub wyj¶ciem TV-out na samodzieln± multimedialn± szafê graj±c± /
magnetowid. Jest zbudowana w oparciu o inne aplikacje, takie jak
xine, mplayer, tvtime i mencoder s³u¿±ce do odtwarzania i nagrywania
obrazu i d¼wiêku.

%package boot
Summary:	Files to enable a standalone Freevo system (started from initscript)
Summary(pl):	Pliki do w³±czania samodzielnego systemu Freevo (uruchamiane z initscriptów)
Group:		Applications/Multimedia
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description boot
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as mplayer and mencoder to play and record
video and audio.

Note: This installs the initscripts necessary for a standalone Freevo
system.

%description boot -l pl
Freevo to linuksowa aplikacja zamieniaj±ca PC z kart± telewizyjn±
i/lub wyj¶ciem TV-out na samodzieln± multimedialn± szafê graj±c± /
magnetowid. Jest zbudowana w oparciu o inne aplikacje, takie jak
xine, mplayer, tvtime i mencoder s³u¿±ce do odtwarzania i nagrywania
obrazu i d¼wiêku.

Ten pakiet instaluje skrypty inicjalizuj±ce potrzebne do samodzielnego
systemu Freevo.

%prep
%setup -q

find . -name CVS | xargs rm -rf
find . -name ".cvsignore" |xargs rm -f
find . -name "*.pyc" |xargs rm -f
find . -name "*.pyo" |xargs rm -f
find . -name "*.py" |xargs chmod 644

%build
env CFLAGS="%{rpmcflags}" \
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--record=INSTALLED_FILES

install local_conf.py.example $RPM_BUILD_ROOT%{_docdir}

install -d $RPM_BUILD_ROOT%{_datadir}/freevo/contrib/lirc
cp -av contrib/lirc $RPM_BUILD_ROOT%{_datadir}/freevo/contrib
mkdir -p %{buildroot}%{_sysconfdir}/freevo
## The following is needed to let RPM know that the files should be backed up
touch %{buildroot}%{_sysconfdir}/freevo/freevo.conf
#
## boot scripts
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_bindir}
install -m 755 boot/freevo %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 boot/freevo_dep %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 boot/recordserver %{buildroot}%{_sysconfdir}/rc.d/init.d/freevo_recordserver
install -m 755 boot/webserver %{buildroot}%{_sysconfdir}/rc.d/init.d/freevo_webserver
install -m 755 boot/recordserver_init %{buildroot}%{_bindir}/freevo_recordserver_init
install -m 755 boot/webserver_init %{buildroot}%{_bindir}/freevo_webserver_init
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/freevo/boot_config
#
#
mkdir -p %{buildroot}/var/log/freevo
mkdir -p %{buildroot}/var/cache/freevo
mkdir -p %{buildroot}/var/cache/freevo/{thumbnails,audio}
mkdir -p %{buildroot}/var/cache/xmltv/logos
chmod 777 %{buildroot}/var/cache/{freevo,freevo/thumbnails,freevo/audio,xmltv,xmltv/logos}
chmod 777 %{buildroot}/var/log/freevo

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Remember to run 'freevo setup' after installing!"

%post boot
# Add the service, but don't automatically invoke it
# user has to enable it via ntsysv
/sbin/chkconfig --add freevo
/sbin/chkconfig --levels 234 freevo off
#/sbin/chkconfig --add freevo_dep
/sbin/chkconfig --add freevo_recordserver
/sbin/chkconfig --levels 234 freevo_recordserver off
/sbin/chkconfig --add freevo_webserver
/sbin/chkconfig --levels 234 freevo_webserver off

%preun boot
if [ "$1" = 0 ] ; then
	/sbin/chkconfig --del freevo
#	/sbin/chkconfig --del freevo_dep
	/sbin/chkconfig --del freevo_recordserver
	/sbin/chkconfig --del freevo_webserver
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog FAQ INSTALL README TODO Docs local_conf.py.example
%doc contrib/lirc
%{_docdir}/local_conf.py.example
%attr(755,root,root) %{_bindir}/*
#%dir %{_docdir}/installation
#%dir %{_docdir}/plugin_writing
%dir %{_datadir}/freevo
%{_datadir}/freevo/*
%dir %{_datadir}/freevo/contrib
%dir %{_datadir}/freevo/contrib/fbcon
%dir %{_datadir}/freevo/contrib/lirc
%{_datadir}/freevo/contrib/lirc/*
%dir %{_sysconfdir}/freevo
%attr(1777,root,root) %dir /var/log/freevo
%attr(1777,root,root) %dir /var/cache/freevo
%attr(1777,root,root) %dir /var/cache/freevo/audio
%attr(1777,root,root) %dir /var/cache/freevo/thumbnails
%attr(1777,root,root) %dir /var/cache/xmltv
%attr(1777,root,root) %dir /var/cache/xmltv/logos
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freevo/freevo.conf
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freevo/record_config.py
%{py_sitescriptdir}/freevo
# ??? DUP
#%{_datadir}/freevo
%dir %{_datadir}/fxd
%{_datadir}/fxd/webradio.fxd

%files boot
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/freevo_*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freevo/boot_config
