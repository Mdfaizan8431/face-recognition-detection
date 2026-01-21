import base64
import cv2
import numpy as np

def base64_to_image(base64_str: str):
    img_bytes = base64.b64decode(base64_str)
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img
