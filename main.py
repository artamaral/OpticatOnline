from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

# driver.title, to get the page's title
# driver.current_url, to get the current URL (this can be useful when there are redirections on the website and you need the final URL)


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

luk = 'BBZH'
valeo = 'BCRR'
sachs = 'BCLZ'

brands = ['BBZH','BCRR','BCLZ']
bvids = [18023,124259,7475,7375,17782,97035,7460,7464
    ,140915,881,7497,149438,7363,118663,148113,30277,885,146479
    ]

#[984,985,18774,7479,967,96891,966,28723,1193,7496,119034,30183,96704,96075,122905,147685,19047,143498,140682,1001,18222,
         #123078,28721,1192,30184,30185,18776,129872,129978,24558,129979,28724,7495,18775,18773,128182,18221,127805,128181,986,
# 7465,7478,127804,18267,130176,118904,96047,414,137008,7513,18220,127966,415,19048,30489,122906,130178,119471,19046,17795,122235,416
    # ,18266,118778,30470,29960,29868,17836,17794,346,140681,137051,118671,96791,137046,18490,122938,28722,128169,18489,130961,17793,128212
#     ,1002,145143,153546,147684,18020,96932,145144,145344,130117,130185,92761,3695,7507,127859,18483,149102,137052,318,400,130184,130236,29969
#     ,17790,143235,7491,134733,124258,140707,18752,128180,968,140918,123099,140917,399,18488,869,398,


#bvids = [28578,18869,18960,118456,127938,153020,29037,125003,130919,6656,29033,29137,95946,30137,128213,8544,19001,29031,18968,18979,30401,28851,18820,18232]
list =[]
i=1
for bvid in bvids:

    print(str(i) + "/" + str(len(bvids)))
    #print(str(i)+"/"+str(len(bvids)), end="\r")
    i= i+1
    for brand in brands:
        time.sleep(10)
        start_url = "https://www.opticatonline.com/search?cat=19933"
        time.sleep(10)
        #&bv=7958&region=mex

        url = start_url+'&bv=' + str(bvid) + '&region=usa' + '&b=' + brand


        if brand == 'BBZH':
            brand_name = "LUK"
        elif brand == 'BCRR':
            brand_name = 'Valeo'
        elif brand == 'BCLZ':
            brand_name = 'Sachs'

        driver.get(url)
        print(url)
        #print(driver.find_element(By.TAG_NAME, "h2").text)
        #print(driver.find_element(By.XPATH, "/html/body/section/div/div/div[2]/div/div/div").text)

        application = driver.find_element(By.TAG_NAME, "h2").text


        table = driver.find_element(By.XPATH, "/html/body/section/div/div/div[2]/div/div/div").text


        table =str(table).replace("\n" ," ")
        list.append([application,bvid,brand_name ,table])
        df = pd.DataFrame(list)
        df.to_csv('table.csv', mode='a', index=False, header=False)
        #print(list)

        time.sleep(35)

# df = pd.DataFrame(list)
# df.to_csv('table.csv', mode='a', index=False, header=False)
driver.quit()