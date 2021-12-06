from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

class WebDriver():
    
    def __init__(self, url) -> None:
        self.url = url

    def open_the_webpage(self) -> None:
        # TODO: use a with block to open connection and close when finished
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.accept_all_cookies()
        
    
    def accept_all_cookies(self):
        sleep(1)
        accept_cookies_button = self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
    
    def navigate_to_menu_bar(self):
        pass

    
    def download_image(self) -> None:
        pass


    def navigate_to_item_type_page(self, gender, item_type):
        pass

    def open_item(self):
        pass

    def next_page(self):
        pass

    def scrape_feature_from_page(self, feature):
        pass



class StoreData():

    def __init__(self) -> None:
        pass

    def upload_image_to_datalake(self):
        pass


def run_scraper():
    URL = "https://www.urbanoutfitters.com/en-gb/"
    driver = WebDriver(URL)
    driver.open_the_webpage()


if __name__ == '__main__':
    run_scraper()
