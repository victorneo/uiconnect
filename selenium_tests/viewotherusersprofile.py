from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class Viewotherusersprofile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_viewotherusersprofile(self):
        driver = self.driver
        login(driver, self, "zgal", "asd") 
        
        #pick an item that does not belong to user:zgal#
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("asd", driver.find_element_by_link_text("asd").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("asd").click()
        
        try: self.assertEqual("asd", driver.find_element_by_css_selector("h5").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2 items, 0 collections.", driver.find_element_by_css_selector("small").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Followed by 0 users.", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/p[3]/small").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        #driver.find_element_by_id("btn_follow").click()
        #try: self.assertEqual("Followed by 1 user.", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/p[3]/small").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))
        #driver.find_element_by_id("btn_follow").click()
        #try: self.assertEqual("Followed by 0 users.", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/p[3]/small").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Items by asd", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Rubik Cube" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)        
        try: self.assertEqual("Collections by asd", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("asd has yet to create a collection.", driver.find_element_by_css_selector("div.span9 > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
                
        driver.find_element_by_css_selector("img[alt=\"Rubik Cube\"]").click()
        try: self.assertEqual("Rubik Cube", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("asd").click()
        try: self.assertEqual("asd", driver.find_element_by_css_selector("h5").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("2 items, 0 collections.", driver.find_element_by_css_selector("small").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Followed by 0 users.", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/p[3]/small").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Items by asd", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Rubik Cube" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)        
        try: self.assertEqual("Collections by asd", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("asd has yet to create a collection.", driver.find_element_by_css_selector("div.span9 > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_xpath("//img[@alt=\"Elmo's ABC Book\"]").click()        
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        driver.find_element_by_link_text("LOGOUT").click()
            
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
