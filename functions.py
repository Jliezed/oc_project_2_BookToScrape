import requests
from bs4 import BeautifulSoup
import re


# Parse URLs links of product pages
def parse_links_products_pages(url):
    page = requests.get(url)
    soup_product_page = BeautifulSoup(page.content, "html.parser")
    main_div = soup_product_page.find_all("h3")

    list_links_products_pages = []
    for item in main_div:
        link_product_page = "https://books.toscrape.com/catalogue/" + item.a["href"][9:]
        list_links_products_pages.append(link_product_page)
    return list_links_products_pages


# Parse product information in product page
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
    if product_description_div:
        product_description = product_description_div.find_next("p").string

    breadcrumb = soup_page.find('ul', class_='breadcrumb')
    list_breadcrumb = breadcrumb.find_all("a")
    category = list_breadcrumb[2].string

    review_rating = soup_page.find("p", class_="star-rating")["class"][1]

    image_url = soup_page.find("div", class_="carousel-inner").find_next("img")
    image_url_text = "https://books.toscrape.com" + image_url["src"][5:]

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

    return product_page_info, image_url_text, universal_product_code


# Download and save image
def save_image(url_image, upc):
    file_image = open(upc + ".jpg", "wb")
    image_response = requests.get(url_image)
    file_image.write(image_response.content)
    file_image.close()
