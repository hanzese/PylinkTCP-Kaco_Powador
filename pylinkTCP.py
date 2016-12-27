import  sys, string
import httplib
import StringIO
import time

from time import sleep
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Domain you want to post to: localhost would be an emoncms installation on you$
# this could be changed to emoncms.org to post to emoncms.org
#domain = "localhost"

# Location of emoncms in your server, the standard setup is to place it in a fo$
# To post to emoncms.org change this to blank: ""
emoncmspath = "emoncms"

# Write apikey of emoncms account
apikey = "6c1d3709c8767eca32b943f0e89978dc"

# Node id youd like the emontx to appear as
nodeid = 5


conn = httplib.HTTPConnection("localhost")
conn1 = httplib.HTTPConnection("192.168.1.20:80")



# Set this to the serial port of your emontx and baud rate, 9600 is standard em$
#ser = serial.Serial('/dev/ttyUSB1', 115200)


while 1:
print "Get data"
  conn1.request("GET", "/realtime.csv")
  r1 = conn1.getresponse()
  sleep (30)
  line = r1.read()

# Remove the new line at the end
  line = line.rstrip()
  conn1.close()
  #print line
  print(bcolors.OKBLUE + line + bcolors.ENDC)

  # Split the line at the whitespaces
  array = line.split(';')

  # Create csv string
  csv = ",".join(array)

  # Send to emoncms

  conn.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&csv="+csv)
  conn.close()
  #sleep (10)
  #response = conn.getresponse()
  #print response.read()
  print "Ootan 40 sekundit"
  sleep (10)
#conn1.close()