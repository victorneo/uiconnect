from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class UpdateprofileAddress(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_updateprofile_ddress(self):
        driver = self.driver      
        login(driver, self, "zgal", "asd")
        
        driver.find_element_by_link_text("MABEL").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        driver.find_element_by_id("id_address").clear()   
        driver.find_element_by_id("submit-id-submit").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)
        
        driver.find_element_by_link_text("Discover").click()
        try: self.assertEqual("discover the newest, the coolest", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("bringing you the newest items on sale!", driver.find_element_by_css_selector("p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//img[@alt=\"Elmo's ABC Book\"]").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("input.btn.btn-large").click()
        self.assertTrue("Added to your shopping cart." in driver.find_element_by_tag_name("body").text)
        
        driver.find_element_by_link_text("SHOPPING CART 1").click()
        try: self.assertEqual("Shopping Cart", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", driver.find_element_by_id("id_address").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("123 Testing the Address Field")
        
        driver.find_element_by_link_text("MABEL").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        #try: self.assertEqual("123 Testing the Address Field", driver.find_element_by_id("id_address").get_attribute("value"))
        #except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_address").clear()   
        driver.find_element_by_id("id_address").send_keys("123 Updated Address Field")
        driver.find_element_by_id("submit-id-submit").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)
        
        driver.find_element_by_link_text("SHOPPING CART 1").click()
        try: self.assertEqual("Shopping Cart", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("123 Updated Address Field", driver.find_element_by_id("id_address").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("123 Modify Address Field")
        
        driver.find_element_by_link_text("MABEL").click()
        try: self.assertEqual("123 Updated Address Field", driver.find_element_by_id("id_address").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        #manual revert/cleanup#  
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("123 Somewhere Over the Rainbow")
        driver.find_element_by_id("submit-id-submit").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Your profile has been updated." in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_link_text("SHOPPING CART 1").click()
        try: self.assertEqual("Shopping Cart", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Empty shopping cart").click()
        
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
