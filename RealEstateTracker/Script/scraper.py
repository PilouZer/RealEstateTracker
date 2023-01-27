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
            "bathrooms" : {"name" : "span",
                                "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--bathrooms" } ,
            "surface": {"name" : "span" ,
                            "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--surface"} ,
            "rooms": {"name" : "span" ,
                        "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--rooms"},
            "elevator": {"name" : "span" ,
                        "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--elevator"},
            "heating": {"name" : "span" ,
                            "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--heating"},
            "floor": {"name" : "span" ,
                        "class_" : "re-CardFeaturesWithIcons-feature-icon re-CardFeaturesWithIcons-feature-icon--floor"},
            "neighborhood": {"name" : "a" }
        }

    columns = ["price",
                "rooms",
                "surface",
                "elevator",
                "heating",
                "floor",
                "neighborhood"]

    df = pd.DataFrame( columns = columns)

    for page in all_pages:

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

        for soupie in soup.find_all("div" , class_ = "re-CardPackPremium-info"):
            for feature in columns:
                try:
                    temp = soupie.find( **tags.get(feature) )
                    if feature == "neighborhood":
                        form = temp.attrs["title"]
                    else:
                        form = temp.string

                except:
                    form = temp
                finally:
                    data[feature].append(form)

            print("*"*20 + "UPDATE" + "*"*20)
            print(data)


        print("*"*20 + "FINAL FORMAT" + "*"*20)
        df = pd.concat( [ pd.DataFrame(data)  , df ] , axis = 0 )

    df.to_csv("/Users/lucas/code/llenci/real-estate-tracker/raw_data/real_estate.csv")
    print(df)
