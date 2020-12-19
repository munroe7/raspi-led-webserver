import neopixel
import board
import time

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 225
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
#define pixel
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def fill(r, g, b):
  pixels.fill((r, g, b))
  pixels.show()

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])


def linear_gradient(start_hex, finish_hex, n=65):
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    for i in range(num_pixels):
      pixels[i] = (curr_vector[0], curr_vector[1], curr_vector[2])
    pixels.show()
  return True

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

def rainbow_cycle(wait):
     for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def cylon(r, g, b, eyeSize):
  for i in range(num_pixels-eyeSize-2):
     fill(0,0,0)
     pixels[i] = (r//10, g//10, b//10)
     for j in range(1, eyeSize):
       pixels[i+j] = (r, g, b)
     pixels[i+eyeSize+1] = (r//10, g//10, b//10)
     pixels.show()

  for i in reversed(range(num_pixels-eyeSize-2)):
    fill(0,0,0)
    pixels[i] = (r//10, g//10, b//10)
    for j in range(1, eyeSize):
      pixels[i+j] = (r, g, b)
    pixels[i+eyeSize+1] = (r//10, g//10, b//10)
    pixels.show()
