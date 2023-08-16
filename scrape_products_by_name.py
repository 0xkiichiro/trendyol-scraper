import time
import json
from core import TrendyolScraper
import argparse

def scrape_product(product):
    # Initialize the scraper
    chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_driver_path = "/usr/local/bin/chromedriver"  # Provide the correct path
    scraper = TrendyolScraper(chrome_binary_path, chrome_driver_path)

    try:
        # Load the website
        scraper.load_website()

        # Close the pop-up if present
        scraper.close_homepage_popup_if_present()

        # Import credentials
        with open("userdata.json", "r") as userdata:
            userdata = json.load(userdata)

        # Log in
        scraper.login(userdata["email"], userdata["password"])

        # Search for a product
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

            if init_height == last_height:
                break

    finally:
        # Close the browser regardless of errors
        scraper.close_browser()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trendyol Scraper")
    parser.add_argument("product", type=str, help="Name of the product to search for")
    args = parser.parse_args()

    scrape_product(args.product)
