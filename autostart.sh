# mbgradio.py autostart
mpc clear
mpc repeat off
mpc add boot.mp3
mpc volume 40
mpc play
sleep 6
python /home/pi/susi-radio/susi.py
respawn
