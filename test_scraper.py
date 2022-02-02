import unittest
from scraper import WebDriver


class ScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        URL = "https://www2.hm.com/en_gb/index.html"
        self.driver = WebDriver(URL)
        self.driver.open_the_webpage()
        self.test_url = 'https://www2.hm.com/en_gb/productpage.1029275008.html'
        self.maxDiff = None
    
    # @unittest.skip("Skipping test_obtain_product_type")
    def test_obtain_product_type(self):
        self.driver.navigate_to_male(self.test_url)
        actual_product_type = self.driver.obtain_product_type()
        expected_product_type = ['Women', 'Sweatshirts &amp; Hoodies', 'Sweatshirts', 'Oversized motif-detail sweatshirt']
        self.assertEqual(expected_product_type, actual_product_type)
    
    # @unittest.skip("Skipping test_obtain_product_type")
    def test_product_price(self):
        self.driver.navigate_to_male(self.test_url)
        actual_product_price = self.driver.obtain_product_price()
        print(actual_product_price)
        expected_product_price = 19.99
        # expected_product_price = '£19.99'
        self.assertEqual(expected_product_price, actual_product_price)

    # @unittest.skip("Skipping test_product_details")
    def test_product_details(self):
        
        self.driver.navigate_to_male(self.test_url)
        actual_product_details = self.driver.obtain_product_details()
                
        expected_product_details = {'Length': 'Long', 'Sleeve Length': 'Long sleeve', 'Fit': 'Oversized', 
        'Style': 'Sweatshirt', 'Neckline': 'Crew-neck', 'Composition': 'Cotton 78%, Polyester 22%', 
        'Care instructions': 'Machine wash at 30°', 'Description': ['Light pink/White/Black', 'Boston'], 
        'Concept': 'MODERN CLASSIC', 'Nice to know': 'Conscious choice', 'Art. No.': 1029275008}

        # expected_product_details = {'Length': ['Long'], 'Sleeve Length': ['Long sleeve'], 'Fit': ['Oversized'],
        # 'Style': ['Sweatshirt'], 'Neckline': ['Crew-neck'], 'Composition': ['Cotton 78%, Polyester 22%'],
        # 'Care instructions': ['Machine wash at 30°'], 'Description': ['Light pink/White/Black', 'Boston'],
        # 'Concept': ['MODERN CLASSIC'], 'Nice to know': ['Conscious choice'], 'Art. No.': ['1029275008']}
        
        self.assertEqual(expected_product_details,actual_product_details)
    
    # @unittest.skip("Skipping test_obtain_image_src")
    def test_obtain_image_src(self):

        self.driver.navigate_to_male(self.test_url)
        actual_image_src = self.driver.obtain_image_src()
        expected_image_src = 'https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F61%2Ff4%2F61f41c1afa02441dfa3491d21ad83126b07a8673.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/main]'

        self.assertEqual(expected_image_src,actual_image_src)

    # @unittest.skip("Skipping test_scrape_product")
    def test_scrape_product(self):
        self.driver.navigate_to_male(self.test_url)
        actual_product_dict = self.driver.scrape_product()
        # expected_product_dict = {'Product': 'Oversized motif-detail sweatshirt',
        # 'Product Type': ['Women', 'Sweatshirts &amp; Hoodies', 'Sweatshirts', 'Oversized motif-detail sweatshirt'], 
        # 'Price': '£19.99',
        # 'SRC': 'https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F61%2Ff4%2F61f41c1afa02441dfa3491d21ad83126b07a8673.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/main]',
        # 'Length': ['Long'], 'Sleeve Length': ['Long sleeve'], 'Fit': ['Oversized'],
        # 'Style': ['Sweatshirt'], 'Neckline': ['Crew-neck'], 'Composition': ['Cotton 78%, Polyester 22%'],
        # 'Care instructions': ['Machine wash at 30°'], 'Description': ['Light pink/White/Black', 'Boston'],
        # 'Concept': ['MODERN CLASSIC'], 'Nice to know': ['Conscious choice'], 'Art. No.': ['1029275008']}

        expected_product_dict = {'Product': 'Oversized motif-detail sweatshirt',
        'Product Type': ['Women', 'Sweatshirts &amp; Hoodies', 'Sweatshirts', 'Oversized motif-detail sweatshirt'], 
        'Price': 19.99,
        'SRC': 'https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F61%2Ff4%2F61f41c1afa02441dfa3491d21ad83126b07a8673.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/main]',
        'Length': 'Long', 'Sleeve Length': 'Long sleeve', 'Fit': 'Oversized',
        'Style': 'Sweatshirt', 'Neckline': 'Crew-neck', 'Composition': 'Cotton 78%, Polyester 22%',
        'Care instructions': 'Machine wash at 30°', 'Description': ['Light pink/White/Black', 'Boston'],
        'Concept': 'MODERN CLASSIC', 'Nice to know': 'Conscious choice', 'Art. No.': 1029275008}

        self.assertEqual(expected_product_dict, actual_product_dict)

        

    def tearDown(self) -> None:
        self.driver.close_down()


unittest.main(argv=[''], verbosity=1, exit=False)