from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class PagelinkingAllcategories(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
    
    def test_pagelinking_allcategories(self):
        driver = self.driver
        driver.get(self.base_url)

        try: self.assertEqual("All Categories", driver.find_element_by_link_text("All Categories").text)
        except AssertionError as e: self.verificationErrors.append(str(e))                
        verifyallcategories(driver,self)

        #fashion
        driver.find_element_by_link_text("see all items under Fashion").click()
        try: self.assertEqual("All Items in Fashion sorted by popularity", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertTrue("6-inch Black Heel" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("div.thumbnail-wrapper > img").click()
        try: self.assertEqual("6-inch Black Heel", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))                
        
        verifyallcategories(driver,self)               
        #books
        driver.find_element_by_link_text("see all items under Books").click()                
        verifybooks(driver, self)
        driver.find_element_by_css_selector("div.thumbnail-wrapper > img").click()
        try: self.assertEqual("Harry Potter and the Philosophers Stone", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)                
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[2]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Chamber of Secrets", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)               
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[3]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Prisoner of Azkaban", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)         
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[4]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Goblet of Fire", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)                 
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[5]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Order of the Phoenix", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)        
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[6]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Half-Blood Prince", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)         
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[7]/div/a/div/img").click()
        try: self.assertEqual("Harry Potter and the Deathly Hallows", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Books").click()
        
        verifybooks(driver, self)        
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[8]/div/a/div/img").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))        
               
        verifyallcategories(driver, self)
        #kids
        driver.find_element_by_link_text("see all items under Kids").click()
        verifykids(driver, self)
        driver.find_element_by_css_selector("div.thumbnail-wrapper > img").click()
        try: self.assertEqual("Rubik Cube", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Kids").click()
        
        verifykids(driver, self)        
        driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/ul/li[2]/div/a/div/img").click()
        try: self.assertEqual("Elmo's ABC Book", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
       
        verifyallcategories(driver, self)
        #electronic & IT Gadget
        driver.find_element_by_link_text("see all items under Electronic & IT Gadget").click()
        try: self.assertEqual("All Items in Electronic & IT Gadget sorted by popularity", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e)) 
        self.assertTrue("Samsung Galaxy Camera" in driver.find_element_by_tag_name("body").text)
        driver.find_element_by_css_selector("div.thumbnail-wrapper > img").click()
        try: self.assertEqual("Samsung Galaxy Camera", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))      
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
def verifyallcategories(driver, self):
    driver.find_element_by_link_text("All Categories").click()
    try: self.assertEqual("All Categories sorted by popularity", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))        
    try: self.assertEqual("Top items under Fashion (see all items under Fashion)", driver.find_element_by_css_selector("h4").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Top items under Books (see all items under Books)", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/h4[2]").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Top items under Kids (see all items under Kids)", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/h4[3]").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Top items under Electronic & IT Gadget (see all items under Electronic & IT Gadget)", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/h4[4]").text)
    except AssertionError as e: self.verificationErrors.append(str(e)) 

def verifybooks(driver, self):
    try: self.assertEqual("All Items in Books sorted by popularity", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e)) 
    self.assertTrue("Harry Potter and the Philosophers Stone" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Chamber of Secrets" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Prisoner of Azkaban" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Goblet of Fire" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Order of the Phoenix" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Half-Blood Prince" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Harry Potter and the Deathly Hallows" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)

def verifykids(driver, self):
    try: self.assertEqual("All Items in Kids sorted by popularity", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e)) 
    self.assertTrue("Rubik Cube" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("Elmo's ABC Book" in driver.find_element_by_tag_name("body").text)
    
if __name__ == "__main__":
    unittest.main()
