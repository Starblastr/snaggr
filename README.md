
### ABOUT snaggr:
Hello! Thank you for installing the snaggr package. snaggr (Snag Google Reviews), is a package developed by Deon Posey. It is intended to be used by Python programmers and/or data scientist who have a little experience with selinium, as it relies heavy on classes and methods from the selinium package. However this package abstracts most of that code away from the user of this package, at least when it comes to automating and scraping google review pages for any given hotel. Yes, at the moment this version of snaggr is only capable of scraping google review pages for hotels. Google provides reviews on many different types busiesses that can be useful for data scientist. However, Google has completely different HTML layouts and page structure for different business categories, so there is more work to be done in order for snaggr to be able to get, for example restaurant reviews, although I do plan on adding such features to snaggr in the future. But for now this package will help you easily gather data to do natural language processing, sentiment analysis or whatever it is you want to do with the data you acquire with snaggr. All while not having to worry about being IP banned!

### Installation:
pip install snaggr



### Usage:
There are two main functions included in snaggr:
1. collect_hotel_google_reviews(google_review_url, options, service, dataset = None)
2. collect_multiple_hotels_google_reviews(urls, options, service, dataset=None)

collect_hotel_google_reviews is a function that takes a single url, options which is an Options() object, service which is your web driver binary location, and an optional dataset keyword argument which is set to None by default; dataset must be a csv file or path to a csv file which has the columns: 'reviews', 'ratings', 'grade', and 'sentiment'. If no dataset is provided, then snaggr will scrape the reviews from the URL, create a new file called 'snaggr_file.csv', and append the data into the snaggr_file.csv file; snaggr will look for this file each time you use collect_hotel_google_reviews function and if found, will append the scraped data to the snaggr_file.csv, effectively saving your data each time you use the function to scrape a hotel's google review webpage.

collect_multiple_hotels_google_reviews is a function that takes a list of hotel google review url's and runs collect_hotel_google_reviews simutaneously on every webpage provided via threading.
