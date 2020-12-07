from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import csv
import codecs
import re
import datetime
import mysql.connector


def opendriver():
    driver = webdriver.Chrome("driver/chromedriver.exe")
    driver.get("https://www.alza.cz/wearables/18855068.htm#f&cst=0&cud=0&pg=1-50&prod=&sc=1022")
    sleep(5)
    writetofile(driver)
    driver.quit()


def writetofile(driver):
    res = driver.page_source

    soup = BeautifulSoup(res, "html.parser")

    pretty_soup = soup.prettify()

    html_file = open("html/alza_main.html", "wb")
    html_file.write(pretty_soup.encode('utf-8'))
    html_file.close()

    print("5 seconds timeout")
    sleep(5)


opendriver()
