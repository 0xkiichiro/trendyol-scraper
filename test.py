from core import TrendyolScraper
import json

if __name__ == "__main__":
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

    # Search for a product
    product = "macbook"
    scraper.search_product(product)

    # Close product pop-up if present
    scraper.close_product_popup_if_present()

    # Get search results
    scraper.get_search_results(product)

    # Get document height
    height = scraper.get_document_height

    # Scroll down to load more products
    scraper.scroll_down()

    # Scrape product details
    scraper.scrape_product_details()

    # Close the browser
    scraper.close_browser()
