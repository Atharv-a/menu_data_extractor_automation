import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from automation.image_url_by_google import get_images_from_google
from automation.image_url_by_zomato import get_images_from_zomato
from ocr.url_to_text import url_to_text
from genai import create_menu

load_dotenv()

path = os.environ.get("CHROMEDRIVER_PATH") 
service = Service(executable_path=path)

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument('--remote-debugging-port=9222')

def webscraping(restaurant,city):
    try:
        driver = webdriver.Chrome(service=service,options=options)
        print("ChromeDriver started successfully.")
        data = ""
        urls = []

        try:
            print("\n","="*5, 'finding images urls in zomato', "="*5, "\n")
            search_url = f"https://www.zomato.com/{city}"
            driver.get(search_url)
            driver.implicitly_wait(1)
            urls = get_images_from_zomato(driver, restaurant)
            
            if len(urls) == 0:
                raise Exception('No image found on zomato')
            
        except Exception as e:
            print("Exception:",e)
            print("\n","="*5, 'no image url extracted from zomato', "="*5, "\n")

            try:
                print("="*5, 'finding images urls in google', "="*5, "\n")
                search_query = f'{restaurant}+{city}+menu+card'
                search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
                driver.get(search_url)
                urls = get_images_from_google(driver, 2, 10)

            except Exception as e:
                print("Exception:",e)

        driver.quit()
        print("ChromeDriver quit successfully.")
        # print("\n","="*5, 'Extracting text from images', "="*5, "\n")

        for i, url in enumerate(urls):
            text = url_to_text(url)       
            if type(text) == str:
                data+=text
            
        create_menu(data, restaurant)
    except Exception as e:
        print("Exception:",e)


print("enter restaurant's name for which menu has to be extracted")
restaurant = input()
print("enter city in which restaurant is located")
city = input().lower()
webscraping(restaurant,city)