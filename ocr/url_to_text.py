import io, os
import httpx
from dotenv import load_dotenv
from PIL import Image
import pytesseract

load_dotenv()

custom_config = os.environ.get('SETTINGS_FOR_TESSERACT')


async def url_to_text(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise Exception(f"Can not fetch image form url: {url}")

        image_content = response.content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)

        
        if image.format not in ["JPEG", "PNG"]:
            print(f"Skipping image with unsupported format: {url}")
            return None

        lines = image_to_text(image)

        print(url)
        print("\n","="*5, 'printing text found', "="*5, "\n")
        print(lines)
        return lines
    except Exception as e:
        print('FAILED -', e)
        return None


def image_to_text(image):
    text = pytesseract.image_to_string(image, config=custom_config)
    lines = text.split('\n')
    return lines
