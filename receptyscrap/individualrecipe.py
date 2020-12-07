from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import codecs
import mysql.connector


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

    x = 0
    for url in cursor:
        print(url)
        x = x + 1
        print(x)


get_all_urls()