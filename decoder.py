
import base64
import io
import numpy as np
from PIL import Image # image to text
import pytesseract # image to text
import cv2
import matplotlib.pyplot as plt

import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def save_image_base64(raw, path_to_file):
    img_data = raw.replace('data:image/png;base64,', '')
    img_data_bytes = img_data.encode()
    base64_img = base64.decodebytes(img_data_bytes)
    with open("{path}".format(path=path_to_file), "wb") as fh:
        fh.write(base64_img)

def image_to_text(path_to_file):
    img = Image.open(path_to_file)
    res = ocr.classification(img)
    text = pytesseract.image_to_string(img, lang='eng')
    res_int = 0
    try:
        if ( res == [] ):
            res = text
        res = res.replace("o","0")
        res_int = int(res)
    except ValueError:
        try:
            if ( text == [] ):
                text = res
            res_int = int(text)
        except:
            res_int = -1
    
    return res_int


def base64_to_text(raw, path_to_file='tmp.png'):
    save_image_base64(raw=raw, path_to_file=path_to_file)
    return image_to_text('tmp.png')

