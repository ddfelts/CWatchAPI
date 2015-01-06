from cwatchAPI import *
from xml.etree import ElementTree
import time
import sys
import string
import os
import argparse


usage = "GetStatsCW -u user -p passw -c client"
parser = argparse.ArgumentParser(description="Get CWatch Stats for a client",epilog=usage)
parser.add_argument("-u","--user",help="Username",type=str,required=True)
parser.add_argument("-p","--passw",help="Password",type=str,required=True)
parser.add_argument("-c","--client",help="Client",type=str,required=True)
opt = parser.parse_args()
if len(sys.argv) < 3:
   parser.print_help()
   sys.exit()

data = cwatchAPI(opt.user,opt.passw)
nodeid = data.getCompanyNodeID(opt.client)
for i in data.apiclientstats(nodeid):
    if opt.client in i["Name"]:
       print "--------------------------------"
       print "Stats for client: %s" % opt.client
       print "Scanned IpAddresses: %s" % i["ScannedIpAddresses"]
       print "Responding IpAddresses: %s" % i["RespondingIpAddresses"]
       print "High: %s" % i["TotalHighs"]
       print "Med: %s" % i["TotalMediums"]
       print "Lows: %s" % i["TotalLows"]
       print "Warnings: %s" % i["TotalWarnings"]
       print "--------------------------------"
       print "Totals: %s" % i["TotalExposures"] 
