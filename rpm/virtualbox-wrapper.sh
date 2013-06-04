#!/bin/bash
export QT_NO_KDE_INTEGRATION=1
/usr/bin/id -nG | grep -v -e "root" -e "vboxusers" >/dev/null && /usr/lib/virtualbox/VBoxPermissionMessage && exit
LD_LIBRARY_PATH="/usr/lib/virtualbox${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" /usr/lib/virtualbox/VirtualBox $@
