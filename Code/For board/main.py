from machine import Pin, SPI
from network import WLAN
from time import sleep_ms, ticks_diff, ticks_ms
from urequests import get
from st7735 import TFT
from sysfont import sysfont

ssid = "WiFi Name"
password = "WiFi Password"
ip = "http://YOUR_IP:8000"

spi = SPI(1, baudrate=20000000)

tft = TFT(
    spi,
    aDC=2,
    aReset=0,
    aCS=16
)

tft.init_7735(tft.REDTAB)
tft.rotation(1)

ap_if = WLAN(WLAN.IF_AP)
ap_if.active(False)

sta_if = WLAN(WLAN.IF_STA)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    sleep_ms(200)

prev_track = Pin(4, Pin.IN, Pin.PULL_UP)
play_pause = Pin(5, Pin.IN, Pin.PULL_UP)
next_track = Pin(12, Pin.IN, Pin.PULL_UP)

pt_flag = 0
pp_flag = 0
nt_flag = 0

last_tick = ticks_ms()
api_interval = 5000

last_data = {"title": None, "artist": None}

def update():
    global last_data
    response = get(ip)
    
    if response.status_code == 200:
        data = response.json()
        if data != last_data:
            tft.fill(TFT.BLACK)
            tft.text((10, 54), data['title'], TFT.WHITE, sysfont, 1)
            tft.text((10, 66), data['artist'], TFT.WHITE, sysfont, 1)
            last_data = data
        

while True:
    current_tick = ticks_ms()
    if ticks_diff(current_tick, last_tick) > api_interval:
        update()
        last_tick = ticks_ms()
    
    if not prev_track.value():
        if not pt_flag:
            try: get(ip+"/prev"); update()
            except: pass
        pt_flag = 1
    else:
        pt_flag = 0
    
    if not play_pause.value():
        if not pp_flag:
            try: get(ip+"/play_pause"); update()
            except: pass
        pp_flag = 1
    else:
        pp_flag = 0
    
    if not next_track.value():
        if not nt_flag:
            try: get(ip+"/next"); update()
            except: pass
        nt_flag = 1
    else:
        nt_flag = 0
    
    sleep_ms(50)
