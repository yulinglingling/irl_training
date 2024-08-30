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

