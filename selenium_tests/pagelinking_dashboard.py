from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class PagelinkingDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_dashboard(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")
        
        try: self.assertEqual("Newsfeed", driver.find_element_by_link_text("Newsfeed").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Newsfeed").click()        
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Rewards (0 points)", driver.find_element_by_link_text("Rewards (0 points)").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Rewards (0 points)").click()
        try: self.assertEqual("Rewards", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Followship", driver.find_element_by_link_text("Followship").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Payments", driver.find_element_by_link_text("Payments").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Payments").click()
        try: self.assertEqual("Your Payments", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("My items and collections", driver.find_element_by_link_text("My items and collections").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("My items and collections").click()
        try: self.assertEqual("My items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("My Collections", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Add Item", driver.find_element_by_link_text("Add Item").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Add Item").click()
        try: self.assertEqual("Add Item", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        try: self.assertEqual("Add Collection", driver.find_element_by_link_text("Add Collection").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Add Collection").click()
        try: self.assertEqual("Add Collection", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
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
