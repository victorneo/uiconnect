from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re,os
from common import login, addcollection, deletecollection

class Collectioneditupdateimage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_collectionedit_updateimage(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")

        #insert a test item and collection#
        addcollection(driver, self)
        driver.find_element_by_link_text("Edit Collection").click() 
        
        try: self.assertEqual("Update Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Clear" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_id("image-clear_id").click()
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Collection Updated." in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_link_text("Edit Collection").click()
        try: self.assertEqual("Update Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        self.assertTrue("Clear" not in driver.find_element_by_tag_name("body").text)        
        driver.find_element_by_id("id_image").send_keys(os.path.abspath("C:\Users\hp\Desktop\CSC303\Images\Kids_ABPlush.jpg"))
        driver.find_element_by_id("submit-id-submit").click()
        
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Collection Updated." in driver.find_element_by_tag_name("body").text)        
        
        #manual revert/clean up#
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
