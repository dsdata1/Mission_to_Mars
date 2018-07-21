import requests as requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#test
def scrape():
    mars_mission = {}


    GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


    driver.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/")
    driver.execute_script('document.getElementById("full_image").click();')
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    a_ = soup.find('img', class_='fancybox-image')['src']
    x_ = 'https://www.jpl.nasa.gov'
    p_ = x_+a_
    mars_mission["featured_image"] = p_
    driver.close()



    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_mission["news"] = soup.find('div', class_="content_title").text.strip()
    mars_mission["news_description"] = soup.find('div', class_="image_and_description_container").text.strip()




    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    mars_mission['weather_tweet'] = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()




    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    all_images = soup.find_all('a', class_='product-item')

    links = ['https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg','https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg','https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg','https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg']
    hemisphere_images = []

    for i in all_images:
        hemisphere = {}
        hemisphere['title'] = i.h3.text
        hemisphere['img_url'] = links[all_images.index(i)]
        hemisphere_images.append(hemisphere)
        
    mars_mission['hemispheres'] = hemisphere_images




    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns = ['categories', 'values']
    df.set_index('categories', inplace=True)
    table = df.to_html()
    table = table.replace('\n', '')
    mars_mission['details'] = table




    return mars_mission

