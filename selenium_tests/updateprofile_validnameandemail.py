from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class UpdateprofileValidnameandemail(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_updateprofile_validnameandemail(self):
        driver = self.driver      
        login(driver, self, "zgal", "asd")
        
        driver.find_element_by_link_text("MABEL").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("tester")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("test@test.com")        
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)        
        try: self.assertEqual("tester", driver.find_element_by_id("id_name").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test@test.com", driver.find_element_by_id("id_email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))        
                         
        #manual revert/cleanup#       
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Mabel")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("zgal@zgal.com")        
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)             
        
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
