from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class ItemdetailQty1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_itemdetail_qty1(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")        
        
        #insert a test collection and item#
        addcollection(driver, self)
        driver.find_element_by_css_selector("div.thumbnail-wrapper").click()        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Edit Item").click()
        try: self.assertEqual("1", driver.find_element_by_id("id_quantity").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("LOGOUT").click()
        
        login(driver, self, "ace", "asd")         
        driver.find_element_by_link_text("New collections").click()
        driver.find_element_by_xpath("//table[@id='collections']/tbody/tr[2]/td/div/a/div").click()
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.thumbnail-wrapper").click()        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))                
        try: self.assertEqual("Hurry - only 1 left!", driver.find_element_by_css_selector("small").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("LOGOUT").click()
        
        #manual revert/clean up
        login(driver, self, "zgal", "asd")     
        driver.find_element_by_link_text("New collections").click()
        driver.find_element_by_xpath("//table[@id='collections']/tbody/tr[2]/td/div/a/div").click()
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
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
