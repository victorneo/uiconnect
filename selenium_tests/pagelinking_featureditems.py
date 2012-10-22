from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class PagelinkingFeatureditems(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_featureditems(self):
        driver = self.driver
        driver.get(self.base_url)
        
        verifyfeatureditem(driver, self)
        driver.find_element_by_link_text("Fashion").click()
        driver.find_element_by_css_selector("img.listing-image").click()
        self.assertTrue("6-inch Black Heel" in driver.find_element_by_tag_name("body").text)   
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        verifyfeatureditem(driver, self)
        driver.find_element_by_link_text("Books").click()
        driver.find_element_by_css_selector("#booksCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Harry Potter and the Chamber of Secrets" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Harry Potter and the Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        verifyfeatureditem(driver, self)
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        verifyfeatureditem(driver, self)
        driver.find_element_by_link_text("Electronic & IT Gadget").click()
        driver.find_element_by_css_selector("#electronic-it-gadgetCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        self.assertTrue("Samsung Galaxy Camera" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Samsung Galaxy Camera", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

def verifyfeatureditem(driver, self):
    driver.find_element_by_link_text("trends").click()
    try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Fashion", driver.find_element_by_link_text("Fashion").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Books", driver.find_element_by_link_text("Books").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Kids", driver.find_element_by_link_text("Kids").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Electronic & IT Gadget", driver.find_element_by_link_text("Electronic & IT Gadget").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("the latest and the trendiest", driver.find_element_by_css_selector("h5").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Why join us?" in driver.find_element_by_tag_name("body").text)        
    try: self.assertEqual("Huge community", driver.find_element_by_css_selector("div.span4 > h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Redeem", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/div[3]/h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Comment and Share", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div/div[4]/h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
        
if __name__ == "__main__":
    unittest.main()
