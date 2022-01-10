from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re as regex

from time import sleep

product_list = []
href_list =[]

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
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window()


        self.accept_all_cookies()
        
    
    def accept_all_cookies(self) -> None:
        '''
        This function is used to close the accept cookies pop-up

        Returns:
            None
        '''
        sleep(1) # Ensure the webpage has fully loaded first
        accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        print(type(accept_cookies_button))
        accept_cookies_button.click()

    def navigate_to_menu_bar(self):
        '''
        This function navigates to the menu bar container and returns the WebElement
        '''
        # TODO: Navigate via xpath to the menu bar container
        pass
    
    def navigate_to_the_item_type_page(self, gender, item_type) -> None:
        '''
        This function is used to navigate to the menu bar container and open the item_type as specified in the input
        The driver will move to the new webpage

        Args:
            gender (str): 'mens' or 'womenscategorise it into '
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




    def load_more(self):
        for i in range(10):
            load_page_xpath = '//*[@id="page-content"]/div/div[2]/div[2]'
            load_page = self.driver.find_element(By.XPATH, load_page_xpath)
            button = load_page.find_element(By.TAG_NAME, 'button')
            button.click()
            sleep(2)
    
    def scrape_href(self):
        href_list = []
        product_container_xpath = '//*[@id="page-content"]/div/div[2]/ul'
        product_container = self.driver.find_element(By.XPATH, product_container_xpath)
        products = product_container.find_elements(By.TAG_NAME, 'li')
        for product in products:
            image_container = product.findelement(By.CLASS_NAME, 'image-container')
            a_tag = image_container.findelement(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            href_list.append(href)
            print(len(href_list))

    def obtain_item_type(self):
        #item type info is stored in 'breadcrumb_list' element
        
        breadcrumb_list_xpath = '//*[@id="main-content"]/div[1]/nav/ul'
        breadcrumb_list = self.driver.find_element(By.XPATH, breadcrumb_list_xpath)
        catagory_containers = breadcrumb_list.find_elements(By.TAG_NAME, 'li')

        for catagory in catagory_containers:
            a_tag = catagory.find_element(By.TAG_NAME, 'a')
            element = a_tag.find_element(By.TAG_NAME, 'span')
            outer_html = element.get_attribute('outerHTML')
            catagories = regex.search('itemprop="name">(.*)</span>', outer_html).group(1)
            
            print(str(catagories))





    def download_image(self) -> None:
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
    

class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features
    '''
    def __init__(self) -> None:
        pass

    def upload_image_to_datalake(self):
        pass




# List of womens items categories to navigate to, input to a function
womens_items = ['Tops', 'Hoodies & Sweatshirts', 'Dresses & Jumpsuits', 'Coats & Jackets', 'Knitwear'
                'Bottoms', 'Jeans', 'Lingerie', 'Loungewear', 'Jewellry & Watches', 'Accessories', 'Shoes']

# List of mens items categories to navigate to, input to a function
mens_items = ['Hoodies & Sweatshirts', 'T-Shirts', 'Shirts', 'Jumpers & Knitwear', 'Coats & Jackets', 'Trousers'
                'Jeans', 'Joggers and Track Pants', 'Shorts and Swim', 'Jewellry & Watches',' Hats & Caps', 
                'Socks', 'Loungewear & Underwear', 'Accessories', 'Shoes']

# List of features to scrape from each item, input to a function
feature = ['Price', 'Sizes', 'Colour', 'Brand', 'Discounted', 'Review Score', 'Number of Reviews']

def run_scraper():
    URL = "https://www2.hm.com/en_gb/productpage.0967440005.html"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    driver.obtain_item_type()
    
    # TODO: Be able to navigate to Womens Tops by uncommenting below
    gender = 'womens'
    item_type = 'Tops'
    # driver.navigate_to_item_type_page(gender, item_type)


if __name__ == '__main__':
    run_scraper()

