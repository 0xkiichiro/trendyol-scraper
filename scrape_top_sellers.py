import time
import json
import argparse
from core import TrendyolScraper

def scrape_top_sellers(category):
    # Initialize the scraper
    firefox_binary_path = "/Applications/Firefox.app/Contents/MacOS/firefox"
    gecko_driver_path = "~/usr/local/bin/geckodriver"
    scraper = TrendyolScraper(firefox_binary_path, gecko_driver_path)

    # Load the website
    scraper.load_website()

    # Close the pop-up if present
    scraper.close_homepage_popup_if_present()

    # Import credentials
    with open("userdata.json", "r") as userdata:
        userdata = json.load(userdata)

    # Log in
    scraper.login(userdata["email"], userdata["password"])

    # Navigating to the top sellers page
    scraper.navigate_to_top_sellers()

    # Switching default category to all
    scraper.set_top_seller_category_to_all()

    # Get all categories in a list
    scraper.get_all_categories_top_sellers()

    # Import CLI args
    category = args.category

    # Move to desired category
    scraper.set_top_seller_category(category)
    time.sleep(2)

    # Get number of products in the page
    scraper.get_nu_of_top_seller_in_category()

    # Scrape product details
    scraper.scrape_top_seller_product_details()

    # Close the browser
    scraper.close_browser()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trendyol Scraper")
    parser.add_argument("category", type=str, help="Category of top sellers", default="erkek")
    args = parser.parse_args()

    scrape_top_sellers(args.category)