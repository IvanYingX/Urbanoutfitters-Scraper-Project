from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import urllib
import urllib.request
import tempfile
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm
import boto3
import re as regex
import time
import json
import sql_data

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
        chrome_options=Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window() #maximised window helps reduce the frequency of unclickable elements
        self.accept_cookies()
        
    
    def accept_cookies(self, css: str = '#onetrust-accept-btn-handler') -> None:
        '''
        This function is used to close the accept cookies pop-up

        Returns:
            None
        '''
        accept_cookies_css = css
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, accept_cookies_css)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
        except:
            pass

    
    def navigate_to_male(self, html: str = 'https://www2.hm.com/en_gb/men/shop-by-product/view-all.html') -> None:
        '''
        This function 'navigates' to the all products male page.

        Returns:
            None
        '''
        male_html = html
        self.driver.get(male_html)

    
    def navigate_to_female(self, html: str = 'https://www2.hm.com/en_gb/ladies/shop-by-product/view-all.html') -> None:
        '''
        This function navigates to the all products female page.

        Returns:
            None
        '''
        female_html = html
        self.driver.get(female_html)


    def load_more(self, css: str = '#page-content > div > div:nth-of-type(2) > div:nth-of-type(2)') -> None:
        '''
        This function waits for the pressence of the 'load_more' button and clicks using actionchains to avoid 
        "Element is not clickable" error.

        Returns:
            None
        '''
        long_wait = WebDriverWait(self, 10)
        load_page_css = css
        load_page = self.driver.find_element(By.CSS_SELECTOR, load_page_css)
        button = load_page.find_element(By.TAG_NAME, 'button')
        element = long_wait.until(EC.element_to_be_clickable(button))
        actionChains = ActionChains(self.driver)
        actionChains.context_click(element).click().perform()
        

    def obtain_product_href(self, css: str = '#page-content > div > div:nth-of-type(2) > ul') -> list:
        '''
        This function locates all products in the observable product_container and itterates through, obtaining 
        all product hrefs. Product hrefs are then appended to href_list. 

        NOTE: # OF HREFS IS NOT EQUAL TO # OF PRODUCTS VISITED BY SCRAPER. 
            H&M STORES MULTIPLE VARIATIONS (COLOUR/DESIGN) OF THE SAME PRODUCT IN A SINGLE HREF.
            NOT QUITE SURE HOW TO FIX THIS.

            AM I REVISITING THE SAME PRODUCT AT ANY POINT?

        Returns:
            List
        '''
        href_list = []
        product_container_css = css
        product_container = self.driver.find_element(By.CSS_SELECTOR, product_container_css)
        products = product_container.find_elements(By.TAG_NAME, 'li')

        for product in products:
            a_tag = product.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')

            if href in href_list:
                pass
            else:
                href_list.append(href)
        return(href_list)
        

    def obtain_product_type(self, css: str = '#main-content > div:first-of-type > nav > ul') -> list:
        '''
        This function obtains the product catagorisation from the 'breadcrumb' container and appends it to 
        product_catagorisation list.  

        TODO: CURRENTLY THE PRODUCT NAME IS STORED AS THE FINAL INDEX IN product_catagorisation, THIS IS NOT NECCESSARY
            SINCE THE NAME IS STORED SEPERATELY IN THE product_dict.

        Returns:
            List
        '''
        #item type info is stored in 'breadcrumb_list' element
        product_catagorisation = []
        breadcrumb_list_css = css
        breadcrumb_list = self.driver.find_element(By.CSS_SELECTOR, breadcrumb_list_css)
        catagory_containers = breadcrumb_list.find_elements(By.TAG_NAME, 'li')

        for catagory in catagory_containers[1:]:
            a_tag = catagory.find_element(By.TAG_NAME, 'a')
            element = a_tag.find_element(By.TAG_NAME, 'span')
            outer_html = element.get_attribute('outerHTML')
            catagories = regex.search('itemprop="name">(.*)</span>', outer_html).group(1)
            product_catagorisation.append(catagories)

        return(product_catagorisation)

    
    def obtain_product_price(self, css: str='#product-price > div > span', 
        css_reduced: str='#product-price > div > div:first-of-type > span') -> str:

        '''
        This function locates the price element on product page from the outerHTML and returns a cleaned string.

        TODO: IF REDUCED, CONVEY THIS IN PRODUCT DICTIONARY.

        Returns:
            Str
        '''
        price_css = css
        reduced_price_css = css_reduced
        try:
            outer_html = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, price_css))).get_attribute("outerHTML")
            price = regex.search('>(.*)</span>', outer_html).group(1)
        except: #if the price is reduced, the element is contained in a seperate xpath
            price = self.driver.find_element(By.CSS_SELECTOR, reduced_price_css)
            outer_html = price.get_attribute('outerHTML')
            price = regex.search('>(.*)</span>', outer_html).group(1)
        price_float = float(price[1:])
        return price_float


    def obtain_product_details(self, css: str = 
        '#main-content > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > menu > ul > li:first-of-type > button') -> dict:

        '''
        This function first locates the details button element and clicks. The elements containing product details are then 
        located and iterated through. Key's are obtained from the outerHTML of the dt tag. Values are obtained from the 
        outerHTML of the dd tags. One dt tag can have multiple dd children and so the dd elements are looped through to obtain
        each value, values then append to a list. Key:values pairs are then appended the product details_dict.

        Returns:
            dict
            
        '''
        #locate and click details tab
        button_css = css
        button = self.driver.find_element(By.CSS_SELECTOR, button_css)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
        details_dict = {}
        #locate general drawer element
        asides = self.driver.find_elements(By.TAG_NAME, 'aside')
        side_drawer = asides[len(asides)-1]
        #details container xpath changes with each product, 
        #the general container is located via TAGNAME and then the correct child is located.
        details = side_drawer.find_element(By.CSS_SELECTOR, 'div > div > div > dl')
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

        for key, value in details_dict.items():
            if len(value) == 1:
                details_dict[key] = value[0]
                if details_dict[key].isnumeric():
                    details_dict[key] = int(details_dict[key])

        return details_dict
    

    def obtain_image_src(self, css: str = 
        '#main-content > div:nth-of-type(2) > div:nth-of-type(2) > div:first-of-type > figure:first-of-type > div > img') -> str:

        '''
        This function locates the first image element and returns the src attribute. 

        NOTE: THIS CAN BE DONE WITHOUT ACTUALLY LOADING THE IMAGES, WHICH CAN IMPROVE SPEED.
        IMAGE RENDERING IS DISABLED

        Returns:
            Str
        '''
        image_css = css
        image = self.driver.find_element(By.CSS_SELECTOR, image_css)
        src = image.get_attribute('src')
        return src


    def obtain_product_sizes(self, id: str = 'picker-1') -> list:
        '''
        This function locates the element containing all product sizes. The container is then iterated through, 
        ignoring the first and last elements which are not sizes. The sizes are obtained from the elements' outerHTML
        and appended to the sizes list. 

        Returns:
            list
        '''
        container_id = id
        sizes = []
        container = self.driver.find_element(By.ID, container_id)
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
            Dict
        '''
        product_type = self.obtain_product_type()
        product_name = product_type[len(product_type)-1]
        product_price = self.obtain_product_price()
        product_details = self.obtain_product_details()
        image_src = self.obtain_image_src()
        product_dict = {'Product':product_name, 'Product Type':product_type, 'Price':product_price, 'SRC':image_src}
        product_dict.update(product_details)
        
        return product_dict


    def scrape_gender(self) -> dict:
        '''
        This function obtains a prompt from self.check_scraper_ready(), while prompt is False, more pages are loaded. 
        Then iterate through href_list and self.obtain_product_type(). 

        For the driver to run quickly and efficiently, all desired pages should be loaded before proceeding with other functions. 

        Returns:
            dict
        '''
        
        page_dict = {}
        href_list = self.obtain_product_href()
        i = 0
        amount_to_scrape = 3

        for href in href_list:
            try:
                self.driver.get(href)
            
                product_dict = self.scrape_product()
            # write the product dictionary to a JSON file.
                product_id = product_dict['Art. No.']
            # with open(f"{product_id}.json", 'w') as fp:
            #     json.dump(product_dict, fp)
            #     product_id = product_dict['Art. No.']
                product_dict.update({'URL': href})
                page_dict.update({product_id:product_dict})
                i += 1
                print(i)
            except:
                pass
            # if i >= amount_to_scrape:
            #     break
            

        return page_dict
        

    def scrape_all(self, rds_params, pages = 0) -> None:
        '''
        This function calls self.scrape_gender(), upon completion of this operation, the function
        to navigate to the next gender is called and commences self.scape_gender() again. 
        
        NOTE: time.time() IS USED TO TIME THE PROCESS FOR OPTIMISATION.

        Returns:
            None
        '''
        start = time.time()
        print(start)
        #scrape female
        self.navigate_to_female()
        for _ in range(pages):
            self.load_more()

        female_page_dict = self.scrape_gender()
        # write the page dictionary to a JSON file.  
        with open(f"female_page_dict.json", 'w') as fp:
            json.dump(female_page_dict, fp)

        
        #scrape male
        self.navigate_to_male()
        for _ in range(pages):
            self.load_more()

        male_page_dict = self.scrape_gender()
        # write the page dictionary to a JSON file.  
        with open(f"male_page_dict.json", 'w') as fp:
            json.dump(male_page_dict, fp)

        end = time.time()
        print(end - start)

        female_page_dict.update(male_page_dict)
        sql_data.sql_data(female_page_dict, rds_params)

        return female_page_dict
    
    def close_down(self):
        self.driver.close()

    
class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features.
    '''
    def __init__(self, s3_params) -> None:
        self.aws_access_key_id = s3_params['access_key_id']
        self.aws_secret_access_key = s3_params['secret_access_key']
        

    def upload_images_to_datalake(self, data) -> None:
        '''
        This function obtains both an image SRC and ID from the page_dict.json file. A tempory directory is constructed and 
        each SRC is accesses, downloaded and then uploaded to the S3 bucket using the ID as a file name. 

        TODO: TIDY THIS CODE, LOOKS SHITTY.
        TODO: IMPORT THE PRIVATE CREDENTIALS VIA FILE FORMATE FOR SECURITY

        Returns:
            None
        '''

        image_list=[]
        for key, item in data.items():
            image_list.append((key, item['SRC']))

        session = boto3.Session( 
        aws_access_key_id = self.aws_access_key_id,
        aws_secret_access_key = self.aws_secret_access_key
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
    
    # s3_bucket_credentials, rds_credentials = data_storage_credentials_from_json()
    s3_bucket_credentials, rds_credentials = data_storage_credentials_from_cli()
    
    URL = "https://www2.hm.com/en_gb/index.html"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    # data = driver.scrape_all(rds_credentials, pages = 1)
    data = driver.scrape_all(rds_credentials)
    driver.close_down()
    store_data = StoreData(s3_bucket_credentials)
    store_data.upload_images_to_datalake(data)

def data_storage_credentials_from_json():
    # with open('data_storage_credentials.json') as json_file:
    with open('Urbanoutfitters-Scraper-Project/data_storage_credentials.json') as json_file:
        storage_credentials = json.load(json_file)
    s3_bucket_credentials = storage_credentials['s3_bucket']
    rds_credentials = storage_credentials['rds']
    return (s3_bucket_credentials, rds_credentials)

def data_storage_credentials_from_cli():
    
    print('Please enter the S3 bucket credentials:')
    access_key_id = input('Access Key ID: ')
    secret_access_key = input('Secret Access Key: ')
    s3_bucket_credentials = {'access_key_id': access_key_id, 'secret_access_key': secret_access_key}

    print('Please enter the RDS credentials:')
    DATABASE_TYPE = input('Database Type: ')
    DBAPI = input('DB API: ')
    ENDPOINT = input('Endpoint: ')
    USER = input('Username: ')
    PASSWORD = input('Password: ')
    PORT = input('Port: ')
    DATABASE = input('Database: ')
    rds_credentials = {
        'DATABASE_TYPE': DATABASE_TYPE,
        'DBAPI': DBAPI,
        'ENDPOINT': ENDPOINT,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'PORT': PORT,
        'DATABASE': DATABASE
    }
    return (s3_bucket_credentials, rds_credentials)
    

if __name__ == '__main__':
    run_scraper()
