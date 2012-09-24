from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, os
from common import login, additem, deleteitem

class Itemmanage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_itemmanage(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")       
        additem(driver, self)           
        driver.find_element_by_link_text("Manage Images").click()
        
        try: self.assertEqual("Current Images for test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Upload a new image", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))       
        driver.find_element_by_name("img").send_keys("C:\Users\hp\Desktop\CSC303\Images\BooksHPBoxset.jpg")
        #driver.find_element_by_name("img").send_keys(os.path.abspath("C:\Users\hp\Desktop\CSC303\Images\munwahkopi.jpg"))        
        #driver.find_element_by_link_text("Remove").click()
        #driver.find_element_by_name("img").send_keys("C:\Users\hp\Desktop\CSC303\Images\BooksHPBoxset.jpg")
        driver.find_element_by_name("caption").clear()
        driver.find_element_by_name("caption").send_keys("A Box of HP Books.")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        
        try: self.assertEqual("Current Images for test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        #try: self.assertEqual("Upload a new image", driver.find_element_by_css_selector("h3").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("Image uploaded!" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("A Box of HP Books.", driver.find_element_by_id("caption_16").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("caption_16").clear()
        driver.find_element_by_id("caption_16").send_keys("A Box of HP Adult Cover Books.")
        driver.find_element_by_link_text("Update Caption").click()

        
        try: self.assertEqual("Current Images for test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        #try: self.assertEqual("Upload a new image", driver.find_element_by_css_selector("h3").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Saved", driver.find_element_by_id("success_16").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("A Box of HP Adult Cover Books.", driver.find_element_by_id("caption_16").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("Delete").click()
        self.assertTrue("Are you sure you want to delete this image?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("div.modal-footer > button.btn").click()
        driver.find_element_by_link_text("Delete").click()
        self.assertTrue("Are you sure you want to delete this image?" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_link_text("Yes, delete").click()        
           
        driver.find_element_by_link_text("Go back").click()
        deleteitem(driver,self)
        
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
