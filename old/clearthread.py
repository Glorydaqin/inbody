#-*-coding:utf-8-*-
import os
import thread
import time
import util
import mylog
import win32api
import json

def clear_log(threadName,delay):
    try:
        cmd = "forfiles /p " + util.get_current_path() + "\log" + " /s /m *.* /d -7 /c " + "\"cmd /c del @path\""
        mylog.log("clear_log\t" + cmd)
        os.system(cmd)
        #time.sleep(86400)
    except Exception, e:
        return

def clear():
    thread.start_new_thread(clear_log, ("Thread-1", 1))

def open_inbody_deal(threadName, exepath):
    try:
        ret = win32api.ShellExecute(0, 'open', exepath, '', '', 1)
        mylog.log("open_inbody=" + json.dumps(ret))
        return ret
    except Exception, e:
        mylog.log("open_inbody wrong")
        return False

def open_inbody(exepath):
    thread.start_new_thread(open_inbody_deal, ("Thread-2", exepath))
