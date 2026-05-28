# ==================================================
#  ESP32-CAM 藥品辨識程式
#  功能：辨識藥品 -> 回傳 RIGHT / WRONG
# ==================================================

from machine import UART, Pin
import time

# 串口傳給ESP32
uart = UART(1, baudrate=9600, tx=1, rx=3)

# 模擬AI辨識 (你之後可以替換成真實模型)
def check_medicine():
    # 這裡以後接你的AI模型
    # 正確回傳 1
    # 錯誤回傳 0
    return 1  # 測試用

# ===================== 主程式 =====================
while True:
    result = check_medicine()
    
    if result == 1:
        uart.write("RIGHT\n")
    else:
        uart.write("WRONG\n")
    
    time.sleep(1)
