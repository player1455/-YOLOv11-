import base64
import io
from PIL import Image
import numpy as np
import cv2

def base64_to_image(base64_string):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

def image_to_base64(image, format='JPEG', quality=85):
    buffered = io.BytesIO()
    image.save(buffered, format=format, quality=quality)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def preprocess_image(image):
    img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return img_np

def postprocess_image(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(img_rgb)
    return result_image
