import sys
import os
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.abspath(current_directory))
sys.path.append(parent_directory)

from processheet.sheetprocessor import writeShopifyDomain,dataFilter

def fetchShopifyDomain(sheetNumber):
    data = dataFilter(sheetNumber)
    if not data:
        return "Waiting For Data !!!"
    for merchantUrl in data:
        try:
            os.remove(ChromeDriverManager().install())
        except:
            pass
        try:
            shopify_domain = merchantUrl["shopify_domain"]
            if not shopify_domain:
                merchant_url = merchantUrl["merchant_url"]                
                if not merchant_url.startswith("https://"):
                    merchant_url = "https://" + merchant_url
                    chr_options = Options()
                    chr_options.add_argument("--disable-popup-blocking")
                    chr_options.add_argument('--headless')
                    chr_options.add_argument('--disable-gpu')
                    driver = webdriver.Chrome(
                        service=Service(ChromeDriverManager().install()), options=chr_options
                    )
                    driver.get(merchant_url)
                    time.sleep(3)
                    domainName = driver.execute_script("return Shopify.shop")
                    dataInArray = {"merchant_name": merchantUrl["merchant_name"], "domain_name": domainName}
                    writeShopifyDomain(dataInArray, sheetNumber)                
                else:
                    dataInArray = {"merchant_name": merchantUrl["merchant_name"], "domain_name": "Invalid URL"}
                    writeShopifyDomain(dataInArray, sheetNumber)
            else:
                print("waiting For Data")
        except Exception as e:
            dataInArray = {"merchant_name": merchantUrl["merchant_name"], "domain_name": "Failed"}
            writeShopifyDomain(dataInArray, sheetNumber)
            print("Domain Update Failed")




