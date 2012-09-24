from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class UpdateprofileSamepwd(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_updateprofile_samepwd(self):
        driver = self.driver      
        login(driver, self, "zgal", "asd")
        
        driver.find_element_by_link_text("Mabel").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("123")
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)         
        driver.find_element_by_link_text("Logout").click()
        
        login(driver, self, "zgal", "123")
        
        driver.find_element_by_link_text("Mabel").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asd")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("asd")
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)         
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
