import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


print("The Arecibo message")
print("The Arecibo message is an interstellar radio message carrying basic information about humanity and Earth that was sent to globular star cluster M13 in 1974.")
print("The entire message consisted of 1,679 binary digits, approximately 210 bytes, transmitted at a frequency of 2,380 MHz and modulated by shifting the frequency by 10 Hz, with a power of 450 kW.")
print()

# Load the sound
fs, data = wav.read('arecibo.wav')
output_file = 'arecibo.jpg'

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

f1, f2 = 1000, 1010
# Apply the band pass filter
data_f2 = butter_bandpass_filter(data, f2 - 10, f2 + 10, fs, order=3)

# One symbol length in seconds
t_sym = 0.1
width, height = 23*int(t_sym*fs), 80

# Display the wav data after filtering as a raster image
image = Image.new('RGB', (width, height))
px, py = 0, 0
for p in range(data_f2.shape[0]):
    image.putpixel((px, py), (0, int(data_f2[p]//32), 0))
    px += 1
    if px >= width:
        px = 0
        py += 1
        if py >= height:
            break

# Image is too narrow, make it wider for better view
image = image.resize((width//100, 10*height))
image.save(output_file)
print("Image '%s' saved" % output_file)
image.show()