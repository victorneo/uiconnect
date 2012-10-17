from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Payment(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
    
    def test_payment(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("LOGIN").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("bartman")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("111")
        driver.find_element_by_id("submit-id-submit").click()
        driver.find_element_by_link_text("All Categories").click()
        driver.find_element_by_css_selector("img[alt=\"Correll\"]").click()
        driver.find_element_by_css_selector("input.btn.btn-large").click()
        driver.find_element_by_link_text("SHOPPING CART 1").click()
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("64 townville")
        driver.find_element_by_id("submit-id-submit").click()
        driver.find_element_by_name("submit").click()
        driver.find_element_by_id("login_password").click()
        driver.find_element_by_id("esignOpt").click()
        driver.find_element_by_id("agree").click()
        driver.find_element_by_id("continue").click()
        driver.find_element_by_link_text("click here").click()
        driver.find_element_by_link_text("View your payment records").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
