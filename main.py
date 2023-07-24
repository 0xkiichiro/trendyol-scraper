from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# initialize webdriver
URL = "https://www.trendyol.com/"
chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
driver = webdriver.Chrome(executable_path="~/usr/local/bin/chromedriver", options=options)
driver.maximize_window()
driver.get(URL)
SLEEP_TIME = 2

#wait for lazy loading
time.sleep(SLEEP_TIME)

#import credentials
with open("userdata.json", "r") as userdata:
    userdata = json.load(userdata)

#check for pop up
try:
    pop_up = driver.find_element(By.CLASS_NAME, "homepage-popup")
    modal_close = driver.find_element(By.CLASS_NAME, "modal-close")
    modal_close.click()
    print("pop up closed in homescreen")
except:
    print("no pop up in homescreen")

#click to sign in
sign_in_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[1]/div[1]/p")
sign_in_button.click()
time.sleep(2)
print("navigated to login page")

#enter credentials
email_field = driver.find_element(By.ID, "login-email")
email_field.send_keys(userdata["email"])
password_field = driver.find_element(By.ID, "login-password-input")
password_field.send_keys(userdata["password"])
password_field.send_keys(Keys.ENTER)
time.sleep(SLEEP_TIME)
print("logged in")

#click on search bar
search_bar = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/input")
#line below will be dynamically sent
product = "suwen"
search_bar.send_keys(product)
search_bar.send_keys(Keys.ENTER)

#inform user of the dataset
nu_of_results = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/div").text.split(" ")[3]
print("results for", product, "=>", nu_of_results)

#check for pop-up
try:
    pop_up = driver.find_element(By.CLASS_NAME, "popup")
    overlay = driver.find_element(By.CLASS_NAME, "overlay")
    overlay.click()
    print("pop up closed in product screen")
except:
    print("no pop up in product screen")

#capture product cards
products_wrapper = driver.find_element(By.CLASS_NAME, "prdct-cntnr-wrppr")
products = products_wrapper.find_elements(By.CLASS_NAME, "p-card-wrppr")
print(len(products), f"{product}' s this page")

#scrape product details
time.sleep(SLEEP_TIME)
for product in products:
    brand_name = product.find_element(By.XPATH, "//div[1]/a/div[2]/div[1]/div/div/span[1]").text
    product_name = product.find_element(By.CLASS_NAME, "prdct-desc-cntnr-name").text
    product_price = product.find_element(By.CLASS_NAME, "prc-box-dscntd").text
    product_picture = product.find_element(By.CLASS_NAME, "p-card-img").get_attribute("src")
    #TODO check for rating, if possible from same page W.I.P.

    # check rating count
    try:
        product_rating_count = product.find_element(By.CLASS_NAME, "ratingCount").text
    except:
        product_rating_count = None

    print(brand_name, product_name)
    print(product_price)
    print(product_picture)
    print(product_rating_count, "people commented this item")
    
    #TODO store product data

#TODO scroll down (send_keys(Keys.DOWN))