import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_images_from_zomato(driver,restaurant):
    item_number = 0
    next_iteration = get_dropdown_list_item(driver,restaurant,item_number)
    
    wait = WebDriverWait(driver,10)
    image_urls =[]

    try:
        while next_iteration and item_number<10:
            print(f'dropdown item: {item_number+1} selected')
            name_of_restaurant = None

            try:
                name_of_restaurant = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/main/div/section[1]/div/h1/a/span'))).text

                if restaurant in name_of_restaurant:
                    image_urls = get_image_url(driver)
                    if len(image_urls)>0: 
                        break
            except Exception as e:
                print(e)
            
            driver.back()

            item_number+=1
            next_iteration = get_dropdown_list_item(driver,restaurant,item_number)
    except Exception as e:
        print(e)
    return image_urls 


def get_dropdown_list_item(driver, restaurant,item_number):
    try:
        wait = WebDriverWait(driver,10)

        input_box = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/header/nav/ul[2]/li[1]/div/div/div[3]/input')))

        input_box.clear()
        input_box.send_keys(restaurant)
        input_box.click()

        driver.implicitly_wait(2)
        item = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"sc-jtHxuu")))[item_number]
        item.click()

        return True
    
    except Exception as e:
        print(e)
        return False
        
    
def get_image_url(driver):
    it = 1
    image_urls = []
    wait = WebDriverWait(driver,10)
    try:
        while it<=5:
            menu_images = wait.until(EC.presence_of_element_located((By.XPATH,f"/html/body/div[1]/div/main/div/section[4]/section/section/article[1]/section[1]/section[2]/section/div/section/section[{it}]/div/div[3]")))
            text  = driver.find_element(By.XPATH,f"/html/body/div[1]/div/main/div/section[4]/section/section/article[1]/section[1]/section[2]/section/div/section/section[{it}]/div/p").text

            no_of_images = text.split()[0]
            no_of_images = int(no_of_images)
                
            menu_images.click()
            print(no_of_images)

            for image in range(no_of_images): 
                try:
                    img =wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/main/div/section[4]/section/section/article[1]/section[1]/section[2]/div[2]/div[2]/img')))
                    src = img.get_attribute('src')

                    if src and 'http' in src and src not in image_urls:
                            image_urls.append(src)
                            print(f'got a url on image no: {image}')
                    
                    if image != no_of_images-1:
                        i=driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/section[4]/section/section/article[1]/section[1]/section[2]/div[2]/div[5]/i')
                        i.click()
                except Exception as e:
                    print(e)
                    continue
            close_button = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div/section[4]/section/section/article[1]/section[1]/section[2]/div[2]/div[1]/i")
            close_button.click()
            it+=1

        print("url returned:",len(image_urls))        
        return image_urls
    
    except Exception as e:
        print(e)
    return image_urls 

