import os
import pytesseract
from PIL import Image

folder_path = './image/'
image_files = os.listdir(folder_path)
custom_config = r'--oem 3 --psm 6 outputbase page'

def image_to_text():
    text_for_images = []
    for image_file in image_files:
        file_path = os.path.join(folder_path, image_file)
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, config=custom_config)

        lines = text.split('\n')

        text_for_images.append(lines)
        
    return text_for_images