from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def get_mars_facts():
 
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    facts = tables[0]

    facts_df = pd.DataFrame(facts) 

    return facts_df.to_html(index=False, header=False)


def get_mars_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Find article with class
    match = soup.find_all('article', attrs={'role': 'article'})[0]
    print(match)
    spans = match.find_all('span')
    weather = None
    for span in spans:
        # should begin with InSight
        text = span.get_text()
        if text[0:7] == "InSight":
            weather = text
            break

    return weather

def get_nasa_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')

    attempts = 0
    haveData = False
    while attempts < 5 and not haveData:
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        image = soup.find_all("img", class_="fancybox-image")[0]
        if image:
            haveData = True

    return f"{url}/{image['src']}"

def get_nasa_news(browser):
    listings = []

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    attempts = 0
    haveData = False
    while attempts < 5 and not haveData:
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        slides = soup.find_all("li", class_="slide")
        if slides:
            haveData = True

    if not haveData:
        raise Exception("Failed to scrape nasa news site")

    for slide in slides:
        news_title = slide.find("div", class_="content_title").get_text()
        news_p = slide.find("div", class_="article_teaser_body").get_text()

        listings.append({"title": news_title
                    , "paragraph": news_p})
 
        return listings


def scrape():
    browser = init_browser()
    listings = get_nasa_news(browser)
    nasa_imag = get_nasa_image(browser)
    weather = get_mars_weather(browser)

    browser.quit()
    return listings, nasa_imag, weather
    #return listings, nasa_imag, weather



browser = init_browser()
facts = get_mars_facts()
print(facts)
browser.quit()

