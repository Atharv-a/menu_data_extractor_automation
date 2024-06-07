import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_images_from_zomato(driver, restaurant):
    items = get_dropdown_list_items(driver,restaurant)
    image_urls =[]

    it = 0
    while it<len(items):
        try:
            items[it].click()

            name_of_restaurant = driver.find_element(By.CLASS_NAME,'sc-7kepeu-0,sc-iSDuPN,fwzNdh').text
            if restaurant in name_of_restaurant:
                image_urls = get_image_url(driver)
            
            driver.back()
            if len(image_urls)>0: 
                break

            items = get_dropdown_list_items(driver,restaurant)
        except:
            print("execption has occured in extracting images from zomato")
        it+=1 
    return image_urls

def get_dropdown_list_items(driver, restaurant):
    input_box = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/header/nav/ul[2]/li[1]/div/div/div[3]/input')
    input_box.send_keys(restaurant)
    input_box.click()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'.sc-eqPNPO' ))

    )
    print("drop down loaded")
    items = driver.find_elements(By.CLASS_NAME,'sc-jotlie,jTjLpA')
    return items


def get_image_url(driver):
    try:
        menu_images = driver.find_element(By.CLASS_NAME,'sc-hBcjXN,cItQfd')
        div_with_text  = driver.find_elements(By.CLASS_NAME,'pgNiI')[0]
        text = div_with_text.text
        no_of_images = text.split()[0]
        no_of_images = int(no_of_images)

        menu_images.click()
        time.sleep(1)
        image_urls = []

        for image in range(no_of_images): 
            try:
                parent_div =  driver.find_element(By.CLASS_NAME,'dYvMzQ')
                divs = parent_div.find_elements(By.TAG_NAME,'div')
                div = divs[1]
                img =  div.find_element(By.TAG_NAME,'img')
                src = img.get_attribute('src')

                if src and 'http' in src and src not in image_urls:
                        image_urls.append(src)
                        print(f'got a url on image no: {image}')
                
                if image != no_of_images-1:
                    div = driver.find_element(By.CLASS_NAME,'jqbUZN')
                    i = div.find_element(By.TAG_NAME,'i')
                    i.click()
                    time.sleep(2)
            except Exception as e:
                print(e)
                continue

        print("url returned:",len(image_urls))        
        return image_urls
    
    except Exception as e:
        print(e)
        return []

