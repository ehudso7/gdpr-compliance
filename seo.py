import requests
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='app.log')

def fetch_keywords(query="gdpr compliance"):
    try:
        response = requests.get(f"https://trends.google.com/trends/api/explore?hl=en-US&q={query}")
        keywords = response.json().get("keywords", [query])
        conn = sqlite3.connect("content.db")
        for kw in keywords:
            conn.execute("INSERT INTO keywords (keyword) VALUES (?)", (kw,))
        conn.commit()
        conn.close()
        logging.info(f"Keywords fetched: {keywords}")
        return keywords
    except Exception as e:
        logging.error(f"Keyword fetch failed: {str(e)}")
        return []

def generate_sitemap(posts):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for post in posts:
        sitemap += f'\n<url><loc>http://yourdomain.com/post/{post["id"]}</loc></url>'
    sitemap += '\n</urlset>'
    with open("sitemap.xml", "w") as f:
        f.write(sitemap)
    logging.info("Sitemap generated")
