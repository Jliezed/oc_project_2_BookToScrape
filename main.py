import requests
from bs4 import BeautifulSoup
import re
import csv

# Functions
def parse_links_products_pages(url):
    page = requests.get(url)
    soup_product_page = BeautifulSoup(page.content, "html.parser")
    main_div = soup_product_page.find_all("h3")

    for item in main_div:
        link_product_page = url_base + "catalogue/" + item.a["href"][9:]
        list_links_products_pages.append(link_product_page)


def parse_product_page(url_product):
    page_response = requests.get(url_product)
    soup_page = BeautifulSoup(page_response.content, 'html.parser')

    product_page_url = url_product

    universal_product_code = soup_page.find(string="UPC").next_element.string

    title = soup_page.h1.string

    price_including_tax = soup_page.find(string="Price (incl. tax)").next_element.string

    price_excluding_tax = soup_page.find(string="Price (excl. tax)").next_element.string

    number_available_text = soup_page.find("p", class_="instock availability").get_text().strip()
    number_available = re.search(" \((.*) available", number_available_text)
    number_available = number_available.group(1)

    product_description_div = soup_page.find(id="product_description")
    product_description = ""
    if product_description_div != None:
        product_description = product_description_div.find_next("p").string

    breadcrumb = soup_page.find('ul', class_='breadcrumb')
    list_breadcrumb = breadcrumb.find_all("a")
    category = list_breadcrumb[2].string

    review_rating = soup_page.find("p", class_="star-rating")["class"][1]

    image_url = soup_page.find("div", class_="carousel-inner").find_next("img")
    image_url_text = "http://books.toscrape.com" + image_url["src"][5:]

    product_page_info = [
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url_text
    ]

    return product_page_info


# Get links by category pages
url_base = "http://books.toscrape.com/"

page = requests.get(url_base)
soup = BeautifulSoup(page.content, "html.parser")


categories_div = soup.find("div", class_="side_categories")
links_categories = categories_div.find_all("a")

list_links_categories = []
for link in links_categories[1:]:
    link = url_base + link["href"]
    list_links_categories.append(link)


for link_category in list_links_categories:
    link_response = requests.get(link_category)
    soup_category = BeautifulSoup(link_response.content, "html.parser")

    category_name = soup_category.h1.string
    print(category_name)
    list_links_products_pages = []
    parse_links_products_pages(link_category)

    next = soup_category.find("a", string="next")
    if next != None:
        link_next = link_category[0:-10] + next["href"]
        parse_links_products_pages(link_next)

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

    with open("data_"+category_name+".csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)
        for link_product in list_links_products_pages:
            product_info = parse_product_page(link_product)
            writer.writerow(product_info)
