import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('trendyol.sqlite')

# Create a cursor object
cur = conn.cursor()

# Execute the DROP TABLE command
cur.execute("DROP TABLE IF EXISTS scraped_products")
cur.execute("DROP TABLE IF EXISTS top_seller_products")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("dropped table")