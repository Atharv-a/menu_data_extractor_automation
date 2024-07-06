import io
import os
import httpx
import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
api_key = os.environ.get('OCR_API_KEY')

def url_to_text(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Cannot fetch image from URL: {url}")
        
        image_content = response.content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        mime_type = Image.MIME[image.format]

        if image.format not in ["JPEG", "PNG", "GIF", "BMP", "TIFF"]:
            print(f"Skipping image with unsupported format: {url}")
            return None
        
        lines = ocr_space_file(api_key, image_content, mime_type, image.format)
        lines = extract_text_from_response(lines)
    
        # print("\n", "=" * 5, 'printing text found', "=" * 5, "\n")
        # print(lines)
        return lines
    except Exception as e:
        print('Failed text extraction: ', e)
        return None


def ocr_space_file(api_key, image_content, mime_type, format, overlay=False, language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
 
    image_file = io.BytesIO(image_content)
    files = {'image': (f'image.{format}', image_file, mime_type)}

    response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload)
    return response.json()

def extract_text_from_response(response):
    parsed_results = response.get("ParsedResults")
    if not parsed_results:
        return "No text found"
    text = parsed_results[0].get("ParsedText")
    return text.strip()


