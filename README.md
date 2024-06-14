# `snaggr`

## About `snaggr`

Hello! Thank you for installing the `snaggr` package. `snaggr` (Snag Google Reviews) is a Python package developed by Deon Posey and is designed for Python programmers and data scientists with some experience in Selenium, as it heavily relies on classes and methods from the Selenium package. However, `snaggr` abstracts most of the underlying code, simplifying the process of automating and scraping Google review pages for any given hotel.

Currently, this version of `snaggr` is specifically tailored to scrape Google review pages for hotels. While Google provides reviews for various types of businesses, each category has a different HTML layout and page structure. Expanding `snaggr` to handle other business types, such as restaurants, is planned for future versions. For now, this package enables you to easily gather data for natural language processing, sentiment analysis, or any other analysis you wish to perform with the acquired data, without the concern of being IP banned.

## Installation

pip install snaggr

## Usage

This version of `snaggr` includes two useful functions for scraping google reviews:

- `collect_hotel_google_reviews(google_review_url, options, service, max_scroll_time=360, dataset=None)`
- `collect_multiple_hotels_google_reviews(urls, options, service, max_scroll_time=360, dataset=None)`

### `collect_hotel_google_reviews`

This function takes the following parameters:

-  google_review_url`: The URL of the Google review page.
- `options`: An `Options` object imported from `selenium.webdriver.chrome.options`.
- `service`: The location of your web driver's binary executable.
- `max_scroll_time`: An optional argument (default value is 360 seconds) that determines how long `snaggr` should scroll down the webpage.
- `dataset`: An optional argument (default is `None`). If provided, it should be a CSV file or a path to a CSV file with the columns: 'reviews', 'ratings', 'grade', and 'sentiment'. If not provided, `snaggr` will create a new file called `snaggr_file.csv` and append the scraped data to it.

### `collect_multiple_hotels_google_reviews`

This function takes a list of hotel Google review URLs and runs `collect_hotel_google_reviews` simultaneously on each webpage using the threading module from the Python standard library.


## Example

```python
import snaggr
from snaggr import *

options = snaggr.Options()
options.binary_location = 'C:/PATH/TO/chromedriver-win64/chrome-win64/chrome.exe'
options.add_argument('--no-sandbox')  # Disable sandbox mode

service = snaggr.Service(r"C:\PATH\TO\chromedriver-win64\chromedriver.exe")

GILA_RIVER_RESORT_REVIEWS_URL = 'https://www.google.com/travel/search?q=casino%20hotel&ts=CAEaNwoXEhU6E01hcmljb3BhIENvdW50eSwgQVoSHBIUCgcI6A8QBhgMEgcI6A8QBhgNGAEyBAgAEAAqBwoFOgNVU0Q&ictx=3&qs=CAAgACgAMidDaGtJMjRIXzRaeWRnb2pwQVJvTUwyY3ZNV2hqTm5Sb01ITmtFQUU4DUgA&ap=KigKEglp-Lc_bbQ1QBG8MyQ4gwNdwBISCXQhEinzFUZAEbwzJDj7UFvAMAC6AQdyZXZpZXdz'

collect_hotel_google_reviews(GILA_RIVER_RESORT_REVIEWS_URL, options, service)
```
The code above will:

- Open your specified Chrome driver web browser.
- Navigate to the webpage associated with the URL value stored in `GILA_RIVER_RESORT_REVIEWS_URL`.
- Scroll down that page for the default value of 360 seconds.
- Snag all the reviews and their associated ratings.
- Export the data into a CSV file with appropriate sentiment labels and 'grades' which the sentiment label was last derived from.

-This version removes the reviews that were translated by Google, as they can be mistranslated and have a negative impact on NLP models. In future versions, this will be optional.

