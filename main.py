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

    # Get next page link
    list_next_pages = []
    first_next_page = soup_category.find("a", string="next")
    if first_next_page:
        first_next_page_link = link_category[0:-10] + first_next_page["href"]
        list_next_pages.append(first_next_page_link)

    # For each next page link
    for next_page in list_next_pages:
        # Function parse URLs links of product pages
        new_links = parse_links_products_pages(next_page)
        for new_link in new_links:
            list_links_products_pages.append(new_link)

        # Check in this next page if there is another next page, if yes, add it to list_next_pages
        following_next_page = requests.get(next_page)
        soup_following_next_page = BeautifulSoup(
            following_next_page.content, "html.parser"
        )

        following_page = soup_following_next_page.find("a", string="next")
        if following_page:
            following_page_link = link_category[0:-10] + following_page["href"]
            list_next_pages.append(following_page_link)

    # Create CSV file
    en_tete = [
        "product_page_url",
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

    with open("data_" + category_name + ".csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)
        for link_product in list_links_products_pages:
            # Function parse product information in product page
            product_info = parse_product_page(link_product)
            writer.writerow(product_info[0])
            # Function save image of each product page
            save_image(product_info[1], product_info[2])
