from cwatchAPI import *
from xml.etree import ElementTree
import time
import sys
import string
import os
import argparse


usage = "GetReportsCW -u user -p passw -c client"
parser = argparse.ArgumentParser(description="Get CWatch Reports for a client",epilog=usage)
parser.add_argument("-u","--user",help="Username",type=str,required=True)
parser.add_argument("-p","--passw",help="Password",type=str,required=True)
parser.add_argument("-c","--client",help="Client",type=str,required=True)
opt = parser.parse_args()
if len(sys.argv) < 3:
   parser.print_help()
   sys.exit()

'''
Get All Reports for Client
'''

data = cwatchAPI(opt.user,opt.passw)
key = []
report = data.getPreReport(opt.client)
for i in report:
    jid = i["id"]
    for b in i["seq"]:
        nkey = data.getReportQueue(jid,b["id"])
        key.append(nkey)
done = 0

os.system('clear')
print "------------------------------------"
print "Getting %s of xml reports" % len(key)
print "------------------------------------"
for i in key:
    while 1:
        nd = data.getReport(i)
        if "Processing" in nd:
            sys.stdout.write("%s" % "*")
            sys.stdout.flush()
            time.sleep(1)
        else:
            print "\n"
            output = "%s-%s-%s.xml" % (opt.client,done,time.strftime("%m-%d-%Y"))
            print "Writing XML Report: %s" % output
            f = open(output,'w')
            f.write(nd)
            break
    done += 1

