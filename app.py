from core import TrendyolScraper
from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__, template_folder = '.')
scraper = TrendyolScraper()

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('trendyol.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/products/<searched_keyword>', methods=['GET', 'POST'])
def scrape_tweets(searched_keyword: str):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            data = scraper.scrape_product(searched_keyword)
            response = jsonify(data)
            return response
        except requests.exceptions.RequestException as e:
            return e
        
    elif request.method == 'GET':
        cursor = conn.execute(f'''
            SELECT * FROM scraped_products
            WHERE searched_keyword == "@{searched_keyword}"
        ''')
        
        products = [
        {
            'id': row[0],
            'brand_name': row[1],
            'product_name': row[2],
            'product_price': row[3],
            'product_picture': row[4],
            'product_rating_count': row[5],
            'product_link': row[6],
            'searched_keyword': row[7]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    if products:
        return jsonify(products)
    else:
        return jsonify([])
if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0', port=5001)