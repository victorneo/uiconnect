from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class SearchValid(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
    
    def test_search_valid(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("LOGIN").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("boy")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("111")
        driver.find_element_by_id("submit-id-submit").click()
        driver.find_element_by_name("query").clear()
        driver.find_element_by_name("query").send_keys("shoe")
        driver.find_element_by_css_selector("button.btn").click()
        Select(driver.find_element_by_id("id_search_type")).select_by_visible_text("Collections only")
        driver.find_element_by_id("submit-id-submit").click()
        Select(driver.find_element_by_id("id_search_type")).select_by_visible_text("Items only")
        driver.find_element_by_id("submit-id-submit").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
