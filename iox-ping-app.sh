#!/bin/sh
#
# Wrapper to launch the python app inside the C91xx container 
# (non blocking and avoid any output to be sent to stdin/stderr
#
# Copyright 11/2021 Cisco Systems /  jpujol@cisco.com
#
/usr/bin/python /iox-ping-app.py >/tmp/iox-ping-app.log 2>&1 &
