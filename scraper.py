from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import undetected_chromedriver.v2 as uc
#import random


class WebDriver():
    '''
    This class is used to control the webdriver and scraper

    Attributes:
        url (str): The URL of the home webpage to navigate to
        driver (selenium.webdriver): The webdriver object
    '''

    def __init__(self, url) -> None:
        '''
        See help(WebDriver) for accurate signature
        '''
        self.url = url

    def open_the_webpage(self) -> None:
        '''
        This function is used to open the webpage to the URL defined in the instance attribute and close any pop-ups

        Returns:
            None
        '''
        # TODO: use a with block to open connection and close when finished
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument('proxy-server=106.122.8.54:3128')
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) 
        #options = uc.ChromeOptions()
        #options.headless=False
        #self.driver = uc.Chrome(version_main=96)
        #self.driver = uc.Chrome(options=options) 
        
        #chrome = uc.Chrome(options=options) 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        # sleep(1)
        self.accept_all_cookies()
        
    
    def accept_all_cookies(self) -> None:
        '''
        This function is used to close the accept cookies pop-up

        Returns:
            None
        '''
        # sleep(2*random.random()) # Ensure the webpage has fully loaded first
        sleep(1)
        accept_cookies_button = self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        print(type(accept_cookies_button))
        accept_cookies_button.click()
        sleep(10)
    
    # Navigate straight to Men's or Women's clothes page

    def navigate_to_gender(self):
        '''
        This function navigates to the gender page and returns the WebElement
        '''
        # TODO: Navigate via xpath to the menu bar container
        pass
    
    def navigate_to_the_item_type_page(self, gender, item_type) -> None:
        '''
        This function is used to navigate to the menu bar container and open the item_type as specified in the input
        The driver will move to the new webpage

        Args:
            gender (str): 'mens' or 'womens'
            item_type (str): valid item_type that belongs to the mens or womens container
        
        Returns:
            None
        '''
        # TODO
        pass
    
    def open_item(self):
        '''
        This function will open the item from the item type page
        The driver will move to the new webpage

        Returns:
            None
        '''
        # TODO
        pass

    def next_item(self):
        '''
        This function will move to the next item from the item type page
        The driver will move to the new webpage

        Returns:
            None
        '''
        # TODO
        pass

    def next_page(self):
        '''
        This function will move to the next set of items from the current item type page
        The driver will move to the new webpage

        Returns:
            None
        '''
        # TODO
        pass
    
    def scrape_feature_from_page(self, feature):
        '''
        This function will scrape the input feature from the item page
        
        Args:
            feature (str): valid feature item, from a list of features to be scraped

        Returns:
            TBD
        '''
        # TODO
        pass
    
    def download_image(self) -> None:
        # TODO
        pass   


class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features
    '''
    def __init__(self) -> None:
        pass

    def upload_image_to_datalake(self):
        pass

# 500 items of Mens & 500 of Womens
number_of_items = {'Mens': {'Hoodies & Sweatshirts' : 50, 'Coats & Jackets': 50, 'Jeans' : 50,'Jewellry & Watches' : 50, 
                            'Shoes' : 50, 'T-Shirts' : 50, 'Accessories' : 50, 'Trousers' : 50, 'Shirts' : 50, 'Loungewear' : 50},  
                    'Womens': {'Hoodies & Sweatshirts' : 50, 'Coats & Jackets' : 50, 'Jeans' : 50, 'Jewellry & Watches' : 50,
                            'Shoes' : 50, 'Tops' : 50, 'Accessories' : 50, 'Bottoms' : 50, 'Dresses & Jumpsuits' : 50,'Loungewear' : 50}}

# List of womens items categories to navigate to, input to a function
#womens_items = ['Tops', 'Hoodies & Sweatshirts', 'Dresses & Jumpsuits', 'Coats & Jackets', 'Knitwear'
#                'Bottoms', 'Jeans', 'Lingerie', 'Loungewear', 'Jewellry & Watches', 'Accessories', 'Shoes']

# List of mens items categories to navigate to, input to a function
# mens_items = ['Hoodies & Sweatshirts', 'T-Shirts', 'Shirts', 'Jumpers & Knitwear', 'Coats & Jackets', 'Trousers'
#                 'Jeans', 'Joggers and Track Pants', 'Shorts and Swim', 'Jewellry & Watches',' Hats & Caps', 
#                 'Socks', 'Loungewear & Underwear', 'Accessories', 'Shoes']

# List of features to scrape from each item, input to a function
feature = ['Price', 'Sizes', 'Colour', 'Brand', 'Discounted', 'Review Score', 'Number of Reviews']

# TODO: Create a pandas data frame, with each feature, and URL, and unique ID


def run_scraper():
    URL = "https://www.urbanoutfitters.com/en-gb/"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    
    # TODO: Be able to navigate to Womens Tops by uncommenting below
    gender = 'womens'
    item_type = 'Tops'
    # driver.navigate_to_item_type_page(gender, item_type)


if __name__ == '__main__':
    run_scraper()
