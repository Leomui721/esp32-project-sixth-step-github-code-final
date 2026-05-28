# ==================================================
#  ESP32 智能長者照護系統 - 最終純淨版
#  班級：S1B   組別：G6
#  功能：手動時間、服藥提醒、AI藥品辨識(只判對錯)
# ==================================================

from machine import Pin, I2C, UART
import ssd1306
import time

# ===================== 腳位 =====================
I2C_SDA = 21
I2C_SCL = 22
BUZZER = 13
CAM_RX = 17  # 接 CAM TX
CAM_TX = 16  # 接 CAM RX

# ===================== 手動時間 =====================
current_hour = 8
current_minute = 0
MED_HOUR = 8    # 提醒小時
MED_MIN = 0     # 提醒分鐘

# ===================== 初始化 =====================
i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
buzzer = Pin(BUZZER, Pin.OUT)
uart = UART(2, tx=CAM_TX, rx=CAM_RX, baudrate=9600)

# ===================== 函式 =====================
def beep(times):
    for _ in range(times):
        buzzer.value(1)
        time.sleep(0.2)
        buzzer.value(0)
        time.sleep(0.2)

def show(txt, x=10, y=20):
    oled.fill(0)
    oled.text(txt, x, y)
    oled.show()

# ===================== 主程式 =====================
show("System Start")
beep(1)
alert = False

while True:
    # 顯示時間
    now = f"{current_hour:02}:{current_minute:02}"
    oled.fill(0)
    oled.text("Elder Care", 20, 0)
    oled.text(now, 40, 15)
    oled.show()

    # 時間前進
    current_minute += 1
    if current_minute >= 60:
        current_minute = 0
        current_hour += 1
        if current_hour >=24:
            current_hour = 0

    # 服藥提醒
    if current_hour == MED_HOUR and current_minute == MED_MIN and not alert:
        alert = True
        show("TAKE MEDICINE!")
        beep(5)
        time.sleep(2)
    if current_minute != MED_MIN:
        alert = False

    # AI 藥品辨識
    if uart.any():
        msg = uart.readline().decode().strip()
        if msg == "RIGHT":
            show("DRUG CORRECT")
        if msg == "WRONG":
            show("DRUG ERROR!")
            beep(3)

    time.sleep(1)
