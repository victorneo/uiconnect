from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class CollectiondetailOthers(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_collectiondetail_others(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")        
        
        driver.find_element_by_link_text("Featured collections").click()
        try: self.assertEqual("Collections", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.collection-preview-image").click()
        
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 likes this collection.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 likes this collection.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_like").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 likes this collection.", driver.find_element_by_css_selector("div.social > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("0 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 followers", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_css_selector("img[alt=\"Harry Potter and the Philosophers Stone\"]").click()        
        try: self.assertEqual("Harry Potter and the Philosophers Stone", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Harry Potter Book Series").click()
        
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        driver.find_element_by_name("content").clear()
        driver.find_element_by_name("content").send_keys("testing non-owner comments...")
        driver.find_element_by_css_selector("input.btn").click()
        try: self.assertEqual("Harry Potter Book Series", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("testing non-owner comments..." in driver.find_element_by_tag_name("body").text)   
        self.assertTrue("Mabel commented 0 minutes ago." in driver.find_element_by_tag_name("body").text)
        
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
