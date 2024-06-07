import os,io, requests
from PIL import Image


def download_image(download_path, url, file_name):
    try:
        print('storing image '+file_name)
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)

        # Check if the image can be identified and is in a compatible format
        if image.format not in ["JPEG", "PNG"]:
            print(f"Skipping image with unsupported format: {url}")
            return

        file_path = os.path.join(download_path, file_name)  # Use os.path.join to ensure correct path

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)