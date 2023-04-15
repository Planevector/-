import cv2
import pytesseract
import os
import subprocess
import time

# 配置ADB工具路径和设备名称
# ADB_PATH = 'D:/Tool/platform-tools/adb'
# DEVICE_NAME = 'R5CTC019WAY'

# 读取图片中的电话号码
image = cv2.imread('./phone_number.png')
phone_number = pytesseract.image_to_string(image, lang='eng', config='--psm 6')

# 移除电话号码中的非数字字符
phone_number = ''.join(filter(str.isdigit, phone_number))

phone_number_list = [phone_number[i:i+11] for i in range(0, len(phone_number), 11)]

index = 0
# 输入电话号码并模拟拨号按键

def check_phone_call():
    cmd1 = "adb shell appops set android READ_PHONE_STATE allow"
    # 执行 adb shell 命令
    adb_output = subprocess.check_output(['adb', 'shell', 'dumpsys', 'telephony.registry']).decode()

   # 使用字符串操作过滤出电话状态信息
    call_state_output = [line for line in adb_output.split('\n') if 'mCallState' in line]

    # 获取电话状态
    if 'mCallState=0' in call_state_output[0]:
        print("Phone is idle.")
        return False
    elif 'mCallState=2' in call_state_output[0]:
        print("Phone is ringing.")
        return True

# 监听键盘事件，等待电话结束
while True:
    if not check_phone_call():
        # 如果电话已挂断，则拨打下一个电话
        print('拨打下一个电话')
        cmd = f'adb shell am start -a android.intent.action.CALL -d tel:{phone_number_list[index]}'
        os.system(cmd)
        index += 1
        if index == len(phone_number_list) :
            exit(0)
        time.sleep(2)  # 等待2秒后开始监听电话状态
    else:
        # 如果电话还在通话中，则继续监听电话状态
        print('等待电话挂断')
        time.sleep(1)
