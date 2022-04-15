import requests
from bs4 import BeautifulSoup
import time
import re

#Functions
def parse_links_products_pages():
    main_div = soup.find_all("h3")

    for item in main_div:
        link_product_page = url + item.a["href"]
        list_links_products_pages.append(link_product_page)

def parse_product_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #product_page_url
    product_page_url = url
    print(product_page_url)
    #universal_ product_code (upc)
    universal_product_code = soup.find(string="UPC").next_element.string
    print(universal_product_code)
    #title
    title = soup.h1.string
    print(title)
    #price_including_tax
    price_including_tax = soup.find(string="Price (incl. tax)").next_element.string
    print(price_including_tax)
    #price_excluding_tax
    price_excluding_tax = soup.find(string="Price (excl. tax)").next_element.string
    print(price_excluding_tax)
    #number_available
    number_available_text = soup.find("p", class_="instock availability").get_text().strip()
    number_available = re.search(" \((.*) available", number_available_text)
    number_available = number_available.group(1)
    print(number_available)
    #product_description
    product_description_div = soup.find(id="product_description")
    product_description = product_description_div.find_next("p").string
    print(product_description)
    #category
    breadcrumb = soup.find('ul', class_='breadcrumb')
    list_breadcrumb = breadcrumb.find_all("a")
    category = list_breadcrumb[2].string
    print(category)
    #review_rating
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    print(review_rating)
    #image_url
    image_url = soup.find("div", class_="carousel-inner").find_next("img")
    image_url_text = "http://books.toscrape.com" + image_url["src"][5:]
    print(image_url_text)



# Main variables
url = "http://books.toscrape.com/"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Get links by category pages
categories_div = soup.find("div", class_="side_categories")
links_categories = categories_div.find_all("a")

list_links_categories =[]
list_links_products_pages = []
for link in links_categories[1:5]:
    link = url + link["href"]
    list_links_categories.append(link)

    link_page = requests.get(link)
    soup_category = BeautifulSoup(link_page.content, "html.parser")
    next = soup_category.find("a", string="next")

    if next != None:
        link_next = link[0:-10] + next["href"]
        list_links_categories.append(link_next)

    parse_links_products_pages()

print(list_links_categories)
print(list_links_products_pages)

for link in list_links_products_pages:
    parse_product_page(link)



