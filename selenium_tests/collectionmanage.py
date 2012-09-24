from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class Collectionmanage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_collectionmanage(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")        
        addcollection(driver, self)
        
        driver.find_element_by_link_text("Manage Items").click()
        try: self.assertEqual("Add Items to Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))         
        select = Select(driver.find_element_by_id("id_listings"))        
        select.deselect_all()
        select.select_by_visible_text("6-inch Black Heel")
        select.select_by_visible_text("Samsung Galaxy Camera")
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Changes saved!" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("6-inch Black Heel" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Samsung Galaxy Camera" in driver.find_element_by_tag_name("body").text)
        
        deletecollection(driver, self)              
        driver.find_element_by_link_text("Logout").click()       
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
