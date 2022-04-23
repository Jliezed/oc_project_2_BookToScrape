import requests
from bs4 import BeautifulSoup
import csv
from functions import parse_links_products_pages, parse_product_page, save_image


"""
MAIN BLOC
"""

url_base = "http://books.toscrape.com/"

page = requests.get(url_base)
soup = BeautifulSoup(page.content, "html.parser")

# Get links by category pages
categories_div = soup.find("div", class_="side_categories")
links_categories = categories_div.find_all("a")

list_links_categories = []
for link in links_categories[1:]:
    link = url_base + link["href"]
    list_links_categories.append(link)

# Parse categories links
for link_category in list_links_categories:
    link_response = requests.get(link_category)
    soup_category = BeautifulSoup(link_response.content, "html.parser")

    category_name = soup_category.h1.string
    list_links_products_pages = parse_links_products_pages(link_category)

    # Parse next page link
    next_page = soup_category.find("a", string="next")
    if next_page:
        link_next = link_category[0:-10] + next_page["href"]
        # Function parse URLs links of product pages
        new_links = parse_links_products_pages(link_next)
        for new_link in new_links:
            list_links_products_pages.append(new_link)

    # Create CSV file
    en_tete = ["product_page_url",
               "universal_product_code",
               "title",
               "price_including_tax",
               "price_excluding_tax",
               "number_available",
               "product_description",
               "category",
               "review_rating",
               "image_url_text",
               ]
    print(list_links_products_pages)
    with open("data_"+category_name+".csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)
        for link_product in list_links_products_pages:
            # Function parse product information in product page
            product_info = parse_product_page(link_product)
            writer.writerow(product_info[0])
            save_image(product_info[1], product_info[2])
