from flask import Flask, render_template, request
import time
import board
import datetime
from tools.w2812b import *
from gpiozero import MotionSensor
from multiprocessing import Process
from threading import Thread

#SETTINGS
active_color = [72, 219, 251]
# Control if motion sensor is functional
motion_enabled = True
# LED color for motion animation
motion_color = (255, 255, 255)
# Autoshutoff LEDs after a specific time period in seconds
inactivity_timeout = 300

#INIT
#create motion sensor
pir = MotionSensor(4)
#create app
app = Flask(__name__)
# Do not change
output = False
# Track active animation
active_animation = {'rainbow': False, 'cycle': False}

#WEBAPP LOGIC
@app.route('/')
def index():
   return render_template('index.html', rgb=active_color, active_color=RGB_to_hex(active_color))

@app.route('/color-change', methods=['POST'])
def colorChange():
   global active_color
   active_color[0] = int(request.form.get('r'))
   active_color[1] = int(request.form.get('g'))
   active_color[2] = int(request.form.get('b'))
   fill(int(request.form.get('r')), int(request.form.get('g')), int(request.form.get('b')))
   return "success"

@app.route('/animation', methods =['POST'])
def animations():
  animate(request.form.get('type'))
  return "success"

def animate(type):
  if type == 'rainbow':
    rainbow_cycle(0.001)
  elif type == 'cycle':
    cylon(72, 219, 251, 100)

if __name__ == '__main__':
  last_motion=-1
  #app.run(debug=True, host='0.0.0.0', port=80)
  Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=80)).start()
  while True:
    # Track current time
    current_time=datetime.datetime.now()
    current_timestamp=current_time.timestamp()
    # Autoshutoff if no motion detected
    if output and ((current_timestamp - last_motion) > inactivity_timeout):
       output = False
       fill(0, 0, 0)
    # If motion is detected and lights are not already on
    if pir.motion_detected and motion_enabled and not output:
      output = True
      #un comment below line to add cylon animation to motion wakeup
      #cylon(251, 5, 26, 50)
      linear_gradient("#000000", RGB_to_hex(motion_color))
      linear_gradient(RGB_to_hex(motion_color), "#000000")
      linear_gradient("#000000", RGB_to_hex(active_color))
      last_motion=current_timestamp
      fill(active_color[0], active_color[1], active_color[2])
    # If motion detected and it's enabled, reset counter
    if pir.motion_detected and motion_enabled and output:
      last_motion=current_timestamp
      output = True
