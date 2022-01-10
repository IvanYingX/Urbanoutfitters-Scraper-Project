# for i in range(10):
        #     try:
        #         product_container_xpath = '//*[@id="page-content"]/div/div[2]/ul'
        #         container_xpath = product_listing_xpath + '/div[' + str(i+2) + ']'
        #         load_more_xpath = product_listing_xpath + '/div[' + str(i+3) + ']'


        #         product_listing = self.driver.find_element(By.XPATH, product_listing_xpath)
        #         container = self.driver.find_element(By.XPATH, container_xpath)
        #         product_list = container.find_elements(By.TAG_NAME, 'li')
        #         for product in product_list:
        #             a_tag = product.find_element(By.TAG_NAME, 'a')
        #             link = a_tag.get_attribute('href')
        #             href_list.append(link)
        #         print(len(href_list))
                    

        #         load_more = product_listing.find_element(By.XPATH, load_more_xpath)
        #         load_more_button = load_more.find_element(By.TAG_NAME, 'button')
        #         load_more_button.click()
        #         sleep(3)
        #     except:
        #         pass