from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class PagelinkingFeaturednewcollection(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_featurednewcollection(self):
        driver = self.driver
        login(driver, self, "zgal", "asd") 
        
        #simulate new collection, differentiate featured collection and new collection# 
        addcollection(driver, self)
        
        try: self.assertEqual("Featured collections", driver.find_element_by_link_text("Featured collections").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Featured collections").click()
        try: self.assertEqual("Collections", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))     
        self.assertTrue("testcollection" not in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("Harry Potter Book Series" in driver.find_element_by_tag_name("body").text)
        
        
        driver.find_element_by_css_selector("div.collection-preview-image").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("New collections", driver.find_element_by_link_text("New collections").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("New collections").click()
        try: self.assertEqual("Collections", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("testcollection" in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("Harry Potter Book Series" in driver.find_element_by_tag_name("body").text)
        
        driver.find_element_by_xpath("//div[@id='tabContent']/div[2]/a/div").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("New collections").click()
        driver.find_element_by_css_selector("div.collection-preview-image").click()
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))           
        
        #manual revert/clean up#
        deletecollection(driver, self)        
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
