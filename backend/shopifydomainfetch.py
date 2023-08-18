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

print(current_directory)

from processheet.sheetprocessor import fetchSheetData,writeShopifyDomain

def fetchShopifyDomain():
    data = fetchSheetData(0)
    for merchantUrl in data:
        try:
            if len(merchantUrl["shopify_domain"]) < 1 and len(merchantUrl["shopify_domain"]) == 0:
                if not merchantUrl["merchant_url"].startswith("https://"):
                    merchantUrl["merchant_url"] = "https://" + merchantUrl["merchant_url"]
                    chr_options = Options()
                    chr_options.add_argument ("--disable-popup-blocking")
                    chr_options.add_argument('--headless') 
                    chr_options.add_argument('--disable-gpu')
                    driver = webdriver.Chrome (service=Service (ChromeDriverManager ().install ()), options=chr_options)
                    driver.get(merchantUrl["merchant_url"])
                    time.sleep(3)
                    domainName = driver.execute_script("return Shopify.shop")
                    dataInArray = {"merchant_name":merchantUrl["merchant_name"],"domain_name":domainName}
                    writeShopifyDomain(dataInArray,0)
                else:
                    print("Passed URL format is incorrect")
        except Exception as e:
            dataInArray = {"merchant_name":merchantUrl["merchant_name"],"domain_name":"Failed"}
            writeShopifyDomain(dataInArray,0)
    if len(dataInArray) > 0:
        driver.quit()
        return dataInArray
    else:
        print("No List to Update")
    

    
    

    
fetchShopifyDomain()   
