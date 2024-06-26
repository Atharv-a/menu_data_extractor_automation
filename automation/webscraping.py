from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from automation.image_url_by_google import get_images_from_google
from automation.image_url_by_zomato import get_images_from_zomato
from ocr.url_to_text import url_to_text


options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

async def webscraping(restaurant='Fiona'):
    driver = webdriver.Chrome(options=options)
    print("ChromeDriver started successfully.")
    data = []
    urls = []

    try:
        print("\n","="*5, 'finding images urls in zomato', "="*5, "\n")
        search_url = "https://www.zomato.com/mumbai"
        driver.get(search_url)
        urls = get_images_from_zomato(driver, restaurant)
        
        if len(urls) == 0:
            raise Exception('No image found on zomato')
        
    except Exception as e:
        print("\n","="*5, 'no image url extracted from zomato', "="*5, "\n")

        try:
            print("="*5, 'finding images urls in google', "="*5, "\n")
            search_query = f'{restaurant}+mumbai+menu+card'
            search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
            driver.get(search_url)
            urls = get_images_from_google(driver, 2, 10)

        except Exception as e:
            print(f"An error occurred: {e}")

    print("\n","="*5, 'Extracting text from images', "="*5, "\n")

    for i, url in enumerate(urls):
        print(f"getting text for image number: {i}")
        text = await url_to_text(url)

        data.append(text)

    driver.quit()
    print("ChromeDriver quit successfully.")
    return data
