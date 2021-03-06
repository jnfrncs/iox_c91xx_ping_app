# iox_c91xx_ping_app
Simple app to install and run as an IOX container on a Cisco C9120-30 AP

reference : Devnet : https://developer.cisco.com/docs/app-hosting-ap/

Below cmds : run them inside the IOX VM (see Devnet ref), or equivalent (docker + ioxclient)
# 
Copyright 11/2021 Cisco Systems /  jpujol@cisco.com
#
STEP 1: 

docker build -t iox_ping_app .
 
STEP2:

mkdir -p package.dir

cp package.yaml package.dir/

sudo ioxclient docker package -p ext2 -r -1 iox_ping_app ./package.dir/

#
Import the package.tar file (should be less than 20Mb) into DNAC as an IOX app, or 
deploy it directly into the AP using ioxclient. 

In case of a direct upload by using ioxclient, the file activation.json is required to define the NAT/PAT option in the networking stack between the AP and the container.

ioxclient --profile AP9120I.5130 application install iox_basic_app package.dir/package.tar

ioxclient --profile AP9120I.5130 application activate iox_basic_app --payload activation.json

ioxclient --profile AP9120I.5130 application start iox_basic_app 

#

In case you are really impatient, do not build the package yourself, you can import the "package.tar" file provided here directly into DNAC app repository  (Provision -> IOT Services), or by the ioxclient manual process.

# 

Multiple calls to this application on a set of APs can be initiated from the iox_dping_srv_app (parallel calls and statistics)
see https://github.com/jnfrncs/iox_dping_srv_app

# test it : 

From your web navigator or curl : http://<AP IP>:8010/help 
 	
help	
 
/ping/help	"This help"
 
/ping/time	"returns the container local time"
 
/ping/<target IP@>	"ping target IP@"
 
/ping/<target IP@>/size/<packet size>	"ping target IP@ (w/ packet size)"

/ping/<target IP@>/ttl/<TTL value>	"ping target IP@ (w/ TTL value) "
