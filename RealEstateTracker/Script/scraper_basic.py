import requests
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd
import re


    # start = 0
    # inc = 3000
    # for key , value in data.items():
    #     driver.execute_script(f"window.scrollTo({start},{inc});")
    #     print(key)
    #     #data = driver.find_elements_by_class_name(value)
    #     data = driver.find_elements_by_xpath(f"//span[contains(@class,'{value}')]")
    #     print([d.text for d in data])
    #     time.sleep(2)
    #     start = inc
    #     inc += 3000

     #(By.xpath("//span[contains(@class,'re-CardPrice')]"))

    # data = driver.find_elements_by_class_name('re-CardPrice')
    # print([d.text for d in data])

base_url = "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/todas-las-zonas/l"
sort = "?sortType=scoring"

def page_builder():
    pages_list = []
    for i in range(400):
        pages_list.append(base_url+"/"+str(i+2)+sort)
    return pages_list


if __name__ == "__main__":


    all_pages = page_builder()

    # """MAKE CHROME UNDETECTABLE!"""
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",    ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    option.add_argument('--no-sandbox')
    option.add_argument('--start-maximized')
    #option.add_argument('--start-fullscreen')
    option.add_argument('--incognito')
    option.add_argument('--single-process')
    option.add_argument('--disable-dev-shm-usage')
    #option.add_argument('disable-infobars')

    """INITIALIZE CHROME DRIVER"""
    driver = webdriver.Chrome( "/Users/lucas/Downloads/chromedriver" , options = option)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    url = "https://www.fotocasa.es/es/comprar/viviendas/madrid-capital/todas-las-zonas/l?sortType=scoring"
    #driver.get(url)

    tags = {"price" : {"name" : "span" ,
                        "class_" : "re-CardPrice" },
            # "bathrooms" : {"name" : "span",
            #                     "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--bathrooms" } ,
             "rooms": {"name" : "li" ,
                             "class_" : "re-CardFeatures-feature"} ,
             "surface": {"name" : "li" ,
                             "class_" : "re-CardFeatures-feature"},
            # "elevator": {"name" : "span" ,
            #             "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--elevator"},
            # "heating": {"name" : "span" ,
            #                 "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--heating"},
            # "floor": {"name" : "span" ,
            #             "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--floor"},
            "neighborhood": {"name" : "a",
                             "class_" : "re-CardPackMinimal-info-container"}
        }

    columns = ["price",
                "rooms",
                "surface",
                "elevator",
                "heating",
                "floor",
                "neighborhood"]

    missing = ["elevator",
                "heating",
                "floor"]

    df = pd.DataFrame( columns = columns)

    for page in all_pages[200:240]:

        driver.get(page)

        if all_pages.index(page) == 0:
            accept = WebDriverWait(driver , 10).until(
                EC.element_to_be_clickable(
                (  By.CSS_SELECTOR ,
                    "button[data-testid='TcfAccept']")
                )
                    ).click()


        start = 0
        inc = 500
        for i in range(25):
            driver.execute_script(f"window.scrollTo({start},{inc});")
            start = inc
            inc += 500
            time.sleep(0.2)


        soup = BeautifulSoup( driver.page_source , 'html.parser')
        data = defaultdict(list)

        for soupie in soup.find_all("div" , class_ = "re-CardPackMinimal-info"):
            room_surface = soupie.find_all("li", class_ = "re-CardFeatures-feature")
            if len(room_surface) > 2:
                room = room_surface[0].string
                surface = room_surface[2].string
            else:
                room = -1
                surface = -1
            price = soupie.find(**tags.get("price")).string
            neighborhood = soupie.find(**tags.get("neighborhood")).attrs["title"]
            elevator = ""
            heating = ""
            floor = ""
            vals = {"price":price,
                    "rooms": room,
                    "surface": surface,
                    "neighborhood": neighborhood,
                    "elevator": elevator,
                    "heating": heating,
                    "floor": floor}

            for key, value in vals.items():

                data[key].append(value)

            print("*"*20 + "UPDATE" + "*"*20)
            print(data)


        print("*"*20 + "FINAL FORMAT" + "*"*20)
        df = pd.concat( [ pd.DataFrame(data)  , df ] , axis = 0 )

    df.to_csv("/Users/lucas/code/llenci/real-estate-tracker/raw_data/real_estate200.csv")
    print(df)




# for i in range(len(lst)):
#     if re.match("hab", i):
#         rooms = i.string
#     elif re.match("m²", i):
#         surface = i.string
#     elif re.match("Cale", i)
