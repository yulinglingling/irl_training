plusx, minusx, plusang, minusang, stay = 0, 1, 2, 3, 4
import random
l_act = []
# for i in range(5):
#     start_yaw = random.randint(0, 35)
#     start_x = random.randint(0, 4)
#     end_yaw, end_x = 19, 2
#     tmp = []
#     print("start: ", start_yaw, start_x)
#     if(start_yaw > end_yaw):
#         for j in range(start_yaw - end_yaw):
#             tmp.append(minusang)
#     else:
#         for j in range(end_yaw - start_yaw):
#             tmp.append(plusang)

#     if(start_x > end_x):
#         for j in range(start_x - end_x):
#             tmp.append(minusx)
#     else:
#         for j in range(end_x - start_x):
#             tmp.append(plusx)
#     l_act.append(tmp)
#     print(tmp);
    

# a = 5
# a //= 2
# print(a)

# print(1e5)

# def record(*args):
#     # 打开文件以进行写入（'w' 模式表示写入模式）
#     with open('output.txt', 'w') as file:
#         # 写入文本数据
#         for arg in args:
            
#             if(type(arg) == list):
#                 arg = map(str, arg)
#                 tmp = ','.join(arg)
#             else: tmp = arg
#             file.write(f'[{tmp}]\n')

# if(__name__ == "__main__"):
#     record([1, 2], 3, [4], 5)
#     print(type([1,2]))

import serial
import time

arduino = serial.Serial('COM6', 9600)
time.sleep(2)

# 发送打开夹爪的命令
arduino.write(b'OPEN\n') 
# time.sleep(0.5) # 等待 Arduino 执行
while True:
    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').rstrip()
        print("Arduino says:", data)
        break
    else:
        time.sleep(0.05)

print('sleep 1 sec')
time.sleep(2)
print('sleep 1 sec done')

# 发送关闭夹爪的命令
arduino.write(b'CLOSE\n')
# time.sleep(0.5) # 等待 Arduino 执行
while True:
    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').rstrip()
        print("Arduino says:", data)
        break
    else:
        time.sleep(0.05)
    
time.sleep(1)

arduino.close()

