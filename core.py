from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import sqlite3
import time
from db import create_products_table, create_top_seller_products_table

class TrendyolScraper:

    # Initialize the scraper
    def __init__(self, chrome_binary_path = None, chrome_driver_path = None):
        self.URL = "https://www.trendyol.com/"
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_binary_path
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.SLEEP_TIME = 2
        time.sleep(self.SLEEP_TIME)
        create_products_table()
        create_top_seller_products_table()

    # Load the website
    def load_website(self):
        self.driver.maximize_window()
        self.driver.get(self.URL)

    # Close homepage pop-up if present
    def close_homepage_popup_if_present(self):
        try:
            pop_up = self.driver.find_element(By.CLASS_NAME, "homepage-popup")
            if pop_up:
                modal_close = self.driver.find_element(By.CLASS_NAME, "modal-close")
                modal_close.click()
                print("Pop-up closed on the homepage.")
        except:
            print("No pop-up on the homepage.")

    # Log in
    def login(self, email, password):
        sign_in_button = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[1]/div[1]/p")
        sign_in_button.click()
        time.sleep(self.SLEEP_TIME)
        print("Navigated to the login page.")

        email_field = self.driver.find_element(By.ID, "login-email")
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.ID, "login-password-input")
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(self.SLEEP_TIME)
        print("Logged in successfully.")


    # ---------------------------------------------------------------
    # Top sellers ARC
    # Navigate to top sellers page
    def navigate_to_top_sellers(self):
        nav = self.driver.find_element(By.CLASS_NAME, "main-nav")
        nav_buttons = nav.find_elements(By.CLASS_NAME, "tab-link")
        top_seller_button = nav_buttons[9]
        top_seller_button.click()
        print("Navigated to top sellers page")

    # Navigate to all categories (normally starts with woman)
    def set_top_seller_category_to_all(self):
        nav = self.driver.find_element(By.CLASS_NAME, "navigation-section")
        all_categories_button = nav.find_element(By.CLASS_NAME, "navigation-section-breadcrumb-item")
        all_categories_button.click()

    # Get all categories for top sellers
    def get_all_categories_top_sellers(self):
        categories = self.driver.find_element(By.XPATH, """//*[@data-testid="sliderList"]""")
        self.children = categories.find_elements(By.XPATH, './*')
        self.child_texts = []
        for child in self.children:
            self.child_texts.append(child.text.lower())
        print(self.child_texts)
        return self.child_texts

    # Set the category for the top sellers
    def set_top_seller_category(self, category: str):
        category_index = self.child_texts.index(category.lower())
        self.children[category_index].click()
        self.category = category
        print(f"Navigated to {category}")

    # Get number of products in the page
    def get_nu_of_top_seller_in_category(self):
        wrapper = self.driver.find_element(By.CLASS_NAME, "best-seller")
        products = wrapper.find_elements(By.CLASS_NAME, "product-card")
        print(len(products))
    
    # Get product details
    def scrape_top_seller_product_details(self):
        wrapper = self.driver.find_element(By.CLASS_NAME, "best-seller")
        products = wrapper.find_elements(By.CLASS_NAME, "product-card")
        for product in products:
            brand_name = product.find_element(By.CLASS_NAME, "product-brand").text
            product_name = product.find_element(By.CLASS_NAME, "product-name").text
            product_price = product.find_element(By.CLASS_NAME, "prc-box-dscntd").text
            product_picture = product.find_element(By.CLASS_NAME, "product-img").get_attribute("src")
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Check rating count
            try:
                product_rating_count = int(product.find_element(By.CLASS_NAME, "ratingCount").text.replace("(", "", -1).replace(")", "", -1))
            except:
                product_rating_count = 0

            # Store product data in DB
            self.store_product_in_database(brand_name, product_name, product_price, product_picture, product_rating_count, product_link, self.category, True)
        pass

    # ---------------------------------------------------------------
    # Scrape any product ARC
    # Search for a product
    def search_product(self, product):
        search_bar = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/input")
        self.searched_keyword = product
        search_bar.send_keys(product)
        search_bar.send_keys(Keys.ENTER)

    # Close product pop-up if present
    def close_product_popup_if_present(self):
        try:
            pop_up = self.driver.find_element(By.CLASS_NAME, "popup")
            if pop_up:
                overlay = self.driver.find_element(By.CLASS_NAME, "overlay")
                overlay.click()
                print("Pop-up closed on the product screen.")
        except:
            print("No pop-up on the product screen.")

    # Get number of search results
    def get_search_results(self, product):
        self.product = product
        nu_of_results = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/div").text.split(" ")[3]
        print(f"Results for {product} => {nu_of_results}")
        self.set_nu_of_product_per_page()

    # Get initial document height
    def get_init_document_height(self):
        init_height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        return init_height

    # Scroll down
    def scroll_down(self):
        init_height = self.get_init_document_height()
        total_height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        target_height = int(total_height - init_height * 0.25)
        self.driver.execute_script(f"window.scrollTo(0, {total_height});")
        time.sleep(self.SLEEP_TIME / 2)
        self.driver.execute_script(f"window.scrollTo(0, {target_height});")
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        time.sleep(self.SLEEP_TIME / 2)

    def get_document_height(self):
        document_height = self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        return document_height

    # Store product data in DB        
    def store_product_in_database(self, brand_name, product_name, product_price, product_picture, product_rating_count, product_link, searched_keyword, top_seller=None):
        conn = sqlite3.connect('trendyol.sqlite')
        cursor = conn.cursor()
        if top_seller is False:

            # Check if product already in DB or not => compare product_link s
            cursor.execute('SELECT * FROM scraped_products WHERE product_link = ?', (product_link,))
            existing_product = cursor.fetchone()

            if not existing_product:
                sql_query = '''INSERT INTO scraped_products (brand_name, product_name, product_price, product_picture, product_rating_count, product_link, searched_keyword)
                            VALUES (?, ?, ?, ?, ?, ?, ?)'''

                cursor.execute(sql_query, (brand_name, product_name, product_price, product_picture, product_rating_count, product_link, searched_keyword))
                print("pushed", product_name, "into DB")

            else:
                print("passed", product_link)

        elif top_seller is True:

            # Check if product already in DB or not => compare product_link s
            cursor.execute('SELECT * FROM top_seller_products WHERE product_link = ?', (product_link,))
            existing_product = cursor.fetchone()

            if not existing_product:
                sql_query = '''INSERT INTO top_seller_products (brand_name, product_name, product_price, product_picture, product_rating_count, product_link, category)
                            VALUES (?, ?, ?, ?, ?, ?, ?)'''

                cursor.execute(sql_query, (brand_name, product_name, product_price, product_picture, product_rating_count, product_link, self.category))
                print("pushed", product_name, "into DB")

            else:
                print("passed", product_link)


        conn.commit()
        conn.close()

    # Set number of items per page
    def set_nu_of_product_per_page(self):
        products_wrapper = self.driver.find_element(By.CLASS_NAME, "prdct-cntnr-wrppr")
        products = products_wrapper.find_elements(By.CLASS_NAME, "p-card-wrppr")
        print(f"{len(products)} {self.product}'s per page")
        self.product_per_page = len(products)

    # Scrape product details
    def scrape_product_details(self):
        products_wrapper = self.driver.find_element(By.CLASS_NAME, "prdct-cntnr-wrppr")
        products = products_wrapper.find_elements(By.CLASS_NAME, "p-card-wrppr")

        for product in products[-self.product_per_page:]:
            brand_name = product.find_element(By.XPATH, "//div[1]/a/div[2]/div[1]/div/div/span[1]").text
            product_name = product.find_element(By.CLASS_NAME, "prdct-desc-cntnr-name").text
            product_price = product.find_element(By.CLASS_NAME, "prc-box-dscntd").text
            product_picture = product.find_element(By.CLASS_NAME, "p-card-img").get_attribute("src")
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            # TODO check for rating, if possible from the same page W.I.P.

            # Check rating count
            try:
                product_rating_count = int(product.find_element(By.CLASS_NAME, "ratingCount").text.replace("(", "", -1).replace(")", "", -1))
            except:
                product_rating_count = 0

            # Store product data in DB
            self.store_product_in_database(brand_name, product_name, product_price, product_picture, product_rating_count, product_link, self.searched_keyword, False)
            

    def close_browser(self):
        self.driver.quit()