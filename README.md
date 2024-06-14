### ABOUT snaggr:
Hello! Thank you for installing the snaggr package. snaggr (Snag Google Reviews), is a package developed by Deon Posey. It is intended to be used by Python programmers and/or data scientist who have a little experience with selinium, as it relies heavy on classes and methods from the selinium package. However this package abstracts most of that code away from the user of this package, at least when it comes to automating and scraping google review pages for any given hotel. Yes, at the moment this version of snaggr is only capable of scraping google review pages for hotels. Google provides reviews on many different types busiesses that can be useful for data scientist. However, Google has completely different HTML layouts and page structure for different business categories, so there is more work to be done in order for snaggr to be able to get, for example restaurant reviews, although I do plan on adding such features to snaggr in the future. But for now this package will help you easily gather data to do natural language processing, sentiment analysis or whatever it is you want to do with the data you acquire with snaggr. All while not having to worry about being IP banned!

### Installation:
pip install snaggr



### Usage:
This version of snaggr includes two useful functions for scraping google reviews:
1. collect_hotel_google_reviews(google_review_url, options, service, max_scroll_time=360, dataset = None,)
2. collect_multiple_hotels_google_reviews(urls5, options, service, max_scroll_time=360, dataset= None)

collect_hotel_google_reviews: This is a function that takes a single url, options which is an Options() object imported by snaggr from selenium.webdriver.chrome.options, service which is your web driver's binary executable location, max_scroll_time which is an optional keyword argument with a default value of 360 (6 minutes) that allows you to control how long snaggr should scroll down the webpage; the more reviews on a page, the longer it will take to scroll down the entirity of the page, and an optional dataset keyword argument which is set to None by default; dataset must be a csv file or path to a csv file which has the columns: 'reviews', 'ratings', 'grade', and 'sentiment'. If no dataset is provided, then snaggr will scrape the reviews from the URL, create a new file called 'snaggr_file.csv', and append the data into the snaggr_file.csv file; snaggr will look for this file each time you use collect_hotel_google_reviews function and if found, will append the scraped data to the snaggr_file.csv, effectively saving your data each time you use the function to scrape a hotel's google review webpage. 

collect_multiple_hotels_google_reviews: This is a function that takes a list of hotel google review url's and runs collect_hotel_google_reviews simutaneously on every webpage provided. This is accomplished using the threading module from the Python standard library.




### Example:
import snaggr
from snaggr import *

options = snaggr.Options()
options.binary_location= 'C:/PATH/TO/chromedriver-win64/chrome-win64/chrome.exe'
options.add_argument('--no-sandbox')  # Disable sandbox mode

service = snaggr.Service(r"C:\PATH\TO\chromedriver-win64\chromedriver.exe")


GILA_RIVER_RESORT_REVIEWS_URL = 'https://www.google.com/travel/search?q=casino%20hotel&ts=CAEaNwoXEhU6E01hcmljb3BhIENvdW50eSwgQVoSHBIUCgcI6A8QBhgMEgcI6A8QBhgNGAEyBAgAEAAqBwoFOgNVU0Q&ictx=3&qs=CAAgACgAMidDaGtJMjRIXzRaeWRnb2pwQVJvTUwyY3ZNV2hqTm5Sb01ITmtFQUU4DUgA&ap=KigKEglp-Lc_bbQ1QBG8MyQ4gwNdwBISCXQhEinzFUZAEbwzJDj7UFvAMAC6AQdyZXZpZXdz'

collect_hotel_google_reviews(GILA_RIVER_RESORT_REVIEWS_URL, options, service)
 
 ##### The code above will open up your specified chrome driver web browser and get the webpage associated with the url value stored in 'GILA_RIVER_RESORT_REVIEWS_URL' scroll down that page for the default value of 360 seconds and then effectively snag all the reviews and their associated ratings and export them into a csv file with appropriate sentiment labels and 'grades' which the sentiment label was last derived from. This version removes the reviews that were translated by Google, as they can be mistranslated and have a negative impact on NLP models. In future versions, this will be optional. 