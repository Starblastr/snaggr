import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import threading
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from fractions import Fraction

class Snaggr:
    def __init__(self):
        self.ratings = None
        self.reviews= None
        self.positive_priceline_reviews = None
 
    def hold_key_down(self, driver, key, hold_time):
        """Holds a given key down for a specified amount of time."""
        end_time = time.time() + hold_time
        actions = webdriver.ActionChains(driver)
        while time.time() < end_time:
            actions.key_down(key).perform()
            time.sleep(0.1)  # Sleep for a short duration
            actions.key_up(key).perform()
            time.sleep(0.1)  # Sleep for a short duration to simulate the key press

    def scroll_using_keys(self, driver, total_duration):
        """Scrolls down the page using Page Down and Page Up keys."""
        initial_hold_time = 5  # Hold Page Down for 5 seconds initially
        alternate_duration = total_duration - initial_hold_time  # Remaining time to alternate between keys
        

        # Hold Page Down key for 5 seconds
        self.hold_key_down(driver, Keys.PAGE_DOWN, initial_hold_time)

        end_time = time.time() + alternate_duration
        while time.time() < end_time:
            last_height = driver.execute_script("return document.body.scrollHeight")
            # Press Page Up key for 1 second
            self.hold_key_down(driver, Keys.PAGE_UP, 1)

            # Hold Page Down key for 10 seconds
            self.hold_key_down(driver, Keys.PAGE_DOWN, 10)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                print('Succesffully scrolled down to the end of page.')
                break
                
                
    def inject_placeholders(self, driver):
        script = """
        var divs = document.querySelectorAll('div.K7oBsc');
        divs.forEach(function(div) {
            // Check if div is empty and inject 'No comment.'
            if (div.innerHTML.trim() === '') {
                var newDiv = document.createElement('div');
                var newSpan = document.createElement('span');
                newSpan.textContent = 'No comment.';
                newDiv.appendChild(newSpan);
                div.appendChild(newDiv);
            }

            // Check for positive and negative spans
            var positiveSpan = div.querySelector('span.tml7sf');
            var negativeSpan = div.querySelector('span.yOgiqb');

            // Handle positive span
            if (positiveSpan && positiveSpan.innerHTML.trim() === '+') {
                var nextSpan = positiveSpan.nextElementSibling;
                if (!nextSpan || nextSpan.tagName.toLowerCase() !== 'span' || nextSpan.innerHTML.trim() === '') {
                    if (!nextSpan) {
                        nextSpan = document.createElement('span');
                        positiveSpan.parentNode.appendChild(nextSpan);
                    }
                    nextSpan.innerHTML = 'No Positive';
                }
            }

            // Handle negative span
            if (negativeSpan && negativeSpan.innerHTML.trim() === '-') {
                var nextSpan = negativeSpan.nextElementSibling;
                if (!nextSpan || nextSpan.tagName.toLowerCase() !== 'span' || nextSpan.innerHTML.trim() === '') {
                    if (!nextSpan) {
                        nextSpan = document.createElement('span');
                        negativeSpan.parentNode.appendChild(nextSpan);
                    }
                    nextSpan.innerHTML = 'No Negative';
                }
            }

            // Ensure each div has a consistent structure
            if (positiveSpan && !negativeSpan) {
                var newDiv = document.createElement('div');
                var newNegativeSpan = document.createElement('span');
                newNegativeSpan.className = 'yOgiqb';
                newNegativeSpan.textContent = '-';
                var newNegativeTextSpan = document.createElement('span');
                newNegativeTextSpan.textContent = 'No Negative';
                newDiv.appendChild(newNegativeSpan);
                newDiv.appendChild(newNegativeTextSpan);
                div.appendChild(newDiv);
            }

            if (negativeSpan && !positiveSpan) {
                var newDiv = document.createElement('div');
                var newPositiveSpan = document.createElement('span');
                newPositiveSpan.className = 'tml7sf';
                newPositiveSpan.textContent = '+';
                var newPositiveTextSpan = document.createElement('span');
                newPositiveTextSpan.textContent = 'No Positive';
                newDiv.appendChild(newPositiveSpan);
                newDiv.appendChild(newPositiveTextSpan);
                div.appendChild(newDiv);
            }
        });
        """
        driver.execute_script(script)
        
    def wait_for_empty_divs(self, driver):
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.K7oBsc > div > span:contains('No comment.')"))
            )
            print('Found elements with placeholder text')
        except:
            print("Webpage preprcessing complete. Proceeding to scrape review text data...")


    def get_review_text(self, driver):
        try:

                    
            # Wait for the updated span elements to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.K7oBsc > div > span"))
            )

            # Find all span elements inside the div with the matching class
            potential_elements = driver.find_elements(By.CSS_SELECTOR, "div.K7oBsc > div > span")
            span_elements = []
            for element in potential_elements:
#                 print(f"Checking element: {element.get_attribute('outerHTML')}")
                # Check if the parent div has empty inner HTML
                parent_div = element.find_element(By.XPATH, "./ancestor::div[@class='K7oBsc']")
#                 print(f"Parent div innerHTML: {parent_div.get_attribute('innerHTML')}")

                if not parent_div.get_attribute("innerHTML").strip():
                    print("Empty inner HTML found. Terminating the search.")
                    break
                    
                span_elements.append(element)
        # If the parent div is not empty, add the element to span_elements
            
    

            # Collect text from all span elements and filter out those containing "Read more"
            review_text_list = []
            for element in span_elements:
                inner_text = element.get_attribute("innerHTML")
                span_class = element.get_attribute('class')
#                 print(f"Processing element with inner HTML: {inner_text}")
#                 if inner_text:
#                     print(f"Processing element with inner HTML: {inner_text}")
#                 else:
#                     print("Skipping element with no inner HTML")
                
                
#                 if "Read more" not in inner_text and inner_text != "+" and inner_text != "-" and span_class != 'tml7sf' and span_class != 'yOgiqb':
                if "Read more" not in inner_text:    
                    # Replace <br> tags with newlines
                    inner_text = re.sub(r'<br\s*/?>', ' ', inner_text)
                    review_text_list.append(inner_text)

            # return list of scraped reviews
            return review_text_list

        except Exception as e:
            print(f"An error occurred: {e}")
    def get_ratings(self, driver):
        ratings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class= 'GDWaad']"))
)
        return ratings
    def clean_priceline_reviews(self, reviews):
        i = 0
        positive_priceline_reviews = []
        while i < len(reviews):
            if reviews[i] == '+':
                # Remove the '+' and the positive review from priceline
                reviews.pop(i)
                if i < len(reviews):
                    positive_priceline_reviews.append(reviews[i])
                    reviews.pop(i)

            elif reviews[i] == '-':
                # Remove the '-' strings -keep the negative review from priceline
                reviews.pop(i)
                i+=1

            else:
                i += 1
        self.positive_priceline_reviews = positive_priceline_reviews
        return reviews, self.positive_priceline_reviews
    
    # Function to remove the priceline ratings from the list entirely, if needed.
    def remove_priceline_ratings(self, ratings):
        for rating in ratings:
            numerator, denomenator = rating.split('/')
            if denomenator == '10':
                ratings.remove(rating)
        return ratings
    
    def clean_trip_advisor_reviews(self, reviews):
        cleaned_reviews = []
        for review in reviews:
            # Tripdvisor reviews are truncated and contain a signature string '&nbsp' that is useless for our model
            review = review.replace('&nbsp', '')
            review = review.replace('&amp;', 'and')
            review = re.sub(r"\\'", "'", review)
            cleaned_reviews.append(review)
        return cleaned_reviews

    
def collect_multiple_hotels_google_reviews(urls, options, service, dataset=None):
    threads = []
    for google_review_url in urls:
        thread = threading.Thread(target=collect_hotel_google_reviews, args=(google_review_url, options, service, dataset))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

counter = 0
counter_lock = threading.Lock()

def increment_counter():
    global counter
    with counter_lock:
        local_counter = counter
        local_counter += 1
        time.sleep(0.1)
        counter = local_counter
    
def collect_hotel_google_reviews(google_review_url, options, service, scroll_time = 180, dataset = None,):
    # control the flow of reading and writing to the file by the threads using the increment_counter function
    increment_counter()
    driver = webdriver.Chrome(options=options, service=service)
    
    driver.get(google_review_url)
    page_engine = Snaggr()
    
    # Scroll down to the end of the page
    print(f'URL successfully located, scrolling down webpage for a maximum of {scroll_time} seconds...') 
    page_engine.scroll_using_keys(driver, scroll_time)
    
    # Inject placeholders to empty divs so they are not skipped
    print('Scrolling phase complete. Injecting placeholder text into empty review fields...')
    page_engine.inject_placeholders(driver)
    print('Placeholders successfully injected...')
    time.sleep(1)
    
    # Wait for all empty divs to have placeholder text
    page_engine.wait_for_empty_divs(driver)
    time.sleep(1)

    # Scrape reviews and ratings data from the google reviews webpage using my function that takes a selenium driver input
    print('Aquiring reviews text data...')
    raw_reviews = page_engine.get_review_text(driver)
    print('Review data successfully acquired...')
    
    print('Acquiring ratings data...')     
    raw_ratings = page_engine.get_ratings(driver)
    print('Ratings data succesfully obtained.\n Proceeding to build dataframe...')
                      # <----Build Dataframe from raw data lists ---->
    # Pull the text from each raw selenium object
    ratings_lst = []
    for s in raw_ratings:
        ratings_lst.append(s.text)
    
    ratings = ratings_lst
    
    google_and_raw_tripadvisor_reviews, positive_priceline_reviews = page_engine.clean_priceline_reviews(raw_reviews.copy())
    
    reviews = page_engine.clean_trip_advisor_reviews(google_and_raw_tripadvisor_reviews.copy())

    
    df = pd.DataFrame({'reviews':reviews,
                 'ratings':ratings[:len(reviews)]})
    
    df = combine_priceline_reviews(df, positive_priceline_reviews)
    print('Dataframe successfully built.')
    
                           # <----Process Dataframe---->
    # Create a grade column from the ratings column. the ratings are in the form of fracions so we convert them to floats using the function 'convert_to_float' which handles string inputs that are structured as fractional values    
    df['grade'] = df['ratings'].apply(convert_to_float)
    # Create a categorical sentiment column based on the grade column using the determine_sentiment function defined in this module
    df['sentiment'] = df['grade'].apply(determine_sentiment)
    
    # Remove unwanted text from the reviews which were translated by google
    df = clean_translated_reviews(df)
    
    # Filter out the reviews which had no text and that we injected 'No comment.' in as a placeholder, they have no value for the model
    df = df[df['reviews'] != 'No comment.']
    
    # initialize dataframe to combine df with, this will be needed if there is no input dataset i.e. dataset==None
    snaggr_df = pd.DataFrame(columns=df.columns)
    
    
    if not dataset:
        try:
            previous_data = pd.read_csv('snaggr_file.csv', index_col=0)
            print('snaggr_file.csv detected. Inserting data...')
            snaggr_df = pd.concat([previous_data,df])
            snaggr_df.to_csv('snaggr_file.csv')
            print('snaggr_file.csv updated.')
        except Exception as e:
            print('snaggr_file.csv not detected, creating new snaggr_file.csv file...')
            snaggr_df = pd.concat([snaggr_df,df])
            snaggr_df.to_csv('snaggr_file.csv')
            print('snaggr_file.csv successfully created.')


            
            
    elif dataset:
        # dataset needs to be a file path to a csv file with the proper structure
        reviews = pd.read_csv(dataset, index_col=0)
        df = pd.concat([reviews,df])
        df.to_csv(dataset)
    
    return df



# Convert string fractions to floats
def convert_to_float(x):
    try:
        return float(Fraction(x))
    # Handle cases where x is not a valid fraction
    except ValueError:
        parts = x.split('/')
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            numerator, denominator = map(float, parts)
            return numerator / denominator
        else:
            return float('nan')




# Function to determine sentiment based on rating
def determine_sentiment(rating):
    if rating <= 0.5:
        return 'Bad'
    elif rating == 0.6:
        return 'Neutral'
    else:
        return 'Good'

def combine_priceline_reviews(df, positive_priceline_reviews):
    n=0
    for rating in df['ratings']:
        # Pricline reviews are fractions that are tenths instead of fifths, this is exploited to re-append the positive notes that were stripped back onto the priceline reviews
        if '10' in rating.split('/') and n <=len(positive_priceline_reviews):
            df.iloc[n]['reviews'] = df.iloc[n]['reviews'] + ' ' + positive_priceline_reviews[n]
        n+=1
    
    return df

def clean_translated_reviews(df):
    df['reviews'] = df['reviews'].str.replace(r'\s*\(Translated by Google\)', '', regex=True)
    df['reviews'] = df['reviews'].str.replace(r'\s*\(Original\)', '', regex=True)
    return df