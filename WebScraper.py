from re import A
from ssl import Options 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdrivermanager.chrome import ChromeDriverManager
import pandas as pd



class Item():
    def __init__(self, title, price):
        self.title = title
        self.price = price

class Scraper:
    def article(self,name):
        count = 1
        page = 1
        nextPage = 10
        maxItems = 10
        a = []

        url = "https://www.amazon.com.mx/s?k=" + name + "&page=" + str(page)
        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Google Chrome .app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = '/Applications/chromedriver'
        browser = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
        #browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.maximize_window()
        browser.get(url)
        browser.set_page_load_timeout(10)
        
        while True:
            try:
                if nextPage*page > maxItems:
                    break

                if count > nextPage:
                    count=1
                    page+=1
                
                xPathItem = '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[' + str(count) + ']/div/div/div/div/div/div/div[2]/div[1]/h2/a/span'
                title = browser.find_element_by_xpath(xPathItem)
                itemText = title.get_attribute("innerHTML").splitlines()[0]
                title.click()

                xPathPrice = '//*[@id="corePrice_feature_div"]/div/span/span[2]/span[2]'
                price = browser.find_element_by_xpath(xPathPrice)
                priceText = price.get_attribute("innerHTML")


                url = "https://www.amazon.com.mx/s?k=" + name + "&page=" + str(page)
                browser.get(url)
                browser.set_page_load_timeout(10)

                info = Item(itemText, priceText)
                a.append(info)

                count+=1

            
            except Exception as e:
                print('Exception', e)
                count+=1

                if nextPage*page > maxItems:
                    break

                if count > nextPage:
                    count=1
                    page+=1
                
                url = "https://www.amazon.com.mx/s?k=" + name + "&page=" + str(page)
                browser.get(url)
                browser.set_page_load_timeout(10)
    
        browser.close()

        return a 


fetcher = Scraper()

df_results = pd.DataFrame()


for article in fetcher.article('iphone 11'):
    df_results = pd.concat([df_results,pd.DataFrame([article.title , article.price]).T])


df_results.columns=['item','price']
df_results.to_csv('results.csv')
    

    




 


