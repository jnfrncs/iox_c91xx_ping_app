#
# Small app server running in a container on a Cisco C91xx AP
# to be started from the shell wrapper
#
# Copyright 11/2021 Cisco Systems /  jpujol@cisco.com
# 
#
from bottle import route, run
from datetime import datetime
import subprocess

SERVICEPORT=8010
DFLT_PKT_SIZE=56 # default ICMP packet size
DFLT_TTL=255 # default ICMP TTL

HELPMSG = { "/ping/help" : "This help",
           "/ping/time" : "returns the container local time",
           "/ping/<target IP@>" : "ping target IP@ ",
           "/ping/<target IP@>/size/<packet size>" : "ping target IP@ (w/ packet size) ",
           "/ping/<target IP@>/ttl/<TTL value>" : "ping target IP@ (w/ TTL value) "}

def target_ping(ip_address, size=DFLT_PKT_SIZE, ttl=DFLT_TTL):
   result = False
   output = subprocess.Popen(['ping', '-n', '-c', '2', '-w', '2', '-s', str(size), '-t', str(ttl), str(ip_address)],
                              stdout=subprocess.PIPE).communicate()[0]
   if "2 packets received, 0% packet loss" in output.decode('utf-8'):
      result = True
   return(result)

@route('/help')
def help():
    return { "help" : HELPMSG }
   
"""
   returns the local AP time 
   try with : curl http://<AP IP@>:<SERVICEPORT>/time 
"""
@route('/time')
def time():
   current_time = datetime.now().isoformat(' ')
   return {"system": 1, "datetime": current_time}

"""
   pings the IP@ given in the URL and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>
"""
@route('/ping/<ip_address>')
def ping(ip_address):
   ip_address = str(ip_address)
   if target_ping(ip_address):
      return { "ping": "Reachable", "ip_address": ip_address }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

"""
   pings the IP@ given in the URL (including packet size) and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>/size/<packet size>
"""
@route('/ping/<ip_address>/size/<size>')
def ping_size(ip_address,size):
   ip_address = str(ip_address)
   size = str(size)
   if target_ping(ip_address,size,DFLT_TTL):
      return { "ping": "Reachable", "ip_address": ip_address }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

"""
   pings the IP@ given in the URL (including TTL) and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>/ttl/<TTL value>
"""
@route('/ping/<ip_address>/ttl/<ttl>')
def ping_ttl(ip_address,ttl):
   ip_address = str(ip_address)
   ttl = str(ttl)
   if target_ping(ip_address, DFLT_PKT_SIZE, ttl):
      return { "ping": "Reachable", "ip_address": ip_address }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

run(host='0.0.0.0', port=SERVICEPORT)
