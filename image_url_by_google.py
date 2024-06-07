import time
from selenium.webdriver.common.by import By

def get_images_from_google(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    image_urls = set()

    print('finding urls for images')
    processed_thumbnails = 0
    while len(image_urls)  < max_images:
        scroll_down(driver)
        thumbnails = driver.find_elements(By.CSS_SELECTOR, '.eA0Zlc')

        for img in thumbnails[processed_thumbnails: ]:
            processed_thumbnails+=1
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = driver.find_elements(By.CSS_SELECTOR, '.sFlh5c, .pT0Scc, .iPVvYb')

            for image in images:
                src = image.get_attribute('src')

                if src and 'http' in src and src not in image_urls:
                    image_urls.add(src)
                    print(f"Found {len(image_urls)}")

                if len(image_urls)>=max_images:
                    return image_urls
                    
    return list(image_urls)
