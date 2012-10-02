from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, additem, deleteitem

class ItemdetailOwn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_itemdetail_own(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")       
        
        #insert a test item#
        additem(driver, self) 
        
        try: self.assertEqual("0 likes this item.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        try: self.assertEqual("1 likes this item.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        try: self.assertEqual("0 likes this item.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_name("content").clear()
        driver.find_element_by_name("content").send_keys("testing owner comments...")
        driver.find_element_by_css_selector("input.btn").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("testing owner comments..." in driver.find_element_by_tag_name("body").text)   
        self.assertTrue("(Owner) Mabel commented 0 minutes ago." in driver.find_element_by_tag_name("body").text)
        
        driver.find_element_by_link_text("Fashion").click()
        try: self.assertEqual("All Items in Fashion sorted by popularity", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("test" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[2]/div/a/h5").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("Manage Images").click()
        try: self.assertEqual("Images for test", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Go back").click()        
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
        
        driver.find_element_by_link_text("Edit Item").click()
        try: self.assertEqual("Update Item", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("My items and collections").click()
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/ul/li[3]/div/a/h5").click()
        try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))  
               
        deleteitem(driver,self)        
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
