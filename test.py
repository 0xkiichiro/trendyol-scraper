import time
import json
import argparse
from core import TrendyolScraper

if __name__ == "__main__":
    # enable CLI args for product
    parser = argparse.ArgumentParser(description="Trendyol Scraper")
    parser.add_argument("product", type=str, help="Name of the product to search for")
    args = parser.parse_args()
    # Initialize the scraper
    chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_driver_path = "~/usr/local/bin/chromedriver"
    scraper = TrendyolScraper(chrome_binary_path, chrome_driver_path)

    # Load the website
    scraper.load_website()

    # Close the pop-up if present
    scraper.close_homepage_popup_if_present()

    # Import credentials
    with open("userdata.json", "r") as userdata:
        userdata = json.load(userdata)

    # Log in
    scraper.login(userdata["email"], userdata["password"])

    # Testing new features
    scraper.navigate_to_top_sellers()
    time.sleep(5)
    scraper.set_top_seller_category_to_all()
    time.sleep(5)
    scraper.get_all_categories_top_sellers()

    # Search for a product
    product = args.product
    scraper.search_product(product)

    # Close product pop-up if present
    scraper.close_product_popup_if_present()

    # Get search results
    scraper.get_search_results(product)

    # Get document height
    # Scroll down to load more products
    while True:
        # Scrape product details
        scraper.scrape_product_details()
        init_height = scraper.get_document_height()
        scraper.scroll_down()
        last_height = scraper.get_document_height()

        if init_height is last_height:
            break

    # Close the browser
    scraper.close_browser()