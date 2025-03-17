import json
import requests
import io
import base64
import uuid
from PIL import Image, PngImagePlugin



def call_extras(imagelocation):
    
    imagewip = Image.open(imagelocation)
    # rest of prompt things
    upscaling_resize = "2"
    upscaler_1 = "4x-UltraSharp"
    upscaler_2 = "R-ESRGAN 4x+"
    
    with open(imagelocation, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string2 = encoded_string.decode('utf-8')
    # Params to stay the same
    url = "http://127.0.0.1:7860"
    outputextrasfolder = "./automated_output/extras/"
    outputextrasfilename = str(uuid.uuid4())
    outputextraspng = '.png'
    outputextrasfull = '{}{}{}.format(outputextrasfolder, outputextrasfilename, outputextraspng)'
    
    
    payload = {
        "upscaling_resize": upscaling_resize,
        "upscaler_1": upscaler_1,
        "image": encoded_string2,
        "resize_mode": 0,
        "show_extras_results": "false",
        "gfpgan_visibility": 0,
        "codeformer_visibility": 0.15,
        "codeformer_weight": 0.1,
        "upscaling_crop": "false",
        "upscaler_2": upscaler_2,
        "extras_upscaler2_visibility": 0.5,
        "upscale_first": "true",
        "rb_enabled": "false",
        "models": "None"                
    }
    
    response = requests.post(url=f'{url}/sdapi/v1/extra-single-image', json=payload)
    
    image = Image.open(io.BytesIO(base64.b64decode(response.json().get("image"))))
    image.save(outputextrasfull)
    
    return outputextrasfull