import os
import time
import requests
from bs4 import BeautifulSoup
from services.storage import Storage
from services.cache import Cache
from models.product import Product
import base64


class ScraperService:
    """Scrapper class to scrape the web page."""
    def __init__(self, settings):
        self.settings = settings
        self.storage = Storage()
        self.cache = Cache()
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def fetch_page(self, url, retries=3, delay=5):
        """Fetch the content of a webpage with retries on failure."""
        for _ in range(retries):
            try:
                response = requests.get(url, proxies=self.settings.proxy, headers=self.headers)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException:
                time.sleep(delay)
        raise Exception(f"Failed to fetch {url} after {retries} retries")

    def scrape_page(self, url):
        """Scrape product data from a single page."""
        page_content = self.fetch_page(url)
        soup = BeautifulSoup(page_content, "html.parser")
        products = []

        for item in soup.select("li.product"):
            try:
                # Extract product title
                title = item.select_one(".woo-loop-product__title").text.strip()

                # Extract product price
                price_text = item.select_one(".woocommerce-Price-amount").text.strip().replace("₹", "").replace(",", "")
                price = float(price_text)

                # Extract product image URL
                image_url = item.select_one(".mf-product-thumbnail img")["data-lazy-src"]

                # Download and save the image
                image_path = self.download_image(image_url)

                # Create Product instance
                product = Product(product_title=title, product_price=price, path_to_image=image_path)

                # Save to database and cache only if not already cached
                if not self.cache.is_cached(product):
                    self.storage.save_product(product)
                    self.cache.add_to_cache(product)
                    products.append(product)

            except Exception as e:
                print(f"Error parsing product: {e}")

        return products

    import base64

    def download_image(self, url):
        """Download an image from a given URL or handle data URIs."""
        if url.startswith("data:"):
            # Handle data URIs
            header, encoded = url.split(",", 1)
            file_extension = header.split(";")[0].split("/")[-1]  # Extract file extension (e.g., svg, png)
            os.makedirs("static/images", exist_ok=True)
            filename = os.path.join("static/images", f"image_{int(time.time())}.{file_extension}")

            with open(filename, "wb") as f:
                f.write(base64.b64decode(encoded))
            return filename
        else:
            # Handle standard URLs
            response = requests.get(url, stream=True)
            response.raise_for_status()
            os.makedirs("static/images", exist_ok=True)
            filename = os.path.join("static/images", os.path.basename(url))

            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename

    def run_scraping(self):
        """Run the scraper across all pages and return the total number of products scraped."""
        total_products = 0

        for page in range(1, self.settings.page_limit + 1):
            url = f"{self.settings.url}page/{page}/"
            print(f"Scraping page: {url}")
            products = self.scrape_page(url)
            total_products += len(products)

        print(f"Total products scraped: {total_products}")
        return total_products
