Summary:	Freevo - open-source home theatre PC platform
Summary(pl.UTF-8):	Freevo - zestaw kina domowego oparty na platformie PC i otwartych źródłach
Name:		freevo
Version:	1.7.2
Release:	3
License:	GPL
Group:		Applications/Multimedia
Source0:	http://dl.sourceforge.net/freevo/%{name}-%{version}.tar.gz
# Source0-md5:	1c05c080cd89d70e07e393f74aaa1730
Source1:	%{name}-boot_config
Patch0:		%{name}-setup.py-elementtree.patch
Patch1:		%{name}-xmltv.py.patch
URL:		http://freevo.sourceforge.net/
BuildRequires:	python-BeautifulSoup
BuildRequires:	python-PIL >= 1.1.4
BuildRequires:	python-TwistedCore >= 2.0.1-1
BuildRequires:	python-TwistedWeb
BuildRequires:	python-devel
BuildRequires:	python-elementtree
BuildRequires:	python-kaa-imlib2
BuildRequires:	python-kaa-metadata
BuildRequires:	python-mmpython >= 0.4.9
BuildRequires:	python-pygame >= 1.5.6
BuildRequires:	python-libxml2
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-libs
Requires:	aumix >= 2.8
Requires:	lsdvd
Requires:	mplayer
Requires:	python-Numeric
Requires:	python-PIL >= 1.1.4
Requires:	python-TwistedWeb
Requires:	python-kaa-metadata
Requires:	python-kaa-imlib2
Requires:	python-mmpython >= 0.4.9
Requires:	python-numpy
Requires:	python-pygame >= 1.5.6
#Suggests:	tvtime
#Suggests:	xine-ui
#Suggests:	xmltv
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as xine, mplayer, tvtime and mencoder to play
and record video and audio.

%description -l pl.UTF-8
Freevo to linuksowa aplikacja zamieniająca PC z kartą telewizyjną
i/lub wyjściem TV-out na samodzielną multimedialną szafę grającą /
magnetowid. Jest zbudowana w oparciu o inne aplikacje, takie jak xine,
mplayer, tvtime i mencoder służące do odtwarzania i nagrywania obrazu
i dźwięku.

%package boot
Summary:	Files to enable a standalone Freevo system (started from initscript)
Summary(pl.UTF-8):	Pliki do włączania samodzielnego systemu Freevo (uruchamiane z initscriptów)
Group:		Applications/Multimedia
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description boot
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as mplayer and mencoder to play and record
video and audio.

Note: This installs the initscripts necessary for a standalone Freevo
system.

%description boot -l pl.UTF-8
Freevo to linuksowa aplikacja zamieniająca PC z kartą telewizyjną
i/lub wyjściem TV-out na samodzielną multimedialną szafę grającą /
magnetowid. Jest zbudowana w oparciu o inne aplikacje, takie jak xine,
mplayer, tvtime i mencoder służące do odtwarzania i nagrywania obrazu
i dźwięku.

Ten pakiet instaluje skrypty inicjalizujące potrzebne do samodzielnego
systemu Freevo.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

find . -name CVS | xargs rm -rf
find . -name ".cvsignore" | xargs rm -f
find . -name "*.pyc" | xargs rm -f
find . -name "*.pyo" | xargs rm -f
find . -name "*.py" | xargs chmod 644

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/freevo
## The following is needed to let RPM know that the files should be backed up
touch $RPM_BUILD_ROOT%{_sysconfdir}/freevo/freevo.conf
#
## boot scripts
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_bindir}
install boot/freevo $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install boot/freevo_dep $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install boot/recordserver $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/freevo_recordserver
install boot/webserver $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/freevo_webserver
install boot/recordserver_init $RPM_BUILD_ROOT%{_bindir}/freevo_recordserver_init
install boot/webserver_init $RPM_BUILD_ROOT%{_bindir}/freevo_webserver_init
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/freevo/boot_config
#
#
install -d $RPM_BUILD_ROOT/var/log/freevo
install -d $RPM_BUILD_ROOT/var/cache/freevo
install -d $RPM_BUILD_ROOT/var/cache/freevo/{thumbnails,audio}
install -d $RPM_BUILD_ROOT/var/cache/xmltv/logos

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	echo "Remember to run 'freevo setup' after installing!"
fi

%post boot
# Add the service, but don't automatically invoke it
# user has to enable it via ntsysv
/sbin/chkconfig --add freevo
/sbin/chkconfig --level 234 freevo off
#/sbin/chkconfig --add freevo_dep
/sbin/chkconfig --add freevo_recordserver
/sbin/chkconfig --level 234 freevo_recordserver off
/sbin/chkconfig --add freevo_webserver
/sbin/chkconfig --level 234 freevo_webserver off

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
%attr(755,root,root) %{_bindir}/freevo
#%dir %{_docdir}/installation
#%dir %{_docdir}/plugin_writing
%{_datadir}/freevo
%dir %{_sysconfdir}/freevo
%attr(1777,root,root) %dir /var/log/freevo
%attr(1777,root,root) %dir /var/cache/freevo
%attr(1777,root,root) %dir /var/cache/freevo/audio
%attr(1777,root,root) %dir /var/cache/freevo/thumbnails
%attr(1777,root,root) %dir /var/cache/xmltv
%attr(1777,root,root) %dir /var/cache/xmltv/logos
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/freevo/freevo.conf
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freevo/record_config.py
%{py_sitescriptdir}/freevo
#%dir %{_datadir}/fxd
#%{_datadir}/fxd/webradio.fxd

%files boot
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/freevo_*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/freevo/boot_config
