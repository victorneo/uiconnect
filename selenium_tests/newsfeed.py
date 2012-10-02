from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from common import login, addcollection, deletecollection

class Newsfeed(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_newsfeed(self):
        driver = self.driver
        
        #verify user:zgal is not following anyone#
        login(driver, self, "zgal", "asd")        
        driver.find_element_by_link_text("Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" in driver.find_element_by_tag_name("body").text)        
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No one is currently following you :(" in driver.find_element_by_tag_name("body").text)
        
        #verify user:zgal has no newsfeed(not following anyone)#
        driver.find_element_by_link_text("Newsfeed").click()
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No items in your newsfeed. Follow users that you like to stay updated on their latest items for sale!" in driver.find_element_by_tag_name("body").text)
        
        #pick an item belong to user:asd an follow user:asd#
        driver.find_element_by_link_text("trends").click()
        try: self.assertEqual("featured items", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Kids").click()
        driver.find_element_by_css_selector("#kidsCarousel > div.carousel-inner > div.item.active > a > img.listing-image").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("btn_follow").click()
        try: self.assertEqual("1 follower", driver.find_element_by_id("span_followers").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        #verify user:zgal newsfeed is populated with user:asd update/feeds#
        driver.find_element_by_link_text("DASHBOARD").click()
        driver.find_element_by_link_text("Newsfeed").click()
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("asd added \"Elmo's ABC Book\" for sale." in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("asd added \"Rubik Cube\" for sale." in driver.find_element_by_tag_name("body").text)                    
        driver.find_element_by_link_text("LOGOUT").click()
        
        #simulate user:asd add an item and collection#
        login(driver, self, "asd", "asd")
        addcollection(driver, self)        
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:zgal receive user:asd latest update(new item)#
        login(driver, self, "zgal", "asd")
        driver.find_element_by_link_text("Newsfeed").click()
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("asd added the collection \"testcollection\"" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("asd added \"test\" for sale." in driver.find_element_by_tag_name("body").text)
        self.assertTrue("asd added \"Elmo's ABC Book\" for sale." in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("asd added \"Rubik Cube\" for sale." in driver.find_element_by_tag_name("body").text)        
        driver.find_element_by_link_text("LOGOUT").click()        
        
        #simulate user:asd delete an item#
        login(driver, self, "asd", "asd")
        driver.find_element_by_link_text("My items and collections").click()        
        driver.find_element_by_css_selector("div.collection-preview-image").click()
        deletecollection(driver, self)        
        driver.find_element_by_link_text("LOGOUT").click()
        
        #verify user:zgal receive user:asd latest udpate(delete item & collection)#
        login(driver, self, "zgal", "asd")
        driver.find_element_by_link_text("Newsfeed").click()
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
        self.assertTrue("asd added \"test\" for sale." not in driver.find_element_by_tag_name("body").text)
        self.assertTrue("asd added \"Elmo's ABC Book\" for sale." in driver.find_element_by_tag_name("body").text)        
        self.assertTrue("asd added \"Rubik Cube\" for sale." in driver.find_element_by_tag_name("body").text)
        
        #manage revert/clean up#
        driver.find_element_by_link_text("Followship").click()
        #driver.find_element_by_link_text("Manage Followship").click()
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." not in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" not in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("asd", driver.find_element_by_link_text("asd").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Unfollow").click()
        
        try: self.assertEqual("Users you are following", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("You are currently not following any users." in driver.find_element_by_tag_name("body").text)
        self.assertTrue("Following users let's you stay updated on the latest items for sale by them!" in driver.find_element_by_tag_name("body").text)
        self.assertTrue("asd" not in driver.find_element_by_tag_name("body").text)
        try: self.assertEqual("Users following you", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/h3[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
        driver.find_element_by_link_text("Newsfeed").click()
        try: self.assertEqual("Newsfeed", driver.find_element_by_css_selector("h3").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("No items in your newsfeed. Follow users that you like to stay updated on their latest items for sale!" in driver.find_element_by_tag_name("body").text)
        
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
