from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class Collectiondelete(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_collectiondelete(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")   

        #insert a test collection and item#
        addcollection(driver, self)
        
        driver.find_element_by_link_text("Delete Collection").click()      
        self.assertTrue("Are you sure you want to delete this collection?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("div.modal-footer > button.btn").click() 
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
