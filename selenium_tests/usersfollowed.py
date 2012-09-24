from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_(self):
        driver = self.driver
        login(driver, self, "zgal", "asd")
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("Featured", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        driver.find_element_by_css_selector("#booksCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("Harry Potter and The Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("Harry Potter and The Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("Featured", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("Dashboard").click()
        try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Users followed").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Unfollow')])[2]").click()
        self.assertTrue("asd" not in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_link_text("Unfollow").click()
        try: self.assertEqual("You are currently not following any users.", driver.find_element_by_css_selector("p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("Featured", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        driver.find_element_by_css_selector("#booksCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("Harry Potter and The Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("Featured", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 followers.", driver.find_element_by_css_selector("div.follow > p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
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
