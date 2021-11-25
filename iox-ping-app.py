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

def dest_ping(ip_address):
   result = False
   output = subprocess.Popen(['ping', '-n', '-c', '2', '-w', '2', str(ip_address)],
				stdout=subprocess.PIPE).communicate()[0]
   if "2 packets received, 0% packet loss" in output.decode('utf-8'):
      result = True
   return(result)

"""
   returns the local AP time 
   try with : curl http://<AP IP@>:<SERVICEPORT>/time 
"""
@route('/time')
def time():
   current_time = datetime.now().isoformat(' ')
   return {"system": 1, "datetime": current_time}

"""
   returns the string <string_id> given in the URL 
   try with : curl http://<AP IP@>:<SERVICEPORT>/status/blah 
"""
@route('/status/<string_id>')
def status(string_id):
   return { "system": 1, "device": str(string_id) }

"""
   pings the IP@ given in the URL and returns (Un)Reachable 
   try with : curl http://<AP IP@>:<SERVICEPORT>/ping/<any IP@>
"""
@route('/ping/<ip_address>')
def status(ip_address):
   ip_address = str(ip_address)
   if dest_ping(ip_address):
      return { "ping": "Reachable", "ip_address": ip_address }
   else:
      return { "ping": "Unreachable", "ip_address": ip_address }


run(host='0.0.0.0', port=SERVICEPORT)
