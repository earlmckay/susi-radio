import time
import os
from gpiozero import Button
from gpiozero import RotaryEncoder
from signal import pause
from subprocess import check_call
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError

#---------- VAR DEFINITION ----------#
current_station = 0;
vol = 40;
btn_clk = RotaryEncoder(17, 27, bounce_time=float)
btn_sw = Button(22)
RS1 = "http://wdr-wdr3-live.icecast.wdr.de/wdr/wdr3/live/mp3/128/stream.mp3"
RS2 = "http://wdr-wdr5-live.icecast.wdr.de/wdr/wdr5/live/mp3/128/stream.mp3"
RS3 = "http://s2-webradio.antenne.de/90er-hits"

#---------- RADIO STATIONS ORDER ----------#
stations = [RS1, RS2, RS3]

#---------- ANNOUNCEMENTS ORDER ----------#
announcements = ["rs1.mp3", "rs2.mp3", "rs3.mp3"]

#---------- DEFINITIONS ----------#
def change_station():
    global current_station
    print("changing station from " + str(current_station))
    current_station = (current_station + 1) % len(stations)  
    play(current_station)

def play(current_station):
    print(stations[current_station])
    sudo_mpc("stop")
    sudo_mpc("clear")
    sudo_mpc("add " + announcements[current_station])
    sudo_mpc("add " + stations[current_station])
    sudo_mpc("play")
 

def check_connection():
    try:
        response = urlopen("https://www.google.de")
    except:
        print('OFFLINE')
        sudo_mpc("add no_connection.mp3")
        sudo_mpc("add wps_client.mp3")
        sudo_mpc("play")
        time.sleep(6)
        btn_sw.wait_for_press(timeout=30)
        if btn_sw.is_pressed:
            sudo_mpc("clear")
            sudo_mpc("repeat off")
            sudo_mpc("add wps_router.mp3")
            sudo_mpc("play")
            time.sleep(7)
            os.system("sudo python /home/pi/susi-radio/auto_wps.py")   
        else:
            sudo_mpc("clear")
            sudo_mpc("repeat on")
            sudo_mpc("add problem.mp3")
            sudo_mpc("play")
            time.sleep(15)
            os.system("sudo python /home/pi/susi-radio/susi.py")
    else:
        print('ONLINE')

def sudo_mpc(command):
    os.system("sudo mpc " + command)
    
def vol_up():
    global vol
    vol += 5
    print(str(vol))
    sudo_mpc("volume " + str(vol))

def vol_down():
    global vol
    vol -= 5
    print(str(vol))
    sudo_mpc("volume " + str(vol)) 
 
#---------- START ----------#
sudo_mpc("clear")
sudo_mpc("volume 40")
sudo_mpc("repeat off")
check_connection()
play(current_station)
 
btn_clk.when_rotated_clockwise = vol_up
btn_clk.when_rotated_counter_clockwise = vol_down
btn_sw.when_pressed = change_station


pause()