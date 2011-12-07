Name: esc 
Version: 1.1.0
Release: 21%{?dist} 
Summary: Enterprise Security Client Smart Card Client
License: GPL+
URL: http://directory.fedora.redhat.com/wiki/CoolKey 
Group: Applications/Internet

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Fix to build against XUlrunner SDK.
Patch1: esc-1.1.0-fix1.patch
#Fix to the smart card handling thread.
Patch2: esc-1.1.0-fix2.patch
#Simple fix to some smart card error messages.
Patch3: esc-1.1.0-fix3.patch
#Add -fno-strict-aliasing compile flag.
Patch4: esc-1.1.0-fix4.patch
#Fix error with reporting a certain smart card error message.
Patch5: esc-1.1.0-fix5.patch
#Allow the http library the ability to observe security exceptions for incoming server certs.
Patch6: esc-1.1.0-fix6.patch
#Ipv6 support for the http library.
Patch7: esc-1.1.0-fix7.patch
#Observe arrow keys in the UI and attach webprogress listener to loading external
#esc UI.
Patch8: esc-1.1.0-fix8.patch
#Fix crash issue when clicking on the tray icon.
Patch9: esc-1.1.0-fix9.patch
#Back out of the webprogress listener fix.
Patch10: esc-1.1.0-fix10.patch
#Minor fix to arrow key support and CAC card handling.
Patch11: esc-1.1.0-fix11.patch
#Minor fix to build with latest Xulrunner SDK.
Patch12: esc-1.1.0-fix12.patch
#Minor fix to #469867, Cannot use arrow keys to move between cards.
Patch13: esc-1.1.0-fix13.patch
#Another minor fix to #469867, Cannot use arrow keys to move between cards.
Patch14: esc-1.1.0-fix14.patch
#A fix to #582283 - ESC Enrollment of formatted card fails when more than one card present in usb.
Patch15: esc-1.1.0-fix15.patch
#A fix to #582833 - ESC already running error message when user logs out and log in.
Patch16: esc-1.1.0-fix16.patch

BuildRequires: doxygen fontconfig-devel freetype-devel >= 2.1
BuildRequires: glib2-devel libIDL-devel atk-devel gtk2-devel libjpeg-devel
BuildRequires: pango-devel libpng-devel pkgconfig zlib-devel
BuildRequires: nspr-devel nss-devel
BuildRequires: autoconf213 libX11-devel libXt-devel
BuildRequires: xulrunner xulrunner-devel

BuildRequires: pcsc-lite-devel coolkey-devel
BuildRequires: desktop-file-utils zip binutils libnotify-devel
BuildRequires: dbus-devel
Requires: pcsc-lite  coolkey nss nspr
Requires: zip dbus >= 0.90 libnotify >= 0.4.2
Requires: xulrunner

# 390 does not have coolkey or smartCards
ExcludeArch: s390 s390x 

# We can't allow the internal xulrunner to leak out
AutoReqProv: 0

#%define __prelink_undo_cmd %{nil}
%define escname %{name}-%{version}
%define escdir %{_libdir}/%{escname}
%define escbindir %{_bindir}
%define esc_chromepath   chrome/content/esc
%define appdir applications
%define icondir %{_datadir}/icons/hicolor/48x48/apps
%define esc_vendor esc 
%define autostartdir %{_sysconfdir}/xdg/autostart
%define pixmapdir  %{_datadir}/pixmaps
%define docdir    %{_defaultdocdir}/%{escname}
%define escappdir src/app/xpcom
%define escxuldir src/app/xul/esc
%define escxulchromeicons %{escxuldir}/chrome/icons/default
%define escdaemon escd


Source0: http://pki.fedoraproject.org/pki/sources/%name/%{escname}.tar.bz2
Source1: esc
Source2: esc.desktop
Source3: esc.png


%description
Enterprise Security Client allows the user to enroll and manage their
cryptographic smartcards.

%prep

%setup -q -c -n %{escname}

#patch esc 

%patch1 -p1 -b .fix1
%patch2 -p1 -b .fix2
%patch3 -p1 -b .fix3
%patch4 -p1 -b .fix4
%patch5 -p1 -b .fix5
%patch6 -p1 -b .fix6
%patch7 -p1 -b .fix7
%patch8 -p1 -b .fix8
%patch9 -p1 -b .fix9
%patch10 -p1 -b .fix10
%patch11 -p1 -b .fix11
%patch12 -p1 -b .fix12
%patch13 -p1 -b .fix13
%patch14 -p1 -b .fix14
%patch15 -p1 -b .fix15
%patch16 -p1 -b .fix16

%build

GECKO_SDK_PATH=%{_libdir}/xulrunner-sdk-1.9.2/sdk
GECKO_BIN_PATH=%{_libdir}/xulrunner-1.9.2
GECKO_INCLUDE_PATH=%{_includedir}/xulrunner-sdk-1.9.2

%ifarch x86_64 ppc64 ia64
USE_64=1
export USE_64
%endif

export GECKO_SDK_PATH
export GECKO_BIN_PATH
export GECKO_INCLUDE_PATH
# last setup call moved  the current directory

cd esc 
#cd ../..

cp %{SOURCE3} %{escxuldir}/%{esc_chromepath}
rm -f %{escxulchromeicons}/*.ico
cp %{escxulchromeicons}/esc-window.xpm %{escxulchromeicons}/default.xpm

make BUILD_OPT=1 HAVE_LIB_NOTIFY=1 ESC_VERSION=%{version}-%{release} USE_XUL_SDK=1

%install

cd esc/src/app/xpcom 

mkdir -p $RPM_BUILD_ROOT/%{escbindir}
mkdir -p $RPM_BUILD_ROOT/%{icondir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{autostartdir}
mkdir -p $RPM_BUILD_ROOT/%{pixmapdir}
mkdir -p $RPM_BUILD_ROOT/%{docdir}


sed -e 's;\$LIBDIR;'%{_libdir}';g'  %{SOURCE1} > $RPM_BUILD_ROOT/%{escbindir}/%{name}


chmod 755 $RPM_BUILD_ROOT/%{escbindir}/esc

mkdir -p $RPM_BUILD_ROOT/%{escdir}

%ifarch x86_64 ppc64 ia64
USE_64=1
export USE_64
%endif


make BUILD_OPT=1 USE_XUL_SDK=1 install DESTDIR=$RPM_BUILD_ROOT/%{escdir}

rm -rf $RPM_BUILD_ROOT/%{escdir}/usr

cd ../../../dist/*OPT*/esc_build/esc

cp %{esc_chromepath}/esc.png $RPM_BUILD_ROOT/%{icondir}
ln -s $RPMBUILD_ROOT%{icondir}/esc.png $RPM_BUILD_ROOT/%{pixmapdir}/esc.png

cp %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/%{appdir}
cp %{SOURCE2} $RPM_BUILD_ROOT/%{autostartdir}

cd %{_builddir}
cp %{escname}/esc/LICENSE $RPM_BUILD_ROOT/%{docdir}

chmod 755 -R $RPM_BUILD_ROOT/%{escdir}/chrome
chmod 755 -R $RPM_BUILD_ROOT/%{escdir}/defaults
chmod 755  $RPM_BUILD_ROOT/%{escdir}/application.ini


%clean

rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

%{escdir}/esc
%{escdir}/escd
%{escbindir}/esc
%{escdir}/application.ini

%{escdir}/chrome/chrome.manifest

%{escdir}/chrome/content
%{escdir}/chrome/locale
%{escdir}/chrome/icons/default
%{escdir}/components

%{escdir}/defaults/preferences/esc-prefs.js   

#%{escdir}/xulrunner
%{icondir}/esc.png
%{pixmapdir}/esc.png
%{autostartdir}/esc.desktop
%{_datadir}/%{appdir}/esc.desktop
%doc %{docdir}/LICENSE

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%preun

killall --exact -q escd
exit 0

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%changelog
* Mon Apr 26 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-21
- Related: #582833 - ESC already running error message when user logs out and logs in.
* Fri Apr 23 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-20
- Resolves: #582283 - ESC Enrollment of formatted card fails when more than one card present in usb.
* Tue Apr 06 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-19
- Resolves: #469867 Cannot use arrow keys to move between cards.
* Tue Mar 30 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-18
- Resolves: #469867 Cannot use arrow keys to move between cards.
* Thu Mar 11 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-17
- Resolves: #556657 Enroll button active for an enrolled CAC card.
- Resolves: #469867 Cannont use arrow keys to move between cards.
* Mon Mar 08 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-16
- Resolves: #556641.
* Tue Mar 02 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-15
- Resolves: #568514. ESC crashed after leaving computer untouched.
* Tue Jan 26 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-14
- Resolves: #556639 #556657 #556641 #469867 #469233.
* Mon Jan 18 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-13
- Rebuild without ifd-egate dependency.
* Thu Jan 14 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-12
- Rebuild with correct license in spec.
* Fri Jan 08 2010  Jack Magne <jmagne@redhat.com>= 1.1.0-11
- Rebuild with tarball from URL.
* Tue Sep 15 2009  Jack Magne <jmagne@redhat.com>= 1.1.0-10
- Pick up latest changes.
* Mon Jun 22 2009  Jack Magne <jmagne@redhat.com>= 1.1.0-9
- Related: #496410, also IPV6 support.
* Fri Jun 19 2009  Jack Magne <jmagne@redhat.com>= 1.1.0-8
- Related: #496410, SSL Conn fix.
* Mon Jun 8  2009  Jack Magne <jmagne@redhat.com>- 1.1.0-7
- Releated: #496410.
* Thu Apr 23 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-6
- Related: #496410. Appease rpmdiff.
* Wed Apr 22 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-5
- Related: #496410, addresses 494981, better error message.
* Wed Apr 22 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-4
- Move to latest rebased code. Related #496410.
* Thu Dec 04 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-39
- Resolves #469202 - Cert Viewer issue              
* Tue Nov 11 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-38
- Resolves  #471923 - ESC Connection issue.
* Thu Oct 16 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-37
- Resolves #467126 - Blank authentication dialog problem. 
* Fri Sep 26 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-36
- Related #200475 - Require the xulrunner package, Resolves #248493
* Thu Sep 18 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-35
- Related 200475, make rpmdiff tests happy.
* Tue Sep 16 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-34
- Resolves #200475 #253081 #437238
* Thu Jan 10 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-33
- Resolves #25324a8 #253268
* Thu Jul 12 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-32
- Resolves #248071 - ESC RPM unistall failure if daemon not running.
* Fri Jun 22 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-31
- Related #208038 - Top things to put in diagnostics log
* Wed Jun 20 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-30
- Related #204021
* Fri Jun 8 2007   Jack Magne <jmagne@redhat.com>- 1.0-0-29
- Related #212010
* Fri Jun 8 2007   Jack Magne <jmagne@redhat.com>- 1.0.0-28
- Resolves #212010 
* Tue Jun 5 2007   Jack Magne <jmagne@redhat.com>- 1.0.0-27 
- Resolves #203466 Better error message strings.
* Mon May 21 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-26
- Related: #206783 Fix the launcher script to work with new logging.
* Fri May 11 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-25
- Resolves: #206783.
* Mon Apr 23 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-24
- More Desktop appearance fixes.
- Related: #208749
* Mon Apr 23 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-23
- Desktop appearance fixes.
- Related: #208749
* Thu Apr 19 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-22
- Second drop of 5.1 fixes.
- Resolves: #203934, #203935, #204959, #206780, #206792, #207721
- Resolves: #207816, #206791
- Related:  #208749
* Wed Apr 18 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-21
- First 5.1 fixes.
- Resolves: #203757, #203806, #204661, #205856, #206788, #206791
- Resolves: #208037, #208333, #210589, #210590, #213912, #226913
- Resolves: #204021, #205498, #224436
* Tue Nov 28 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-20
- fix for bug to commit config changes immediately.  Bug #210988
* Wed Nov 15 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-19
-fix for escd double free problem. Bug #209882
* Tue Oct 24 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-18
-rebuilt on RHEL-5 branch
* Sun Oct 4  2006 Jack Magne <jmagne@redhat.com>- 1.0.0-17
- Diagnostics display fixes, Mac and Window fixes.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-16
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-15
- Fix to the build version

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>= 1.0.0-14
- Fix to compile error in daemon

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-13
- Fix to include the new esc daemon.  

* Sat Sep 16 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-12
- Fix for Password Reset and minor UI revision.

* Fri Sep 15 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-11
- Further UI enhancement bug fixes

* Thu Sep 7 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-10
- Further strings revisions.

* Wed Aug 30 2006 Jack Magne <jmagne@redhat.com>-  1.0.0-9
- Revision of the strings used in ESC.

* Sat Aug 27 2006 Jack Magne <jmagne@redhat.com>-  1.0.0-8
- Fixes to get libnotify working properly on FC6 systems.

* Tue Aug 22 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-7
- Fix for bug #203211, use of system NSS and NSPR for
- Xulrunner ,addressing the problem running on 64 bit.
- Overwriting 5 and 6 due to important bug #203211.

* Fri Aug  18 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-6
- Correct problem with Patch #6

* Tue Aug  17 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-5
- Build ESC's xulrunner component using system nss and nspr
- Build process creates run script based on {_libdir} variable,
  accounting for differences on 64 bit machines.
- UI enhancements

* Tue Aug  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.0-4
- Don't auto-generate requires either

* Mon Jul 31 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.0-3
- Don't provide mozilla libraries

* Fri Jul 28 2006 Ray Strode <rstrode@redhat.com> - 1.0.0-2
- remove bogus gtk+ requires (and some others that will
  be automatic)

* Tue Jun 13 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-1
- Initial revision for fedora

