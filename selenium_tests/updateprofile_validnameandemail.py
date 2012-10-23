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
        Select(driver.find_element_by_id("id_converted_currency")).select_by_visible_text("Singapore Dollars")        
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)        
        try: self.assertEqual("tester", driver.find_element_by_id("id_name").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test@test.com", driver.find_element_by_id("id_email").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("All Categories").click()
        try: self.assertEqual("All Categories", driver.find_element_by_link_text("All Categories").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        driver.find_element_by_css_selector("img[alt=\"6-inch Black Heel\"]").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("SGD" in driver.find_element_by_tag_name("body").text)
                         
        #manual revert/cleanup#
        driver.find_element_by_link_text("TESTER").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))         
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Mabel")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("zgal@zgal.com")
        Select(driver.find_element_by_id("id_converted_currency")).select_by_visible_text("US Dollars")
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)        
        
        driver.find_element_by_link_text("All Categories").click()
        try: self.assertEqual("All Categories", driver.find_element_by_link_text("All Categories").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        driver.find_element_by_css_selector("img[alt=\"6-inch Black Heel\"]").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))          
        try: self.assertEqual("USD 49.9", driver.find_element_by_xpath("//div[@id='listing-info']/div[2]/p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
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
