import sys, os
sys.path.append(os.path.abspath(".."))

from call_txt2img import *
from call_img2img import *
from build_dynamic_prompt import *
from call_extras import *

loops = 20
steps = 0

while steps < loops:
    randomprompt = build_dynamic_prompt(5,"humanoid","all","all")
    
    
    steps += 1