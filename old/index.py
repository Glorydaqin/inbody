#coding:utf-8

import win32serviceutil
import win32service
import win32event
import winerror
import servicemanager
import os, sys, time, json
import mylog
import deal
import win32api

class InbodyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "InbodyTest"  # 服务名
    _svc_display_name_ = "A Inbody Service "  # 服务在windows系统中显示的名称
    _svc_description_ = "inbody test of physical strength"  # 服务的描述

    def __init__(self, args):
        mylog.log("__init__\targs" + json.dumps(args))
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        #self.License = self._LicenseExist()

        #deal.open_inbody()
        self.run = True

    def SvcDoRun(self):
        while self.run:
            # 已经运行
            time.sleep(2)  # 推迟调用线程的运行2秒
            self.dealLogic()

    def SvcStop(self):
        # 服务已经停止
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
        mylog.log("stop service")
    def ClearThread(self):
        print "test"
    def dealLogic(self):
        deal.run()

if __name__ == '__main__':

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(InbodyPythonService)
            servicemanager.Initialize('InbodyPythonService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error , details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
                time.sleep(5)

    else:
        print "start service"
        mylog.log("start service argv=" + json.dumps(sys.argv))
        win32serviceutil.HandleCommandLine(InbodyPythonService)