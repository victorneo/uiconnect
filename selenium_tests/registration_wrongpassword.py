from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Wrongpassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
    
    def test_wrongpassword(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("REGISTER").click()
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("andy")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("andyLau")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("andylau@yahoo.com.sg")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("aaa")
        driver.find_element_by_id("id_bio").clear()
        driver.find_element_by_id("id_bio").send_keys("andy lau is old")
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
