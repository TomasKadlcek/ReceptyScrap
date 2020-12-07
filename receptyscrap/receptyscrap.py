from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import codecs
import mysql.connector


# get first 1000 recipe URLs from site and save them to MySQL database

# Opens driver. Sets URL with pagination from 1 to 20 and sends result to write_to_file method. 7 seconds timeout for
# driver to load the page
def open_driver():
    driver = webdriver.Chrome("driver/chromedriver.exe")
    for num in range(1, 21):
        page = "https://www.recepty.cz/vyhledavani/pokrocile?showResults=1&page=" + str(num)
        driver.get(page)
        sleep(7)

        write_to_file(driver)
    driver.quit()


# gets result from driver, prettify and saves it into a HTML file. Proceed to scrap_file method
def write_to_file(driver):
    resource = driver.page_source

    soup = BeautifulSoup(resource, "html.parser")

    pretty_soup = soup.prettify()

    html_file = open("html/recepty.html", "wb")
    html_file.write(pretty_soup.encode('utf-8'))
    html_file.close()

    scrap_file()


# sends request to mysql to make a new connection and proceeds to scrape_and_send method
def scrap_file():
    scrapped_file = codecs.open("html/recepty.html", "r", "utf-8")
    soup = BeautifulSoup(scrapped_file, "lxml")

    cnx = connect_mysql()
    scrape_and_send(cnx, soup)


# connection to mysql via connector. returns cnx to scrap_file
def connect_mysql():
    cnx = mysql.connector.connect(user='root', password='password',
                                  host='localhost',
                                  database='py_scrap')
    return cnx


# finishes the process by scrapping all needed URLs and sending them to MySQL. Process goes over again in open_driver
# until condition of 20 pages met.
def scrape_and_send(cnx, soup):
    x = 0
    for wrapper in soup.find_all("div", class_="search-results__wrapper"):
        for recipe in wrapper.find_all("div", class_="recommended-recipes__article-meta"):
            a = recipe.find("a", href=True)
            cursor = cnx.cursor()

            add_url = ("INSERT INTO urls " "(url) " "VALUES (\"" + a["href"] + "\")")

            cursor.execute(add_url)

            cnx.commit()
            cursor.close()

    cnx.close()


# initializing methods
connect_mysql()
open_driver()
