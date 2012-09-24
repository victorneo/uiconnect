from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, additem, deleteitem

class Itemedit_normal(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_itemedit_normal(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")
        additem(driver, self)       
        driver.find_element_by_link_text("Edit Item").click()        
        
        try: self.assertEqual("Update Item", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("test!")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("testing123!")
        driver.find_element_by_id("id_price").clear()
        driver.find_element_by_id("id_price").send_keys("10")
        driver.find_element_by_id("submit-id-submit").click()
       
        try: self.assertEqual("test!", driver.find_element_by_css_selector("h1").text) 
        except AssertionError as e: self.verificationErrors.append(str(e))               
        self.assertTrue("Item updated." in driver.find_element_by_tag_name("body").text)       
        self.assertTrue("testing123!" in driver.find_element_by_tag_name("body").text)       
        self.assertTrue("USD 10" in driver.find_element_by_tag_name("body").text)        
        
        deleteitem(driver,self)        
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
