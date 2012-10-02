from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class PagelinkingHeader(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_header(self):
        driver = self.driver
        driver.get(self.base_url)
        try: self.assertEqual("trends", driver.find_element_by_link_text("trends").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("REGISTER", driver.find_element_by_link_text("REGISTER").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("REGISTER").click()
        try: self.assertEqual("Register", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("LOGIN", driver.find_element_by_link_text("LOGIN").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        login(driver, self, "zgal", "asd")
        
        try: self.assertEqual("MABEL", driver.find_element_by_link_text("MABEL").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("MABEL").click()
        try: self.assertEqual("Profile", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("DASHBOARD", driver.find_element_by_link_text("DASHBOARD").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("DASHBOARD").click()
        try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("SHOPPING CART", driver.find_element_by_link_text("SHOPPING CART").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("SHOPPING CART").click()
        try: self.assertEqual("Shopping Cart", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("trends", driver.find_element_by_link_text("trends").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("LOGOUT").click()
        
        try: self.assertEqual("LOGIN", driver.find_element_by_link_text("LOGIN").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("REGISTER", driver.find_element_by_link_text("REGISTER").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
