# -*-coding:utf-8-*-

import os
import sys
import json
import platform
import uuid
import config

# 获取系统信息
def get_system_info():
    op = platform.system()
    release = platform.platform()
    version = platform.version()
    node = platform.node()
    sys = op + " |" + version + " |" + release + "|" + node

    node1 = uuid.getnode()
    unique_id = uuid.UUID(int=node1).hex[-12:].upper()
    data = {"sys": sys, "client_unique_id": unique_id}
    return data



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
        res = b.getvalue()
    except Exception,e:
        res = False
    return res

def post2(url, data):
    try:
        res = requests.post(url,data=data)
        code = res.status_code
        if code == 200:
            ret = res.text
        else:
            ret = ""
    except Exception, e:
        ret = ""
    return ret

def check_license(bus_id, license):
    succ = False
    url = config.pre_url + "/Web/Inbody/check_license"
    info = get_system_info()

    for i in range(0, 1000):
        data = {"bus_id": bus_id, "license": license, "device_info": json.dumps(info)}
        res = post2(url, data)
        if res != "":
            r = json.loads(res)
            errorcode = r['errorcode']
            if errorcode == 0:
                succ = True
                break
        else:
            time.sleep(2)

    return succ
