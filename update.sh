#!/bin/bash

. "/etc/os-release"

LS_USER=""
LS_LOC=""

if [[ "$ID_LIKE" = "debian" ]]; then
	echo "Copying /var/log/auth.log"
	sudo cp /var/log/auth.log "$LS_LOC/auth.log"
elif [[ "$ID_LIKE" = "rhel fedora" ]]; then
	echo "Copying /var/log/secure"
	sudo cp /var/log/secure "$LS_LOC/auth.log"
fi

cd "$LS_LOC"
chown $LS_USER:$LS_USER "$LS_LOC/auth.log"

sudo -u "$LS_USER" python get_stats.py