from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class PagelinkingFeatureditems(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_featureditems(self):
        driver = self.driver
        driver.get(self.base_url)
        
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Fashion").click()
        driver.find_element_by_css_selector("img.listing-image").click()
        self.assertTrue("6-inch Black Heel" in driver.find_element_by_tag_name("body").text)   
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        driver.find_element_by_link_text("Books").click()
        driver.find_element_by_css_selector("#booksCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Harry Potter and the Chamber of Secrets" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Harry Potter and the Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        driver.find_element_by_link_text("Electronic & IT Gadget").click()
        driver.find_element_by_css_selector("#electronic-it-gadgetCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Samsung Galaxy Camera" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Samsung Galaxy Camera", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
