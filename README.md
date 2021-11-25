# iox_c91xx_ping_app
Simple app to install and run as an IOX container on a Cisco C9120-30 AP

#
# reference : Devnet : https://developer.cisco.com/docs/app-hosting-ap/
# run inside the IOX VM , or equivalent (docker + ioxclient)
# 
# Copyright 11/2021 Cisco Systems /  jpujol@cisco.com
#
# STEP 1: 
# docker build -t iox-ping-app .
# 
# STEP2:
# mkdir -p package.dir
# cp package.yaml package.dir/
# sudo ioxclient docker package -p ext2 -r -1 iox-ping-app ./package.dir/
#
# Import the package.tar file (should be less than 20Mb) into DNAC as an IOX app, or 
# deploy it directly into the AP using ioxclient. 
