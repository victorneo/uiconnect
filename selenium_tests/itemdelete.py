from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, additem, deleteitem

class Itemdelete(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_itemdelete(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")        
        
        #insert a test item#
        additem(driver, self)
        
        driver.find_element_by_link_text("Delete Item").click()        
        self.assertTrue("Are you sure you want to delete this item?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("div.modal-footer > button.btn").click()        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        deleteitem(driver,self)
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
