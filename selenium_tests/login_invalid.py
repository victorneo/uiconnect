from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import verifylogin

class LoginInvalid(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_login_invalid(self):
        driver = self.driver      
        driver.get(self.base_url)
        
        driver.find_element_by_link_text("LOGIN").click()       
        verifylogin(driver, self)               
       
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("test")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asd")
        driver.find_element_by_id("submit-id-submit").click()    
        
        verifylogin(driver, self)
       
        self.assertTrue("Invalid login." in driver.find_element_by_tag_name("body").text)                    
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)        
        
if __name__ == "__main__":
    unittest.main()
