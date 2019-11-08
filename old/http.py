#/usr/bin/python
#coding:utf-8
import pycurl
from io import *
import mylog
import requests

def get(url,header=[]):
    try:
        b=BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.CONNECTTIMEOUT,5)
        ch.setopt(pycurl.HTTPHEADER, header)
        ch.setopt(pycurl.WRITEFUNCTION, b.write)
        ch.setopt(pycurl.URL,url)

        ch.setopt(pycurl.TIMEOUT,5)
        ch.setopt(pycurl.NOPROGRESS,1)
        ch.setopt(pycurl.FORBID_REUSE,1)
        ch.setopt(pycurl.MAXREDIRS,1)
        ch.setopt(pycurl.DNS_CACHE_TIMEOUT,30)

        if url.find("https://", 0, 8) >= 0:
            ch.setopt(pycurl.SSL_VERIFYPEER, 0)
            ch.setopt(pycurl.SSL_VERIFYHOST, 0)
        ch.perform()
        ch.close()
        res = b.getvalue()
    except:
        res = False
    return res

def post(url, data, header=[]):
    try:
        b = BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.CONNECTTIMEOUT, 5)
        ch.setopt(pycurl.HTTPHEADER, header)
        ch.setopt(pycurl.POSTFIELDS, data)
        ch.setopt(pycurl.WRITEFUNCTION, b.write)
        ch.setopt(pycurl.URL, url)

        ch.setopt(pycurl.TIMEOUT, 5)
        ch.setopt(pycurl.NOPROGRESS, 1)
        ch.setopt(pycurl.FORBID_REUSE, 1)
        ch.setopt(pycurl.MAXREDIRS, 1)
        ch.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
        if url.find("https://", 0, 8) >= 0:
            ch.setopt(pycurl.SSL_VERIFYPEER, 0)
            ch.setopt(pycurl.SSL_VERIFYHOST, 0)
        ch.perform()
        ch.close()
        res = b.getvalue();
        mylog.log("post\turl=" + url + "\tres=" + res)
    except Exception,e:
        mylog.log("post\texcept\turl" + url + "\tmsg=" + e.message)
        res = False
    return res

def post2(url, data):
    ret = ""
    try:
        mylog.log("url=" + url + "\trequest")
        res = requests.post(url,data=data)
        code = res.status_code
        if code == 200:
            ret = res.text
        else:
            ret = ""
        mylog.log("post\turl=" + url + "\tres=" + ret)
    except Exception, e:
        mylog.log("url=" + url + "\twrong")
        ret = ""
    return ret