from splinter import Browser
from bs4 import BeautifulSoup
import time
import re
import pandas as pd


executable_path = {'executable_path':r'C:\Users\nguye\Downloads\chromedriver_win32\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape_info():

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)
    news_title = soup.select_one('ul.item_list li.slide div.content_title').text

    time.sleep(5)
    news_p = soup.select_one('ul.item_list li.slide div.article_teaser_body').text   
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23446_hires.jpg"

    url ="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(1)
    tweets=soup.find_all("span",text=re.compile('InSight sol'))
    time.sleep(1)
    latestweather=tweets[0].get_text()

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
        ]
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_table = pd.read_html(url)[0]
    mars_table.columns=['Descriptions', 'Mars']
    mars_table.set_index('Descriptions', inplace=True)
    mars_table_html = mars_table.to_html()


    # Store data in a dictionary
    mars_data = {
        "News_Title": news_title,
        "News_Text": news_p,
        "Featured_Image": featured_image_url,
        "Latest_Weather": latestweather,
        "Hemisphere_Images": hemisphere_image_urls,
        "Mars_Fact": mars_table_html
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
