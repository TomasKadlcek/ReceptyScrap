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
    driver.quit()
    return driver




opendriver()
