from subprocess import Popen,PIPE, check_output
import os, sys
import tempfile
import uuid
import cv2
import pytesseract as pt
from PIL import Image

def convert_dpi(input_image):
    path = tempfile.gettempdir()
    filename = str(uuid.uuid4())[:8] + ".jpg"
    filename_out = str(uuid.uuid4())[:8] + "_out.jpg"
    image_path = os.path.join(path, filename)
    image_path_out = os.path.join(path, filename_out)
    cv2.imwrite(image_path, input_image)
    
    proc_identify = check_output(['identify', '-format', "dpi:%y", image_path], stderr=PIPE)
    dpi = str(proc_identify).replace('dpi:','')
    print("image identify finish, DPI: "+dpi)
    proc_convert = Popen(['convert', '-units', 'PixelsPerInch', image_path, '-density', dpi, image_path_out])
    out = proc_convert.communicate()
    p_status = proc_convert.wait()
    print("image convert finished: ", out, p_status, image_path_out)
    return image_path_out


imagepath = './Data/2/mj-1.tif'
img = cv2.imread(imagepath)
print("first attempt: ", pt.image_to_string(img))
converted_img = convert_dpi(img)
print("second attempt: ", pt.image_to_string(cv2.imread(converted_img)))
print("thrid attempt: ", pt.image_to_string(converted_img))
print("fourth attempt: ", pt.image_to_string(Image.open(converted_img)))