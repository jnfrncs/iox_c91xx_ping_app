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

"""
   extracts rtt values from the ping command results, or returns all = 0
"""
def rttValues(pings):
   min = avg = max = 0
   str1 = pings.split("round-trip")
   if len(str1) > 1:
      str2 = str1[1].split()
      if len(str2) >2:
         str3 = str2[2].split('/')
         if len(str3) == 3 :
            min = str3[0]
            avg = str3[1]
            max = str3[2]
   return({ 'min':min, 'avg':avg, 'max':max})

"""
   exec ping command from the container
"""
def target_ping(ip_address, size=DFLT_PKT_SIZE, ttl=DFLT_TTL):
   results = { 'ping': False }
   output = subprocess.Popen(['ping', '-n', '-c', '3', '-w', '2', '-s', str(size), '-t', str(ttl), str(ip_address)],
                              stdout=subprocess.PIPE).communicate()[0]
   if "2 packets received, 0% packet loss" in output.decode('utf-8'):
      results = { 'ping': True , 'stats' : rttValues(output)}
   return(results)

"""
   help message
"""
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
   results = target_ping(ip_address)
   if results['ping'] :
      return { "ping": "Reachable", "ip_address": ip_address , 'stats' : results['stats']}
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

"""
   pings the IP@ given in the URL (including packet size) and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>/size/<packet size>
"""
@route('/ping/<ip_address>/size/<size>')
def ping_size(ip_address,size):
   results = target_ping(ip_address,size,DFLT_TTL)
   if results['ping']:
      return { "ping": "Reachable", "ip_address": ip_address, 'stats' : results['stats'] }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

"""
   pings the IP@ given in the URL (including TTL) and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>/ttl/<TTL value>
"""
@route('/ping/<ip_address>/ttl/<ttl>')
def ping_ttl(ip_address,ttl):
   results = target_ping(ip_address, DFLT_PKT_SIZE, ttl)
   if results['ping']:
      return { "ping": "Reachable", "ip_address": ip_address, 'stats' : results['stats'] }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }

run(host='0.0.0.0', port=SERVICEPORT)
