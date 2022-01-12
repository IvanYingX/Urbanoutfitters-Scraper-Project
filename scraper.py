from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import urllib.request
import tempfile
from tqdm import tqdm
import boto3
import re as regex
from time import sleep



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

    
    def load_more(self):
        '''
        This function waits for the pressence of the 'load_more' button and clicks indefinitely.
        A Timeout exception is thrown if the button cannot be found (i.e. at end of page).

        Returns:
            None
        '''
        wait = WebDriverWait(self, 1)
        load_page_xpath = '//*[@id="page-content"]/div/div[2]/div[2]'
        load_page = self.driver.find_element(By.XPATH, load_page_xpath)
        button = load_page.find_element(By.TAG_NAME, 'button')
        while True:
            try:
                element = wait.until(EC.element_to_be_clickable(button))
                element.click()
            except TimeoutException:
                break



    def scrape_href(self):
        '''
        This function locates all products in the observable product_container and itterates through, obtaining 
        all product hrefs. Product hrefs are then appended to href_list. 

        Returns:
            None
        '''
        href_list = []


        product_container_xpath = '//*[@id="page-content"]/div/div[2]/ul'
        product_container = self.driver.find_element(By.XPATH, product_container_xpath)
        products = product_container.find_elements(By.TAG_NAME, 'li')

        for product in products:
            article = product.find_element(By.CLASS_NAME, 'hm-product-item')
            image_container = article.find_element(By.CLASS_NAME, 'image-container')
            a_tag = image_container.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            href_list.append(href)
            print(href_list)
        return(href_list)
        

    def obtain_product_type(self):
        '''
        This function obtains the product catagorisation from the 'breadcrumb' container and appends it to 
        product_catagorisation list.   

        Returns:
            None
        '''
        #item type info is stored in 'breadcrumb_list' element
        product_catagorisation = []
        breadcrumb_list_xpath = '//*[@id="main-content"]/div[1]/nav/ul'
        breadcrumb_list = self.driver.find_element(By.XPATH, breadcrumb_list_xpath)
        catagory_containers = breadcrumb_list.find_elements(By.TAG_NAME, 'li')

        for catagory in catagory_containers:
            a_tag = catagory.find_element(By.TAG_NAME, 'a')
            element = a_tag.find_element(By.TAG_NAME, 'span')
            outer_html = element.get_attribute('outerHTML')
            catagories = regex.search('itemprop="name">(.*)</span>', outer_html).group(1)
            product_catagorisation.append(catagories)

        return(product_catagorisation)


    def scrape_data(self):
        product_dict = {}

        href_list = self.scrape_href()

        for href in href_list:
            self.driver.click(href)
            value = self.obtain_product_type()
            item = {[href]:[value]}
            product_dict.append(item)
            print(product_dict)
        return(product_dict)
         


        


    def download_image(self) -> None:
        s3_client = boto3.client('s3')

        image_container = self.driver.find_element(By.CLASS_NAME, 'product-detail-main-image-container')
        image = image_container.find_element(By.TAG_NAME, 'img')
        src = image.get_attribute('src')
        

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, scr in enumerate(tqdm(src)):
                urllib.request.urlretrieve(scr, f'{temp_dir}/image_{i}.png')
                s3_client.upload_file(f'{temp_dir}/image_{i}.png', 'urbanoutfittersbucket', f'dest_img_{i}.png')



    

class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features
    '''
    def __init__(self) -> None:
        pass

    def upload_image_to_datalake(self):
        pass


def run_scraper():
    URL = "https://www2.hm.com/en_gb/ladies/shop-by-product/view-all.html"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    driver.scrape_href()
    
    # TODO: Be able to navigate to Womens Tops by uncommenting below
    gender = 'womens'
    item_type = 'Tops'
    # driver.navigate_to_item_type_page(gender, item_type)


if __name__ == '__main__':
    run_scraper()

