from call_img2img import *
from call_extras import *
import os

directory = './automated_output/Upscale Me/'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        
        img2img1 = call_img2img(f,0.25,1.5,256)
        
        finalfile = call_extras(img2img1)