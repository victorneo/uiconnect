from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class LoginAllempty(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_login_allempty(self):
        driver = self.driver      
        driver.get(self.base_url)
        driver.find_element_by_link_text("Login").click()
        try: self.assertEqual("Login", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))   
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Login", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        try: self.assertEqual("This field is required.", driver.find_element_by_css_selector("#error_1_id_username > strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("This field is required.", driver.find_element_by_css_selector("#error_1_id_password > strong").text)
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
