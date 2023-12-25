from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = chrome_options)

mongo_client = MongoClient('mongodb://localhost:27017')
db = mongo_client['scraping']
collection = db['data']


def scrape():

    driver.get('https://timesofindia.indiatimes.com/')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_list = soup.find_all('div', class_='col_l_6')

    for new in news_list:
        all_news = new.find('figcaption')

        if all_news:
            news_name = all_news.text.strip()
        else:
            news_name = "News Cannot be found"

        all_news_link = new.find('a')
        if all_news_link:
            news_link = all_news_link.get('href')
        else:
            news_link = "News link not found"

        news_data = {
            "news" : news_name,
            "link" : news_link
        }
        db.data.insert_one(news_data)
        print(f"{news_name} stored in DB.")
    driver.quit()
    mongo_client.close()


if __name__ == "__main__":
    scrape()                         
