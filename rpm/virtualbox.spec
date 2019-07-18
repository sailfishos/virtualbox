#
# spec file for package virtualbox
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           virtualbox
#BuildRequires:  acpica
#BuildRequires:  dmidecode
BuildRequires:  fdupes
BuildRequires:  sed
#BuildRequires:  glibc-devel-static
#gsoap,libopenssl and java needed for building webservice
#BuildRequires:  gsoap-devel
#BuildRequires:  java-devel >= 1.6.0
#BuildRequires:  libgsoap-devel
BuildRequires:  pkgconfig(openssl)
##
#BuildRequires:  LibVNCServer-devel
#BuildRequires:  SDL-devel
#BuildRequires:  bin86
BuildRequires:  boost-devel
#BuildRequires:  dev86
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  kernel-adaptation-pc >= 5.0.21
BuildRequires:  kernel-adaptation-pc-devel >= 5.0.21
%define kernel_rpm_version %{expand:%(rpm -q --qf '[%%{version}-%%{release}]' kernel-adaptation-pc-devel)}
%define kernel_version %{lua:print((rpm.expand("%{kernel_rpm_version}"):gsub("\+.+-", "-")))}
BuildRequires:  kbuild
#BuildRequires:  kernel-syms
BuildRequires:  libcap-devel
BuildRequires:  libcurl-devel
#BuildRequires:  libidl-devel
#BuildRequires:  libqt4-devel
BuildRequires:  libxslt-devel
BuildRequires:  module-init-tools
#BuildRequires:  pam-devel
BuildRequires:  pulseaudio-devel
BuildRequires:  python-devel
BuildRequires:  quilt
BuildRequires:  udev
#BuildRequires:  update-desktop-files
#BuildRequires:  xorg-x11
#BuildRequires:  xorg-x11-devel
#BuildRequires:  xorg-x11-server
#BuildRequires:  xorg-x11-server-sdk
BuildRequires:  yasm
#BuildRequires:  zlib-devel-static
# and just for the macro:
BuildRequires:   systemd

Version:        5.2.30
Release:        1
Summary:        VirtualBox is an Emulator
License:        GPL-2.0+
Group:          System/Emulators/PC
Url:            http://www.virtualbox.org/

Source0:        %{name}-%{version}.tar.bz2
Source2:        %{name}-60-vboxdrv.rules
Source3:        %{name}-60-vboxguest.rules
Source4:        %{name}-default.virtualbox
Source5:        %{name}-host-kmp-files
Source6:        %{name}-guest-kmp-files
Source7:        %{name}-host-preamble
Source8:        %{name}-guest-preamble
Source9:        %{name}-wrapper.sh
Source10:       %{name}-LocalConfig.kmk
# init script to start virtual boxes during boot, to be configured via /etc/sysconfig/vbox bnc#582398
Source12:       %{name}-vboxes
Source13:       %{name}-sysconfig.vbox
# added by lbt as the Mer systemd service
Source14:       vboxservice.service
Source98:       rpmlintrc
Source99:       virtualbox.changes_suse
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#PreReq:         pwdutils permissions
Requires:       %{name}-host-kmp = %version
#rename from ose version:
Provides:       %{name}-ose = %version
Obsoletes:      %{name}-ose < %version
#PreReq:         sysvinit(syslog)

%description
VirtualBox is an extremely feature rich, high performance product
for enterprise customers, it is also the only professional solution
that is freely available as Open Source Software under the terms of the
GNU Public License (GPL).
##########################################
%package guest-modules
Summary:        Guest kernel modules for VirtualBox
Group:          System/Emulators/PC
Requires:	kernel-adaptation-pc == %{kernel_rpm_version}

%description guest-modules
This package contains the kernel-module for VirtualBox.
##########################################
%package guest-x11
Summary:        VirtualBox X11 drivers for mouse and video
Group:          System/X11/Servers/XF86_4
Requires:       %{name}-guest-modules = %version
#Supplements:    modalias(pci:v000080EEd0000BEEFsv*sd*bc*sc*i*)

%description guest-x11
VirtualBox
This package contains X11 guest utilities and X11 guest mouse and video drivers
###########################################
%package guest-tools
Summary:        VirtualBox guest tools
Group:          System/Emulators/PC
Requires:       %{name}-guest-modules = %version
#Supplements:    modalias(pci:v000080EEd0000BEEFsv*sd*bc*sc*i*)

%description guest-tools
VirtualBox guest addition tools.
###########################################
%prep
# version may contain a +, and virtualbox refuses to build with that in the path
# so change the buildsubdir to be different from what's in the tarfile
# Special care must be taken to preserve compatibility with both OBS and mb2
%setup -q -c -n %{name}/%{name}
mv %{name}-%{version}/%{name}/* . ||:

#copy kbuild config
%__cp %{S:10} LocalConfig.kmk
%__cp %{S:14} vboxservice.service 
#
##########################
####workaround kmk_sed --v
#instead of kmk_sed use /usr/bin/sed because of bug http://svn.netlabs.org/kbuild/ticket/112, 
#but we have to create wrapper which will handle --append and --outpout options which are not provided by /usr/bin/sed
cat >> kmk_sed <<EOF
#!/bin/bash
while [ "\$#" != "0" ]; do
	pass=\${pass}" \$1"
	[ "\$1" == "-e" ] && shift && pass=\${pass}" '\$1'"
	shift
done
eval "sed \$(echo "\$pass" | sed -e "s/--output=/>/g;s/--append=/>/g;s/--output/>/g;s/--append/>>/g");"
EOF
chmod +x ./kmk_sed
echo "SED = $(readlink -f ./kmk_sed)"  >> LocalConfig.kmk
####workaround kmk_sed --^
##########################
#
%build
#	--disable-kmods		don't build Linux kernel modules -  but use SUSE specific way see few lines under
#	--nofatal		try to avoid build fail caused by missing makeself package
./configure \
	--enable-vnc \
	--enable-vde \
	--disable-kmods \
	--disable-java \
	--disable-docs \
	--nofatal \
	--enable-webservice

# configure actually warns we should source env.sh (which seems like it could influence the build...)
source env.sh

#
#  	VBOX_PATH_PACKAGE_DOCS set propper path for link to pdf in .desktop file
# 	VBOX_WITH_REGISTRATION_REQUEST= VBOX_WITH_UPDATE_REQUEST= just disable some functionality in gui

echo "build basic parts"
/usr/bin/kmk %{?_smp_mflags} VBOX_GCC_WERR= KBUILD_VERBOSE=2 VBOX_WITH_REGISTRATION_REQUEST= VBOX_WITH_UPDATE_REQUEST= TOOL_YASM_AS=yasm VBOX_PATH_PACKAGE_DOCS=/usr/share/doc/packages/virtualbox VBOX_ONLY_ADDITIONS=1 mount VBoxControl VBoxService


# build kernel modules for guest and host (check novel-kmp package as example)
# host  modules : vboxdrv,vboxnetflt,vboxnetadp
# guest modules : vboxguest,vboxsf,vboxvideo
echo "build kernel modules"

mkdir -p modules_build_dir
src/VBox/Additions/linux/export_modules.sh modules_build_dir/modules.tar.gz
pushd modules_build_dir
tar xf modules.tar.gz
KERN_DIR=/usr/src/kernels/%{kernel_version} KERN_VER=%{kernel_version} make
popd


%install
#################################
echo "create directory structure"
#################################
%__install -d -m 755 %{buildroot}%{_bindir}
%__install -d -m 755 %{buildroot}/sbin

####################################################################################
echo "entering virtualbox-modules-guest and virtualbox-modules-host install section"
####################################################################################
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=vbox
# Feel free to find a better solution:
KERNEL_DIR=/usr/src/kernels/%{kernel_version}
# -M doesn't work if it ends in "/." :/
for module_name in modules_build_dir/*/.
do
    %__make -C $KERNEL_DIR modules_install M=$(dirname $PWD/$module_name)
    if [ ! -f "$INSTALL_MOD_PATH"/lib/modules/*/vbox/$(basename $(dirname $module_name)).* ]
    then
        echo "Failed to build $module_name"
        exit 1
    fi
done
# Clean up spurious stuff
rm -f %{buildroot}/lib/modules/*/modules.*

# Remove vboxvideo which is not needed with new kernel
rm -f %{buildroot}/lib/modules/*/vbox/vboxvideo.ko

###########################################
echo "entering guest-tools install section"
###########################################
%__install -m 755 out/linux.*/release/bin/additions/VBoxControl  %{buildroot}%{_bindir}/VBoxControl
%__install -m 755 out/linux.*/release/bin/additions/VBoxService  %{buildroot}%{_bindir}/VBoxService
%__install -m 755 out/linux.*/release/bin/additions/mount.vboxsf %{buildroot}/sbin/mount.vboxsf

###########################################
echo "entering systemd install section"
###########################################
%__install -d -m 755  %{buildroot}%{_unitdir}/basic.target.wants/
%__install -m 644 vboxservice.service  %{buildroot}%{_unitdir}/vboxservice.service
ln -sf ../vboxservice.service %{buildroot}%{_unitdir}/basic.target.wants/


%post guest-modules
# depmod for kernel we require
depmod -a %{kernel_version}
# Create a group for accessing automounted vbox sf folders
groupadd -r vboxsf || true

%files guest-tools
%defattr(-, root, root)
%{_bindir}/VBoxControl
%{_bindir}/VBoxService
/sbin/mount.vboxsf
%{_unitdir}/vboxservice.service
%{_unitdir}/basic.target.wants/vboxservice.service

%files guest-modules
%defattr(-, root, root)
/lib/modules/*/vbox
