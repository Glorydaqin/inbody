# -*-coding:utf-8-*-

import serial
import serial.tools.list_ports
import time

# 先检查下有哪些端口可用

port_list = list(serial.tools.list_ports.comports())
print(port_list)
if len(port_list) == 0:
    print '无可用串口'
else:
    for i in range(0, len(port_list)):
        print(port_list[i])

exit()



ser = serial.Serial('COM3', 19200, timeout=0.5)  # winsows系统使用com1口连接串行口
# ser = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', timeout=0.5)  # winsows系统使用com1口连接串行口

if ser.isOpen():

    while True:

        # 发送获取测量状态
        ser.write('02 63 03'.encode())
        response = ser.readline()
        print("开始获取响应")
        print(response.decode())  # 打印响应内容
        time.sleep(0.1)

else:
    print('未连接')
