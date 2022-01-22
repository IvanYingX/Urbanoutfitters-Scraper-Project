from botocore.utils import should_bypass_proxies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import urllib
import urllib.request
import tempfile
from sklearn.feature_extraction import image
from tqdm import tqdm
import boto3
import re as regex
from time import sleep
import json

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
        prefs = {'profile.managed_default_content_settings.images': 2}
        
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window() #maximised window helps reduce the frequency of unclickable elements
        self.accept_cookies()
        
    
    def accept_cookies(self, xpath: str='//*[@id="onetrust-accept-btn-handler"]') -> None:
        '''
        This function is used to close the accept cookies pop-up

        Returns:
            None
        '''
        accept_cookies_xpath = xpath
        try:
            button = self.driver.find_element(By.XPATH, accept_cookies_xpath)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
        except:
            pass


    def load_more(self, xpath: str='//*[@id="page-content"]/div/div[2]/div[2]'):
        '''
        This function waits for the pressence of the 'load_more' button and clicks using actionchains to avoid 
        "Element is not clickable" error.
        Returns:
            None
        '''
        long_wait = WebDriverWait(self, 10)
        load_page_xpath = xpath
        load_page = self.driver.find_element(By.XPATH, load_page_xpath)
        button = load_page.find_element(By.TAG_NAME, 'button')
        element = long_wait.until(EC.element_to_be_clickable(button))
        actionChains = ActionChains(self.driver)
        actionChains.context_click(element).click().perform()


    def check_scraper_ready(self, xpath: str='//*[@id="page-content"]/div/div[2]/div[2]/h2'):
        '''
        This function obtains the number of items visible to the driver and the total number of items. 
        If all possible items are shown, then scraper is ready, returns True. 

        Returns:
            Bool
        '''
        load_more_xpath = xpath
        load_more_element = self.driver.find_element(By.XPATH, load_more_xpath)
        items_shown = load_more_element.get_attribute('data-items-shown')
        total_items = load_more_element.get_attribute('data-total')

        x = int(items_shown)
        y = int(total_items)
        print(f'The number of items visible is {x}')
        if x > 10: #currently using placeholder number for testing
            print('Scraper is ready')
            return True 
        else:
            print('Scraper is not ready')
            return False        


    def obtain_product_href(self, xpath: str='//*[@id="page-content"]/div/div[2]/ul'):
        '''
        This function locates all products in the observable product_container and itterates through, obtaining 
        all product hrefs. Product hrefs are then appended to href_list. 

        Returns:
            List
        '''
        href_list = []
        product_container_xpath = xpath
        product_container = self.driver.find_element(By.XPATH, product_container_xpath)
        products = product_container.find_elements(By.TAG_NAME, 'li')

        for product in products[:10]:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            href_list.append(href)
        return(href_list)
        

    def obtain_product_type(self):
        '''
        This function obtains the product catagorisation from the 'breadcrumb' container and appends it to 
        product_catagorisation list.   

        Returns:
            List
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

    
    def obtain_product_price(self, xpath: str='//*[@id="product-price"]/div/span', xpath_reduced: str='//*[@id="product-price"]/div/div[1]/span') -> str:
        '''
        This function locates the price element on product page from the outerHTML and returns a cleaned string.

        Returns:
            Str
        '''
        price_xpath = xpath
        reduced_price_xpath = xpath_reduced
        try:
            price = self.driver.find_element(By.XPATH, price_xpath)
            outer_html = price.get_attribute('outerHTML')
            price = regex.search('>(.*)</span>', outer_html).group(1)
        except:#if the price is reduced, the element is contained in a seperate xpath
            price = self.driver.find_element(By.XPATH, reduced_price_xpath)
            outer_html = price.get_attribute('outerHTML')
            price = regex.search('>(.*)</span>', outer_html).group(1)
        return price


    def obtain_product_details(self, button_xpath: str='//*[@id="main-content"]/div[2]/div[2]/div[2]/menu/ul/li[1]/button',
        xpath_1: str='//*[@id="side-drawer-2"]/div/div/div/dl', xpath_2: str='//*[@id="side-drawer-3"]/div/div/div/dl') -> dict:
        '''
        This function first locates the details button element and clicks. The elements containing product details are then 
        located and iterated through. Key's are obtained from the outerHTML of the dt tag. Values are obtained from the 
        outerHTML of the dd tags. One dt tag can have multiple dd children and so the dd elements are looped through to obtain
        each value, values then append to a list. Key:values pairs are then appended the product details_dict.

        Returns:
            dict
        '''
        button_xpath = button_xpath
        button = self.driver.find_element(By.XPATH, button_xpath)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
        details_dict = {}
        details_xpath_1 = xpath_1
        details_xpath_2 = xpath_2

        try:
            details = self.driver.find_element(By.XPATH, details_xpath_1)
        except:
            details = self.driver.find_element(By.XPATH, details_xpath_2)

        elements = details.find_elements(By.TAG_NAME, 'div') 
        for element in elements:
            detail = element.find_element(By.TAG_NAME, 'dt')
            detail_outer_html = detail.get_attribute('outerHTML')
            key = regex.search('>(.*)</dt>', detail_outer_html).group(1)
            comments = []
            values = element.find_elements(By.TAG_NAME, 'dd')
            for value in values:
                outer_html = value.get_attribute('outerHTML')
                comment = regex.search('>(.*)</dd>', outer_html).group(1)
                comments.append(comment)
            details_dict.update({key:comments})
        return details_dict


    def obtain_image_src(self, xpath: str='//*[@id="main-content"]/div[2]/div[2]/div[1]/figure[1]/div/img') -> str:
        '''
        This function locates the first image element and returns the src attribute. 

        Returns:
            Str
        '''
        image_xpath = xpath
        image = self.driver.find_element(By.XPATH, image_xpath)
        src = image.get_attribute('src')
        return src


    def obtain_product_sizes(self, xpath: str='//*[@id="picker-1"]/ul') -> list:
        '''
        This function locates the element containing all product sizes. The container is then iterated through, 
        ignoring the first and last elements which are not sizes. The sizes are obtained from the elements' outerHTML
        and appended to the sizes list. 

        Returns:
            list
        '''
        sizes_xpath = xpath
        sizes = []
        container = self.driver.find_element(By.XPATH, sizes_xpath)
        elements = container.find_elements(By.TAG_NAME, 'li')
        for element in elements [1:len(elements)-1]:
            span = element.find_element(By.TAG_NAME, 'span')
            outer_html = span.get_attribute('outerHTML')
            size = regex.search('>(.*)</span>', outer_html).group(1)
            sizes.append(size)
        return sizes


    def scrape_product(self) -> dict:
        '''
        This function calls all product specific methods to obtain all product data. The data is then stored in a 
        dictionary. 

        Returns:
            dict
        '''
        product_type = self.obtain_product_type()
        product_name = product_type[len(product_type)-1]
        product_price = self.obtain_product_price()
        product_details = self.obtain_product_details()
        image_src = self.obtain_image_src()
        product_dict = {'Product':product_name, 'Product Type':product_type, 'Price':product_price, 'SRC':image_src}
        product_dict.update(product_details)
        return product_dict


    def scrape_page(self):
        '''
        This function obtains a prompt from self.check_scraper_ready(), if prompt is False, more pages are loaded. 
        If prompt is True, self.scrape_href() then iterate through href_list and self.obtain_product_type(). 

        The reason for structuring the code this way is as follows: 
        Unless all desired pages are loaded before scraping, the driver will try to locate elements which it has already
        located and perform self.obtain_product_href() and self.obtain_product_type() on the same items over and over.
        
        For the driver to run quickly and efficiently, all pages should be loaded before proceeding with other functions. 
        '''

        # this function causes errors when the page finishes scraping, the program attempts to obtain all product
        # hrefs again after scraping.

        # prompt = self.check_scraper_ready() 
        # while prompt is False: # See line 102, atm the scraper should be ready to proceed when > 100 items are visible. 
        #     self.load_more()
        #     prompt = self.check_scraper_ready() 
        # while prompt is True:

        page_dict = {}
        href_list = self.obtain_product_href()
        for href in href_list:
            self.driver.get(href)
            product_dict = self.scrape_product()
            # write the product dictionary to a JSON file.
            product_id = product_dict.get('Art. No.')[0]
            with open(f"{product_id}.json", 'w') as fp:
                json.dump(product_dict, fp)
                product_id = product_dict.get('Art. No.')


            page_dict.update({product_id[0]:product_dict})

        # write the page dictionary to a JSON file.  
        with open(f"page_dict.json", 'w') as fp:
            json.dump(page_dict, fp)

    
class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features.

    Returns:
        None
    '''
    def __init__(self) -> None:
        pass

    def upload_image_to_datalake():
        '''
        This function obtains both an image SRC and ID from the page_dict.json file. A tempory directory is constructed and 
        each SRC is accesses, downloaded and then uploaded to the S3 bucket using the ID as a file name. 

        Returns:
            None
        '''
        with open('page_dict.json') as json_file:
            page_dict = json.load(json_file)
        key = "SRC"
        src_list = [sub[key] for sub in page_dict.values() if key in sub.keys()]
        image_id_list = list(page_dict.keys())
        image_list = []
        for (a,b) in zip(image_id_list, src_list):
            image = (a,b)
            image_list.append(image)
        print(image_list)

        #TODO import the private credentials via file format for security purposes
        session = boto3.Session( 
        aws_access_key_id='AKIA3E73GVKXZ5IQTHWG',
        aws_secret_access_key='cUy4Gb/EJ8DqtRqCGN/gk1ZrhZG/yz4Ve98XWsdI'
        )
        s3 = session.client('s3')
        # Create a temporary directory, so you don't store images in your local machine
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, image in enumerate(tqdm(image_list)):
                # headers allow bypass of the website security restrictions
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
                id = image[0]
                src = image[1]

                request_ = urllib.request.Request(src,None,headers) #The assembled request
                response = urllib.request.urlopen(request_)# store the response
                f = open(f'{temp_dir}/image_{i}.jpg','wb')
                f.write(response.read())           
                s3.upload_file(f'{temp_dir}/image_{i}.jpg', 'urbanoutfittersbucket', f'{id}.jpg')
        





def run_scraper():
    #URL = 'https://www2.hm.com/en_gb/productpage.1019417008.html'
    URL = "https://www2.hm.com/en_gb/ladies/shop-by-product/view-all.html"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    driver.scrape_page()
    
    
if __name__ == '__main__':
    run_scraper()

#StoreData.upload_image_to_datalake()


