from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import codecs
import mysql.connector
import re


def connect_mysql():
    cnx = mysql.connector.connect(user='root', password='password',
                                  host='localhost',
                                  database='py_scrap')
    return cnx


def get_all_urls():
    cnx = connect_mysql()
    cursor = cnx.cursor()
    query = ("SELECT url FROM urls")
    cursor.execute(query)

    send_url_to_driver(cursor, cnx)
    cnx.close()


def send_url_to_driver(cursor, cnx):
    driver = webdriver.Chrome("driver/chromedriver.exe")
    for url in cursor:
        refined_url = "https://recepty.cz" + url[0]
        driver.get(refined_url)
        sleep(4)

        write_to_file(driver, cnx, refined_url)

    cursor.close()
    driver.quit()


def write_to_file(driver, cnx, refined_url):
    resource = driver.page_source

    soup = BeautifulSoup(resource, "html.parser")

    pretty_soup = soup.prettify()

    html_file = open("html/individualrecipe.html", "wb")
    html_file.write(pretty_soup.encode('utf-8'))
    html_file.close()

    scrap_file(cnx, refined_url)


def scrap_file(cnx, refined_url):
    scrapped_file = codecs.open("html/individualrecipe.html", "r", "utf-8")
    soup = BeautifulSoup(scrapped_file, "lxml")

    scrape_data(cnx, soup, refined_url)


def scrape_data(cnx, soup, refined_url):
    img_regex = re.compile("v-carousel--item.*")
    description_regex = re.compile("paragraph.*")

    rating = soup.find("div", class_="recipe-rating-box__rating--total").text
    refined_rating = " ".join(rating.split())

    name = soup.find("h1", class_="recipe-title-box__title").text
    refined_name = " ".join(name.split())

    img = soup.find("div", class_=img_regex).a.img["src"]

    ingredience_str = ""
    description_str = ""

    for ingredient in soup.find_all("div", class_="ingredient-assignment__desc"):
        ingredient_text = ingredient.text
        refined_ingredience = " ".join(ingredient_text.split())
        ingredience_str = ingredience_str + refined_ingredience + "\\n "

    for description in soup.find_all("div", id=description_regex):
        description_text = description.text
        refined_description = " ".join(description_text.split())
        description_str = description_str + refined_description + " "

    print(refined_url)
    print(refined_rating)
    print(refined_name)
    print(img)
    print(ingredience_str)
    print(description_str)

    send_to_db(cnx, refined_name, refined_rating, ingredience_str, description_str, img, refined_url)


def send_to_db(cnx, refined_name, refined_rating, ingredience_str, description_str, img, refined_url):
    cnx2 = mysql.connector.connect(user='root', password='password',
                                   host='localhost',
                                   database='py_scrap')
    cursor = cnx2.cursor(buffered=True)

    add_recipe = ("INSERT INTO recipes "
                  "(recipe_name, rating, pict_url, ingredients, recipe_desc, url) "
                  "VALUES (%(recipe_name)s, %(rating)s, %(pict_url)s, %(ingredients)s, %(recipe_desc)s, %(url)s)")

    data_recipe = {
        'recipe_name': refined_name,
        'rating': refined_rating,
        'pict_url': img,
        'ingredients': ingredience_str,
        'recipe_desc': description_str,
        'url': refined_url,
    }

    cursor.execute(add_recipe, data_recipe)

    cnx2.commit()
    cursor.close()
    cnx2.close()


get_all_urls()
