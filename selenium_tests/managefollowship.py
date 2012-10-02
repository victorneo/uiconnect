from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login

class Managefollowship(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_managefollowship(self):
        driver = self.driver
        
        #verify user:zgal has nobody following#
        login(driver, self, "zgal", "asd")             
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No one is currently following you :(" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:ace is not following anyone#
        login(driver, self, "ace", "asd")
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        #pick an item belong to user:zgal and follow user:zgal#
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Fashion").click()
        driver.find_element_by_css_selector("#fashionCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:ace is under user:zgal 'users following you'#
        login(driver, self, "zgal", "asd")        
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No one is currently following you :(" not in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Portgas D. Ace", driver.find_element_by_link_text("Portgas D. Ace").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:zgal is under user:ace 'users you are following'#        
        login(driver, self, "ace", "asd")        
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." not in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" not in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Mabel", driver.find_element_by_link_text("Mabel").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        #user:ace unfollow user:zgal# 
        driver.find_element_by_link_text("Unfollow").click()        
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Mabel" not in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        #verify user:zgal counter decrement by 1#
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Fashion").click()
        driver.find_element_by_css_selector("#fashionCarousel > div.carousel-inner > div.item.active > a > img").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:ace is remove from user:zgal 'users following you'#
        login(driver, self, "zgal", "asd")        
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No one is currently following you :(" in driver.find_element_by_tag_name("body").text)
        
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
