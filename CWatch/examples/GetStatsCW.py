from CWatch.cwatchAPI import *
from cwatchGraph import cwGraph
from cwatchPDF import cwPDF
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

graph = cwGraph()

data = cwatchAPI(opt.user,opt.passw)
nodeid = data.getCompanyNodeID(opt.client)
main = []

for i in data.apiclientstats(nodeid):
    if opt.client in i["Name"]:
       main.append({"title":"High",
                 "data":i["TotalHighs"]})
       main.append({"title":"Med",
                 "data":i["TotalMediums"]})
       main.append({"title":"Lows",
                 "data":i["TotalLows"]})
       main.append({"title":"Warnings",
                 "data":i["TotalWarnings"]})
       scanned = i["ScannedIpAddresses"]
       respond = i["RespondingIpAddresses"]

ndata = {}
ndata["ScannedIpAddresses"] = scanned
ndata["RespondingIpAddresses"] = respond
graph.HBar("Totals",main)
nameit = opt.client + "-CWStats.pdf"
doc = cwPDF(nameit)
doc.setTitle("CriticalWatch Stats")
doc.setDates("01-06-2015","01-06-2015")
doc.setClient(opt.client)
doc.setPortrait()
doc.addStoryTitle("Critical Watch Stats")
#doc.addStory("Scanned IpAddresses: %s" % scanned)
#doc.addStory("Responding IpAddresses: %s" % respond)
doc.addImage("%s/Totals.png" % graph.getDir(),450,200)
doc.addTable(ndata)
doc.savePDF()
graph.removeDir()
sys.exit(1)
