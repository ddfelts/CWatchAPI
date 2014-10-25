import os
import string
import sys
import requests
import json
from xml.etree import ElementTree

class cwatchAPI(object):

    def __init__(self,usr,passwd):
        self.sess = requests.session()
        self.url = 'https://www.fusionvm.com/rest/v2/api/'
        self.url2 = 'https://api.fusionvm.com/'
        self.usr = usr
        self.passwd = passwd

    def getData(self,v,url):
        ndata = ""
        if v == "2":
            data = self.sess.get(self.url + url, auth=(self.usr,self.passwd), verify=False)
        if v == "1":
            data = self.sess.get(self.url2 + url)
        for i in data.iter_content(chunk_size=1024):
            if i:
                ndata += i
        return ndata

    def getXml(self,v,url):
        ndata = self.getData(v,url)
        #print ndata
        data = ElementTree.fromstring(ndata)
        return data

    def getJson(self,v,api):
        data = json.loads(self.getData(v,api))
        return data

    def clientstats(self):
        data = self.getJson("2",'clientstats')
        return data

    def exposurestats(self):
        data = self.getJson("2",'exposurestats')
        return data

    def vmserverstats(self):
        data = self.getJson("2",'vmserverstats')
        return data

    def report(self,mtype="list",args=""):
        #startdata,enddate,hoursback,companyid
        if mtype == "list":
            if args != "":
               data = self.getXml("1",'/report/list.aspx?emailaddress=%s&password=%s&%s' % (self.usr,self.passwd,args))
            else:
               data = self.getXml("1",'/report/list.aspx?emailaddress=%s&password=%s' % (self.usr,self.passwd))
        #jobid,seqnumber
        if mtype == "queue":
           data = self.getXml("1",'/report/queue.aspx?emailaddress=%s&password=%s&%s' % (self.usr,self.passwd,args))
        #guid
        if mtype == "download":
           data = self.getData("1",'/report/download.aspx?emailaddress=%s&password=%s&%s' % (self.usr,self.passwd,args))
        return data

    def mssplist(self):
        data = self.getXml("1",'/mssp/company_list.aspx?emailaddress=%s&password=%s' % (self.usr,self.passwd))
        lst = data.findall("Companies/Company")
        c = []
        for i in lst:
            d = {"Name":"","ID":""}
            d["Name"] = i.find("CompanyName").text
            d["ID"] = i.attrib.get("CompanyID")
            c.append(d)
            d = ""
        return c

    #doesnt seem to work
    def vmserverlist(self,comid):
        data = self.getXml("1",'/company/vmservers_list.aspx?emailaddress=%s&password=%s&companyid=%s' % (self.usr,self.passwd,comid))
        lst = data.findall("VMServers/VMServer")
        c = []
        for i in lst:
            d = {"Name":"","ID":""}
            d["Name"] = i.find("VMServerName").text
            d["ID"] = i.attrib.get("VMServerID")
            c.append(d)
            d = ""
        return c

        
    def job(self,mtype="status",jobid=""):
        #need to add create function
        if mtype == "status":
            data = self.getXml("1",'/job/status.aspx?emailaddress=%s&password=%s&jobid=%s' % (self.usr,self.passwd,jobid))
        if mtype == "start":
            data = self.getXml("1",'/job/start.aspx?emailaddress=%s&password=%s&jobid=%s' % (self.usr,self.passwd,jobid))
        if mtype == "pause":
            data = self.getXml("1",'/job/pause.aspx?emailaddress=%s&password=%s&jobid=%s' % (self.usr,self.passwd,jobid))
        if mtype == "stop":
            data = self.getXml("1",'/job/stop.aspx?emailaddress=%s&password=%s&jobid=%s' % (self.usr,self.passwd,jobid))
        return data

    def xsd(self,mtype):
         data = self.getXml("1",'/xsd.aspx?type=%s' % mtype)
         return data

    def getCompanyID(self,cn):
        ndata = self.mssplist()
        for i in ndata:
            if cn == i["Name"]:
               return i["ID"]

    def getPreReport(self,cn):
        fd = []
        data = {"seq":[]}
        id = self.getCompanyID(cn)
        if id == None:
            return None
        else:
            ls = self.report(mtype="list",args="companyid=%s" % id)
            for b in ls.iter(tag = "Job"):
                data["id"] = b.attrib.get("ID")
                data["name"] = b.attrib.get("Name")
                for c in b.iter(tag="Sequence"):
                    data["seq"].append(c.attrib.get("ID"))
                fd.append(data)
                data = {"seq":[]}
            return fd
    
    def getReportQueue(self,jid,sid):
         ls = self.report(mtype="queue",args="jobid=%s&seqnumber=%s" % (jid,sid))
         return ls.find("RequestKey").text 

    def getReport(self,guid):
        ls = self.report(mtype="download",args="guid=%s" % guid)
        return ls

