# -*-coding:utf-8-*-

import serial
import serial.tools.list_ports
import time
import tool

# 先检查下有哪些端口可用

# port_list = list(serial.tools.list_ports.comports())
# print(port_list)
# if len(port_list) == 0:
#     print '无可用串口'
# else:
#     for i in range(0, len(port_list)):
#         print(port_list[i])
#
# exit()


ser = serial.Serial('COM3', 19200, timeout=0.1, stopbits=1)  # winsows系统使用com1口连接串行口
# ser = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', timeout=0.5)  # winsows系统使用com1口连接串行口

# command list
start_command = "\x02\x7A\x14\x0A\x50\x30\x30\x1B\x30\x1B\x30\x1B\x30\x1B\x0E\x03"
measuring_command = "\x02\x7A\x0C\x0A\x51\x49\x34\x03"
receive_one_level = "\x02\x7A\x0C\x0A\x50\x30\x1A\x03"
receive_two_level = "\x02\x7A\x0C\x0A\x44\x50\x2E\x03"
receive_three_level = "\x02\x7A\x0A\x44\x52\x1B\x0C\x03"
# receive_three_level = "\x02\x7A\x0C\x0A\x44\x52\x1B\x0C\x03"

if ser.isOpen():
    while True:
        # 发送获取测量状态
        print('send -->' + measuring_command)
        n = ser.write(measuring_command)

        time.sleep(1)
        response = ser.readall()
        tool.log('send --> ' + measuring_command)
        tool.log('receive <-- ' + response)
        response = tool.hexShow(response)
        tool.log('receive <-- ' + response)
        print("receive <--" + response)

        if ("51 49 30 30 30 30 42 45 34 32" in response):
            tool.log('start to finish')

            # 直到收到QM才进行发送
            while (True):
                response = ser.readall()
                tool.log('finish wait receive <-- ' + response)
                response = tool.hexShow(response)
                print("finish wait receive <--" + response)
                tool.log('finish wait receive <-- ' + response)
                if ('51 4d' in response):
                    break
                time.sleep(0.5)

            # start get data
            print('finish 1 send -->' + receive_one_level)
            n = ser.write(receive_one_level)
            tool.log('finish 1 send --> ' + receive_one_level)

            while (True):
                response = ser.readall()
                tool.log('finish 1 receive <-- ' + response)
                response = tool.hexShow(response)
                print("finish 1 receive <--" + response)
                tool.log('finish 1 receive <-- ' + response)
                if ('50 30 72' in response):
                    break
                time.sleep(0.5)

            print('finish 2 send -->' + receive_two_level)
            n = ser.write(receive_two_level)
            tool.log('finish 2 send --> ' + receive_two_level)

            last_step = False
            while (True):
                if (last_step):
                    response = ser.readall()
                    tool.log('total receive <-- ' + response)
                    response = tool.hexShow(response)
                    print("total receive <--" + response)
                    tool.log('total receive <-- ' + response)
                    # if (ser.in_waiting):
                    # response = ser.read(ser.in_waiting)
                    # tool.log('total receive <-- ' + response)
                    # response = tool.hexShow(response)
                    # print("total receive <--" + response)
                    # tool.log('total receive <-- ' + response)
                    time.sleep(0.5)
                else:
                    response = ser.readall()
                    tool.log('finish 3 receive <-- ' + response)
                    response = tool.hexShow(response)
                    print("finish 3 receive <--" + response)
                    tool.log('finish 3 receive <-- ' + response)
                    # 得到包含DP和DR的返回后继续获取完整数据
                    if (('44 50' in response) and ('44 52' in response)):
                        time.sleep(0.5)
                        n = ser.write(receive_three_level)
                        print('finish 3 send -->' + receive_three_level)
                        tool.log('finish 3 send -->' + receive_three_level)
                        last_step = True
                    time.sleep(0.5)

        time.sleep(1)
else:
    print('未连接')