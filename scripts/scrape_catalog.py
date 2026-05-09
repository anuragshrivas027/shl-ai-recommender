import json
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.shl.com"

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_product_links():
    response = requests.get(CATALOG_URL, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    links = soup.find_all("a", href=True)

    product_links = []

    seen = set()

    for link in links:
        href = link["href"]

        text = link.get_text(strip=True)

        if "/products/" not in href:
            continue

        if not text:
            continue

        full_url = href

        if href.startswith("/"):
            full_url = BASE_URL + href

        if full_url in seen:
            continue

        seen.add(full_url)

        product_links.append({
            "name": text,
            "url": full_url
        })

    return product_links


def scrape_product_details(product):
    try:
        response = requests.get(product["url"], headers=headers, timeout=20)

        soup = BeautifulSoup(response.text, "lxml")

        paragraphs = soup.find_all("p")

        description = " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs[:8]
        )

        description = description[:1500]

        return {
            "name": product["name"],
            "url": product["url"],
            "description": description
        }

    except Exception as e:
        print("ERROR:", product["url"])
        print(e)

        return None


def main():
    products = get_product_links()

    print("FOUND:", len(products))

    final_data = []

    for index, product in enumerate(products):
        print(f"[{index+1}/{len(products)}] Scraping:", product["name"])

        details = scrape_product_details(product)

        if details:
            final_data.append(details)

        time.sleep(1)

    with open("data/catalog.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    print("\nDONE")
    print("TOTAL SAVED:", len(final_data))


if __name__ == "__main__":
    main()