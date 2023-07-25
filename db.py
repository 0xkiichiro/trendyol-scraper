import sqlite3

def create_products_table():
    conn = sqlite3.connect('trendyol.sqlite')
    cursor = conn.cursor()

    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='scraped_products';''')
    table_exists = cursor.fetchone()

    # If the table does not exist, create it
    if not table_exists:
        sql_query = '''CREATE TABLE scraped_products (
            id INTEGER PRIMARY KEY,
            brand_name TEXT,
            product_name TEXT,
            product_price TEXT,
            product_picture TEXT,
            product_rating_count INTEGER,
            product_link TEXT
        )'''
        cursor.execute(sql_query)

    conn.commit()
    conn.close()
