from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class CollectiondetailOwn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_collectiondetail_own(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")        
        addcollection(driver, self)
        
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 likes this.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 likes this.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 likes this.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
               
        driver.find_element_by_link_text("test").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("testcollection").click()
        
        driver.find_element_by_link_text("Edit Collection").click()
        try: self.assertEqual("Update Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 

        driver.find_element_by_link_text("New collections").click()
        try: self.assertEqual("Collections", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("testcollection (1 items)").click()        
        driver.find_element_by_link_text("Manage Items").click()
        try: self.assertEqual("Add Items to Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        
        driver.find_element_by_link_text("New collections").click()
        try: self.assertEqual("Collections", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("testcollection (1 items)").click()
        
        deletecollection(driver, self)
           
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
