# -*-coding:utf-8-*-
import os
import sys
import json
import platform
import uuid
import accessdb
import mylog
import http
import ConfigParser
import util
import win32api
import clearthread
import time
import serial

PREFIX_URL = "https://wx.rocketbird.cn"
is_read_file = True
new_id = 10
bus_id = ""
license = ""
check_status = False




# 检测体测数据
def run():
    global is_read_file, new_id, check_status
    # mylog.log("args2="+json.dumps(sys.argv))
    # mylog.log("run=" + os.path.split(os.path.realpath(sys.argv[0]))[0])
    # mylog.log("pwd=" +os.getcwd())
    if not check_status:
        clearthread.clear()
        succ = check()
        if succ:
            check_status = True
    id = get_new_id()
    mylog.log("id=" + id)
    res = accessdb.get("select * from SPHYG_DATA_TBL where DATETIMES>'" + id + "' order by DATETIMES asc")
    mylog.log(json.dumps(res))
    for v in res:
        # print res
        local_id = v[0]
        lastest_new_id = v[1]
        # 获取用户信息
        # 获取各个表数据
        bodys = get_body_datas(local_id, lastest_new_id)
        # 提交给服务器
        succ = upload_body_data(bodys)

        # 写new_id到配置文件
        if succ == True:
            set_new_id(lastest_new_id)
            is_read_file = True
            new_id = lastest_new_id
    if len(res) == 0:
        is_read_file = False




# 添加一个缓存，不用每次都去读取文件
def get_new_id():
    global new_id, is_read_file, bus_id, license
    if is_read_file:
        filepath = util.get_current_path() + "\license.ini"
        conf = ConfigParser.ConfigParser()
        res = conf.read(filepath)
        new_id = conf.get("config", "new_id")
        bus_id = conf.get("config", "bus_id")
        license = conf.get("config", "license")
    return new_id


def set_new_id(lastest_new_id):
    filepath = util.get_current_path() + "\license.ini"
    conf = ConfigParser.ConfigParser()
    res = conf.read(filepath)
    conf.set("config", "new_id", lastest_new_id)
    conf.write(open(filepath, "wb"))


def get_body_datas(local_id, lastest_new_id):
    # lastest_new_id = '20171109154017'
    # print "select * from USER_INFO1_TBL where LOCAL_ID = " + str(local_id)
    # 基本信息
    res = accessdb.get("select * from USER_INFO1_TBL where LOCAL_ID = " + str(local_id))
    v = res[0]
    phone = v[1]
    sex = v[3]
    age = v[4]
    height = v[5]
    base = {"PHONE": phone, "SEX": sex, "AGE": age, "HEIGHT": height, "TEST_TIME": lastest_new_id}

    bodys = {}
    # 身体成分分析 Body composition analysis
    res = accessdb.get(
        "select bca.WT,bca.BFM,bca.BFM_MIN,bca.BFM_MAX ,bca.TBW,bca.TBW_MIN,bca.TBW_MAX,bca.FFM,bca.FFM_MIN,bca.FFM_MAX  from BCA_TBL bca where bca.DATETIMES='" + lastest_new_id + "'")
    v1 = res[0]
    # 体重
    wt = v1[0]
    # 体脂肪
    bfm = v1[1]
    bfm_min = v1[2]
    bfm_max = v1[3]
    # 身体水分含量
    tbw = v1[4]
    tbw_min = v1[5]
    tbw_max = v1[6]
    # 去脂体重
    ffm = v1[7]
    ffm_min = v1[8]
    ffm_max = v1[9]

    bodys['WT'] = wt
    bodys['BFM'] = bfm
    bodys['BFM_MIN'] = bfm_min
    bodys['BFM_MAX'] = bfm_max
    bodys['TBW'] = tbw
    bodys['TBW_MIN'] = tbw_min
    bodys['TBW_MAX'] = tbw_max
    bodys['FFM'] = ffm
    bodys['FFM_MIN'] = ffm_min
    bodys['FFM_MAX'] = ffm_max

    sql = "select mfa.WT_MIN,mfa.WT_MAX,mfa.SMM,mfa.SMM_MIN,mfa.SMM_MAX from  MFA_TBL as mfa  where mfa.DATETIMES='" + lastest_new_id + "'"
    res = accessdb.get(sql)
    v2 = res[0]

    wt_min = v2[0]
    wt_max = v2[1]
    # 骨骼肌
    smm = v2[2]
    smm_min = v2[3]
    smm_max = v2[4]
    bodys['WT_MIN'] = wt_min
    bodys['WT_MAX'] = wt_max
    bodys['SMM'] = smm
    bodys['SMM_MIN'] = smm_min
    bodys['SMM_MAX'] = smm_max

    sql = "select lb.LLA,lb.LRA, lb.LT ,lb.LLL,lb.LRL,  lb.PBFLA,lb.FLA,  lb.PBFRA,lb.FRA, lb.PBFT,lb.FT,  lb.PBFLL,lb.FLL, lb.PBFRL,lb.FRL from LB_TBL as lb  where lb.DATETIMES='" + lastest_new_id + "'"
    res = accessdb.get(sql)
    v3 = res[0]
    # 节段肌肉
    lla = v3[0]
    lra = v3[1]
    lt = v3[2]
    lll = v3[3]
    lrl = v3[4]

    # 节段脂肪
    pbfla = v3[5]
    fla = v3[6]

    pbfra = v3[7]
    fra = v3[8]

    # 躯干
    pbft = v3[9]
    ft = v3[10]

    pbfll = v3[11]
    fll = v3[12]

    pbfrl = v3[13]
    frl = v3[14]

    bodys['LLA'] = lla
    bodys['LRA'] = lra
    bodys['LT'] = lt
    bodys['LLL'] = lll
    bodys['LRL'] = lrl
    bodys['PBFLA'] = pbfla
    bodys['FLA'] = fla
    bodys['PBFRA'] = pbfra
    bodys['FRA'] = fra
    bodys['PBFT'] = pbft
    bodys['FT'] = ft
    bodys['PBFLL'] = pbfll
    bodys['FLL'] = fll
    bodys['PBFRL'] = pbfrl
    bodys['FRL'] = frl
    # print bodys
    res = accessdb.get(
        "select mfa.BMI,mfa.BMI_MIN,mfa.BMI_MAX,  mfa.PBF,mfa.PBF_MIN,mfa.PBF_MAX,  mfa.WHR,mfa.WHR_MIN,mfa.WHR_MAX from MFA_TBL as mfa where mfa.DATETIMES = '" + lastest_new_id + "'")
    v4 = res[0]
    # 身体质量指数
    bmi = v4[0]
    bmi_min = v4[1]
    bmi_max = v4[2]
    # 体脂肪百分比
    pbf = v4[3]
    pbf_min = v4[4]
    pbf_max = v4[5]
    # 腰臀比
    whr = v4[6]
    whr_min = v4[7]
    whr_max = v4[8]
    bodys['BMI'] = bmi
    bodys['BMI_MIN'] = bmi_min
    bodys['BMI_MAX'] = bmi_max
    bodys['PBF'] = pbf
    bodys['PBF_MIN'] = pbf_min
    bodys['PBF_MAX'] = pbf_max
    bodys['WHR'] = whr
    bodys['WHR_MIN'] = whr_min
    bodys['WHR_MAX'] = whr_max

    res = accessdb.get(
        "select wc.BMR,wc.BMR_MIN,wc.BMR_MAX, wc.MC,wc.FC,wc.FS,wc.RBMR from WC_TBL as wc where DATETIMES = '" + lastest_new_id + "'")
    v5 = res[0]
    # 基础代谢
    bmr = v5[0]
    bmr_min = v5[1]
    bmr_max = v5[2]
    # 肌肉控制
    mc = v5[3]
    # 脂肪控制
    fc = v5[4]
    # 健康评估
    fs = v5[5]
    # 每天摄入卡路里
    rbmr = v5[6]

    bodys['BMR'] = bmr
    bodys['BMR_MIN'] = bmr_min
    bodys['BMR_MAX'] = bmr_max
    bodys['MC'] = mc
    bodys['FC'] = fc
    bodys['FS'] = fs
    bodys['RBMR'] = rbmr
    # print base
    # print bodys
    return {"basic_data": base, "hbca_data": bodys}


# 验证本地数据和license
def check():
    succ = False
    filepath = util.get_current_path() + "\license.ini"
    conf = ConfigParser.ConfigParser()
    res = conf.read(filepath)
    mylog.log("check\t filepath=" + filepath + "\tres=" + json.dumps(res))
    if res == []:
        return succ
    mdb = conf.get("config", "dbpath")
    if not os.path.exists(mdb):
        mylog.log("mdb=" + mdb + "\tres=False")
        succ = False
        return succ

    bus_id = conf.get("config", "bus_id")
    license = conf.get("config", "license")
    # mylog.log("bus_id="+bus_id+"\tlicense"+license)
    succ = check_license(bus_id, license)
    return succ


# 默认在后台打开inbody软件
def open_inbody():
    try:
        succ = False
        filepath = util.get_current_path() + "\license.ini"
        conf = ConfigParser.ConfigParser()
        res = conf.read(filepath)
        mylog.log("open_inbody\t filepath=" + filepath + "\tres=" + json.dumps(res))
        if res == []:
            return succ
        exepath = conf.get("config", "exepath")
        mylog.log("exepath=" + exepath)
        ret = win32api.ShellExecute(0, 'open', exepath, '', '', 0)
        mylog.log("open_inbody\tret=" + json.dumps(ret))
        return ret
    except Exception, e:
        mylog.log("open_inbody error")
        return False


# 验证license
def check_license(bus_id, license):
    succ = False
    url = PREFIX_URL + "/Web/Inbody/check_license"
    info = get_system_info()
    # data = 'bus_id='+bus_id+ "&license="+license+"&device_info="+json.dumps(info)
    # mylog.log("license=" + json.dumps(data),1)
    # res = http.post2(url, data)
    for i in range(0, 1000):
        data = {"bus_id": bus_id, "license": license, "device_info": json.dumps(info)}
        mylog.log("check_license\tdata=" + json.dumps(data))
        res = http.post2(url, data)
        mylog.log("check_license\tdata=" + json.dumps(data) + "\tres=" + json.dumps(res), 1)
        if res != "":
            r = json.loads(res)
            errorcode = r['errorcode']
            if errorcode == 0:
                succ = True
                break
        else:
            time.sleep(2)

    return succ


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


def upload_log(str):
    url = PREFIX_URL + "/Web/Upload/log"
    data = {"log_info": str}
    # http.post2(url,"log_info=" + str)
    http.post2(url, data)


def upload_body_data(data):
    global bus_id, license
    succ = False
    phone = data['basic_data']['PHONE']
    data['bus_id'] = bus_id
    data['license'] = license
    data['phone'] = phone

    # dt = "bus_id="+bus_id+"&license="+license+"&phone=" + phone + "&basic_data=" + json.dumps(data['basic_data']) + "&hbca_data=" + json.dumps(data['hbca_data'])
    dt = {"bus_id": bus_id, "license": license, "phone": phone, "basic_data": json.dumps(data['basic_data']),
          "hbca_data": json.dumps(data['hbca_data'])}
    url = PREFIX_URL + "/Web/Inbody/body_data"
    res = http.post2(url, dt)
    mylog.log("update_body_data\tdt=" + json.dumps(dt) + "\tres=" + json.dumps(res))
    if res != "":
        r = json.loads(res)
        errorcode = r['errorcode']
        if errorcode == 0:
            succ = True
    return succ
