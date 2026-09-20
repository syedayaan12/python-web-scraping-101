import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

all_books = []

print("Multi-page scraping start ho rhi hai...")

for page in range(1, 4):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    print(f"Fetching Page {page}...")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")
        
        for book in books:
            title = book.h3.a["title"]
            price = book.select_one("p.price_color").text.replace("Â", "")
            stock = book.select_one("p.instock.availability").text.strip()
            
            all_books.append({
                "Page": page,
                "Book Title": title,
                "Price": price,
                "Availability": stock
            })
            
        time.sleep(1)

df = pd.DataFrame(all_books)
csv_filename = "scraped_books_multi_page.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"\nSUCCESS! {len(df)} books exported to '{csv_filename}'.")