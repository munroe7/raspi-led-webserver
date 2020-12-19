from flask import Flask, render_template
from flask import request
import neopixel
import board
from gpiozero import MotionSensor
from multiprocessing import Process

# Control if motion sensor is functional
motion_enabled = True
motion_color = (116, 185, 255)
current_color = (116, 185, 255)
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 300
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
#define pixel
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

#create motion sensor
pir = MotionSensor(4)

#create app
app = Flask(__name__)

# Do not change
output = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/color-change', methods=['POST'])
def colorIn():
    print(request.form.get('r'))
    pixels.fill((int(request.form.get('r')), int(request.form.get('g')), int(request.form.get('b'))))
    pixels.show()
    return "done"

def colorCrawl():
   for i in range(num_pixels):
      pixels[i-1] = (0, 0, 0)
      pixels[i] = motion_color
      pixels.show()
   for i in reversed(range(num_pixels)):
      if i < num_pixels-1:
        pixels[i+1] = (0, 0, 0)
      pixels[i] = motion_color
      pixels.show()

def colorFadeIn():
  pixels[0] = (255,255,255)
  pixels[1] = (255,255,255)
  pixels.show()


if __name__ == '__main__':
  #app.run(debug=True, host='0.0.0.0', port=80)
  Process(target=app.run, kwargs=dict(host='0.0.0.0', port=80)).start()
  while True:
    # If motion is detected and lights are not already on
    if pir.motion_detected and motion_enabled and not output:
      output = True
      # Show animation on motion
      colorCrawl()
      colorFadeIn()
      print("motion")
