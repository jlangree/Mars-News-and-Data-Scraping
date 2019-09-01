# # Mission to Mars
# 
# ### Web-Scraping for Mars Info


# Dependencies
import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup as bs


# --------------------------------------------------------------------------------------------------------------------

# Function that initializes browser
def init_browser():
    # Initialize browser using chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    
    return Browser("chrome", **executable_path, headless=False)


# Function that visits a website and scrapes the html into Beautiful Soup
def get_html(url, browser):    
    
    # visit website
    browser.visit(url)

    # scrape page into soup
    html = browser.html
    soup = bs(html, "lxml")
    
    return soup


# -------------------------------------------------------------------------------------------------------------------
# Function that scrapes latest mars data --> returns dict of results
# -------------------------------------------------------------------------------------------------------------------
def scrape():

    # Initialize browser using chromedriver
    browser = init_browser()


    # -------------------------------------------------------------------------------------------------------------------
    # #### NASA Mars News
    # 
    # * Get title and teaser paragraph for latest Mars news story


    # set url and scrape site into soup
    NASA_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+'        'desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    soup = get_html(NASA_url, browser)

    # get html for latest news story
    latest_story = soup.find('li', attrs={'class': 'slide'})

    # get title and paragraph from latest story (first story)
    news_title = latest_story.find('div', {'class': 'content_title'}).text

    news_p = latest_story.find('div', {'class': 'article_teaser_body'}).text
  


    # ------------------------------------------------------------------------------------------------------------------
    # #### JPL Mars Space Images
    # 
    # - Get url for featured Mars image

    # set url and scrape site into soup
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    soup = get_html(JPL_url, browser)


    # find url for image
    relative_url = soup.find('a', id='full_image')['data-fancybox-href']

    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = base_url + relative_url


    # ---------------------------------------------------------------------------------------------------------------
    # #### Mars Weather
    # 
    # - Get latest tweet from Mars Weather Twitter account


    # set url and scrape site into soup
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    soup = get_html(weather_url, browser)


    # save text of latest tweet
    mars_weather = soup.find('p', {'class': 'TweetTextSize'}).text.replace('\n', ', ')
    print(mars_weather)


    # ---------------------------------------------------------------------------------------------------------------
    # #### Mars Facts
    # 
    # - Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # - Use Pandas to convert the data to a HTML table string.

    # set url
    facts_url = 'https://space-facts.com/mars/'

    # read tables into pandas
    tables = pd.read_html(facts_url)

    # get relevant table
    df = tables[1]

    # convert df to html table string; remove index and col headings; set CSS id
    html_table = df.to_html(header=False, index=False, table_id='mars-table', classes=['table', 'table-striped'])


    # ------------------------------------------------------------------------------------------------------------------
    # #### Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


    # set url for USGS Astrogeology site and visit
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # names of hemispheres
    hemi_names = [
        'Cerberus Hemisphere',
        'Schiaparelli Hemisphere',
        'Valles Marineris Hemisphere',
        'Syrtis Major Hemisphere'
    ]

    # visit USGS website
    browser.visit(USGS_url)


    # set up empty list for img url dicts
    hemisphere_image_urls = []

    # loop through hemispheres, get img urls after clicking links
    for hemi in hemi_names:

        # click link for hemisphere
        browser.click_link_by_partial_text(hemi)

        # get html with bs4
        soup = bs(browser.html, "lxml")

        # find image url in first anchor of first list item on page
        img_url = soup.find('li').find('a')['href']

        # create dict for image and add to list
        hemi_dict = dict(title=hemi, img_url=img_url)
        hemisphere_image_urls.append(hemi_dict)
        
        # redirect back
        browser.back()
        
    hemisphere_image_urls

    # -------------------------------------------------------------
    # close browser
    browser.quit()

    # add info to dict to be returned
    mars_data_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'html_table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # return mars_data_dict
    return mars_data_dict
