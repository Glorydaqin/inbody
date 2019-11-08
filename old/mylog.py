#-*-coding:utf-8-*-
import datetime
import os
import deal
import util
def log(str,isupload=False):
    now = datetime.datetime.now()
    str = now.strftime('%Y-%m-%d %H:%M:%S') +"\t" +str + "\n"
    dt =  now.strftime('%Y-%m-%d')
    if os.path.exists(util.get_current_path() + "\log") == False:
        os.mkdir(util.get_current_path() + "\log")
    filename = util.get_current_path() + "\log\inbody-" + dt + ".log"
    #print filename
    fp = open(filename, "a+")
    fp.write(str)
    fp.close()
    if isupload:
        deal.upload_log(str)
        return
