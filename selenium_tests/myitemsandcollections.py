from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, additem

class Mitemsandcollections(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_myitemsandcollections(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")       
        
        #insert a test item#
        additem(driver, self) 
        
        driver.find_element_by_link_text("DASHBOARD").click()
        driver.find_element_by_link_text("My items and collections").click()        
        
        driver.find_element_by_xpath("(//a[contains(text(),'Manage Images')])[3]").click()
        try: self.assertEqual("Images for test", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Go back").click()        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        driver.find_element_by_link_text("DASHBOARD").click()
        driver.find_element_by_link_text("My items and collections").click()  
        try: self.assertEqual("My items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("My Collections", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_xpath("(//a[contains(text(),'Edit Item')])[3]").click()
        try: self.assertEqual("Update Item", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("My items and collections").click()
        try: self.assertEqual("My items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("My Collections", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
                
        driver.find_element_by_xpath("(//a[contains(text(),'Delete Item')])[3]").click()        
        self.assertTrue("Are you sure you want to delete test?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("#listing14 > div.modal-footer > button.btn").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Delete Item')])[3]").click()        
        self.assertTrue("Are you sure you want to delete test?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("#listing14 > div.modal-footer > a.btn.btn-danger").click()
        try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Item has been deleted." in driver.find_element_by_tag_name("body").text)
     
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
