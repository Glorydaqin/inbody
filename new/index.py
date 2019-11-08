# -*-coding:utf-8-*-

import serial
import serial.tools.list_ports
import time
import tool
import config
import json

ser = serial.Serial(config.serial_port, 19200, timeout=0.1)  # winsows系统使用com1口连接串行口


def deal230(response):
    # 拆分数据
    array = response.split(' ')
    try:
        base = {"PHONE": array[1], "SEX": array[2], "AGE": array[4], "HEIGHT": array[3], "TEST_TIME": array[7]}

        # 身体成分分析 Body composition analysis
        bodys = {}
        bodys['WT'] = array[5]  # 体重
        bodys['BFM'] = array[17]  # 体脂肪
        bodys['BFM_MIN'] = array[152]  # Lower Limit(BFM Normal Range)
        bodys['BFM_MAX'] = array[151]  # Upper Limit(BFM Normal Range)
        bodys['TBW'] = array[18]  # 身体水分含量
        bodys['TBW_MIN'] = array[173]  # Lower Limit(TBW Normal Range)
        bodys['TBW_MAX'] = array[174]  # Upper Limit(TBW Normal Range)
        bodys['FFM'] = array[19]  # 去脂体重
        bodys['FFM_MIN'] = array[175]  # Lower Limit(FFM Normal Range)
        bodys['FFM_MAX'] = array[176]  # Upper Limit(FFM Normal Range)
        bodys['WT_MIN'] = array[154]  # Lower Limit(Weight Normal Range)
        bodys['WT_MAX'] = array[153]  # Upper Limit(Weight Normal Range)
        bodys['SMM'] = array[20]  # 骨骼肌
        bodys['SMM_MIN'] = array[156]  # Lower Limit(SMM Normal Range)
        bodys['SMM_MAX'] = array[155]  # Upper Limit(SMM Normal Range)
        bodys['LLA'] = array[104]  # LBM of Left Arm 节段肌肉
        bodys['LRA'] = array[103]  # LBM of Right Arm
        bodys['LT'] = array[105]  # LBM of Trunk
        bodys['LLL'] = array[107]  # LBM of Left Leg
        bodys['LRL'] = array[106]  # LBM of Right Leg
        bodys['PBFLA'] = array[120]  # PBF of Left Arm 节段脂肪
        bodys['FLA'] = array[104]  # FFM of Left Arm
        bodys['PBFRA'] = array[119]  # PBF of Right Arm
        bodys['FRA'] = array[103]  # FFM of Right Arm
        bodys['PBFT'] = array[121]  # PBF of Trunk 躯干
        bodys['FT'] = array[105]  # FFM of Trunk
        bodys['PBFLL'] = array[123]  # PBF of Left Leg
        bodys['FLL'] = array[107]  # FFM of Left Leg
        bodys['PBFRL'] = array[122]  # PBF of Right Leg
        bodys['FRL'] = array[106]  # FFM of Right Leg
        bodys['BMI'] = array[22]  # 身体质量指数
        bodys['BMI_MIN'] = array[158]
        bodys['BMI_MAX'] = array[157]
        bodys['PBF'] = array[191]  # 体脂肪百分比
        bodys['PBF_MIN'] = array[160]
        bodys['PBF_MAX'] = array[159]
        bodys['WHR'] = array[24]  # 腰臀比
        bodys['WHR_MIN'] = array[162]
        bodys['WHR_MAX'] = array[161]
        bodys['BMR'] = array[27]  # 基础代谢
        bodys['BMR_MIN'] = array[171]
        bodys['BMR_MAX'] = array[172]
        bodys['MC'] = array[25]  # 肌肉控制
        bodys['FC'] = array[206]  # FFM Control 脂肪控制
        bodys['FS'] = array[207]  # InBody Score 健康评估
        bodys['RBMR'] = ''  # 每天摄入卡路里

        return {"basic_data": base, "hbca_data": bodys}
    except Exception as e:
        return False


def upload_body_data(data):
    succ = False
    phone = data['basic_data']['PHONE']
    data['bus_id'] = config.bus_id
    data['license'] = config.license
    data['phone'] = phone

    dt = {"bus_id": data['bus_id'], "license": data['license'], "phone": phone,
          "basic_data": json.dumps(data['basic_data']),
          "hbca_data": json.dumps(data['hbca_data'])}
    url = config.pre_url + "/Web/Inbody/body_data"
    res = tool.post2(url, dt)
    if res != "":
        r = json.loads(res)
        errorcode = r['errorcode']
        if errorcode == 0:
            succ = True
    return succ


def main():
    check_status = False
    # 开机启动位置 C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

    # 开局检测license
    if not check_status:
        succ = tool.check_license(config.bus_id, config.license)
        if succ:
            check_status = True
    if not check_status:
        exit("check status error")

    if config.device_version == 230:
        while True:
            data = {}
            response = ser.readline()
            if response.len > 0:
                data = deal230(response)
            if data:
                upload_body_data(data)
            time.sleep(1)

    else:
        exit('no device code')


if __name__ == '__main__':
    main()
