#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string
import httplib
import urllib2
import StringIO
import time
import datetime
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Domain you want to post to: localhost would be an emoncms installation on your own laptop
# this could be changed to emoncms.org to post to emoncms.org
# Location of emoncms in your server, the standard setup is to place it in a folder called emoncms
# To post to emoncms.org change this to blank: ""

emoncmspath = 'emoncms'

# Write apikey of emoncms account
apikey = '6c1d3709c8767eca32b943f0e89978dc'

# Node id youd like the emontx to appear as
nodeid = 5
conn = httplib.HTTPConnection("192.168.1.3")

test = "200"
global data
global MaxRetry
MaxRetry = 5
def con(MaxRetry):
    print "Get data"
    while (MaxRetry >= 0):
        try:
            r1 = urllib2.urlopen("http://192.168.1.20:80/realtime.csv",timeout = 1 )
            r2 = r1.getcode()
            print r2
            global data
            line = r1.read()
            data = line
            print "Inverter data: ", line
            print "data muutuja", data
            line = line.rstrip()
            data = map(int, line.split(";"))
            print "Print a: ", data
            print "Esimene data:", data[0]
            print "Teine data  :", data[1]
            print "Komas data  :", data[2]
            timestamp = time.strftime("%d:%m:%Y %H:%M:%S", time.gmtime(data[0]))
            print "Timestamp  : ", timestamp
            if r2 == test:
               print "Response Fail_Fail_Fail"
               sleep(5)
               r1.close()
               con(MaxRetry)
            else:
               print "Response OK OK OK"
               sleep(1)
               send()
        except urllib2.URLError as e:
            print (e)
            print ("Ühenduse viga!! Proovin 5 korda veel:"), MaxRetry
            time.sleep(5)
            MaxRetry = MaxRetry - 1
            print ("Connect to Internet and Retry Later ")
            print(" ######--- Closing Connection -- ###### ")
            r1.close()
            exit()

# Remove the new line at the end
#  line = line.rstrip()
# print line

def send():

# Split the line at the whitespaces

    b = ','.join(str(e) for e in data)
    array = b.split(",")
# Create csv string
    ajastamp = str(data[0])
    csv = ",".join(array)
#csv = ','.join(array)
    
    print bcolors.OKBLUE + csv + bcolors.ENDC
# Send to emoncms
    print "Sending data"
    print ('&node=' + str(nodeid) + '&timestamp=' + ajastamp + '&csv=' + csv)
    conn.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&timestamp="+ajastamp+"&csv="+csv)
    conn.close()

while 1:
   sleep(1)
   con(5)
