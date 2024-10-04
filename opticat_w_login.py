from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import lxml
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrapeInfo():
    username = "artamaral@yahoo.com.br"
    password = "Artamaral@123"

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get("https://web.tecalliance.net/opticat/qa/login")


    time.sleep(5)
    username_field = driver.find_element(By.ID, "userName")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)
    time.sleep(3)
    button = driver.find_element(By.ID, "ppms_cm_agree-to-all")
    button.click()
    password_field.send_keys(Keys.RETURN)

    df = pd.DataFrame()

    """
    Master Cylinder
    https://web.tecalliance.net/opticat/qa/parts/ap/assigned?targetId=0&parentAssemblyGroupId=20&assemblyGroupId=183&partTypeId=1996&groups=1996
    
    Slave Cylinder
    https://web.tecalliance.net/opticat/qa/parts/ap/assigned?targetId=0&parentAssemblyGroupId=20&assemblyGroupId=183&partTypeId=2044&groups=2044
    
    Clutch Release bearing and slave cylinder assembly
    https://web.tecalliance.net/opticat/qa/parts/ap/assigned?targetId=0&parentAssemblyGroupId=20&assemblyGroupId=183&partTypeId=2020&groups=20200
    
    Clutch cable
    https://web.tecalliance.net/opticat/qa/parts/ap/assigned?targetId=0&parentAssemblyGroupId=20&assemblyGroupId=183&partTypeId=1972&groups=1972
    
    Clutch kits
    https://web.tecalliance.net/opticat/qa/parts/ap/assigned?targetId=0&parentAssemblyGroupId=20&assemblyGroupId=442&partTypeId=1993&groups=1993#
    
    """


    driver.get(
        "")


    all_pn = []
    all_brand = []
    all_productType = []

    while True:

        try:

            # Aguarde alguns segundos para que a página seja carregada
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, features='lxml')
            allData = soup.find_all(name='div', attrs='ag-center-cols-container')


            all_rowEven = soup.find_all(name='div', attrs='ag-cell-content')

            for row in all_rowEven:
                #print(row)
                #print(row.get_text())
                for pn in row.find_all(name='div', attrs='text-truncate'):
                    all_pn.append(pn.get_text())


                for brand in row.find_all(name='span', attrs='font-weight-bold'):
                    all_brand.append(brand.get_text())
                    break

                for productType in row.find_all(name='span', attrs='generic-article'):
                    all_productType.append(productType.get_text())

            print("nextPage")
            next_productList = driver.find_element(By.CLASS_NAME, "ta-icon-right-open")
            next_productList.click()
            time.sleep(1)

        except:
            print("Break")
            break

    df['pn'] = all_pn
    df['Brand'] = all_brand
    df['Type of product'] = all_productType

    df.to_csv('opticat.csv')

    #
    #
    # for data in allData:
    #
    #     #print(data)
    #     rowEven = data.find(name='div', attrs='ag-row-even')
    #     rowOdd = data.find(name='div', attrs='ag-row-odd')
    #
    #     pn = data.find(name='div', attrs='text-truncate text-primary')
    #     brand = data.find(name='a', attrs='ont-weight-bold')
    #     productType = data.find(name='a', attrs='generic-article')
    #
    #     #print(pn, brand, productType)
    #
    #
    # while True:
    #     try:
    #         print("nextPage")
    #         next_productList = driver.find_element(By.CLASS_NAME, "ta-icon-right-open")
    #         next_productList.click()
    #         time.sleep(5)
    #     except:
    #         print("Break")
    #         break


if __name__ == "__main__":
    scrapeInfo()

