from selenium.webdriver.support.ui import Select
import os

def login(driver, self, username, pwd):
    driver.get(self.base_url)
    driver.find_element_by_link_text("LOGIN").click()   
    
    verifylogin(driver, self)
    driver.find_element_by_id("id_username").clear()
    driver.find_element_by_id("id_username").send_keys(username)
    driver.find_element_by_id("id_password").clear()
    driver.find_element_by_id("id_password").send_keys(pwd)
    driver.find_element_by_id("submit-id-submit").click()
    
    try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    
def verifylogin(driver, self):
    try: self.assertEqual("Login", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("", driver.find_element_by_id("user-avatar").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Forgot your password?" in driver.find_element_by_tag_name("body").text)    
    try: self.assertEqual("Alternative logins", driver.find_element_by_css_selector("h6").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("", driver.find_element_by_css_selector("a > img").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("", driver.find_element_by_id("persona-signin").text)
    except AssertionError as e: self.verificationErrors.append(str(e))    
    
def additem(driver, self):
    driver.find_element_by_link_text("Add Item").click()
    try: self.assertEqual("Add Item", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    driver.find_element_by_id("id_name").clear()
    driver.find_element_by_id("id_name").send_keys("test")
    driver.find_element_by_id("id_description").clear()
    driver.find_element_by_id("id_description").send_keys("testing 123")
    driver.find_element_by_id("id_price").clear()
    driver.find_element_by_id("id_price").send_keys("1")
    select = Select(driver.find_element_by_id("id_categories"))        
    select.select_by_visible_text("Fashion")
    select.select_by_visible_text("Electronic & IT Gadget")
    driver.find_element_by_id("submit-id-submit").click()
    
    try: self.assertEqual("Images for test", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Upload a new image", driver.find_element_by_xpath("//div[@id='container-wrapper']/div/div/div[2]/div/h3[2]").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Your item has been created. Upload some images!" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("No images yet!" in driver.find_element_by_tag_name("body").text)
    driver.find_element_by_link_text("Go back").click()
    try: self.assertEqual("test", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))  

def deleteitem(driver, self):
    driver.find_element_by_link_text("Delete Item").click()
    self.assertTrue("Are you sure you want to delete this item?" in driver.find_element_by_tag_name("body").text)
    driver.find_element_by_link_text("Yes, delete").click() 
    try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Item has been deleted." in driver.find_element_by_tag_name("body").text)

def addcollection(driver,self):
    additem(driver,self)
    driver.find_element_by_link_text("DASHBOARD").click()
    driver.find_element_by_link_text("Add Collection").click()
    try: self.assertEqual("Add Collection", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    driver.find_element_by_id("id_name").clear()
    driver.find_element_by_id("id_name").send_keys("testcollection")
    driver.find_element_by_id("id_description").clear()
    driver.find_element_by_id("id_description").send_keys("testing collection 123")
    driver.find_element_by_id("id_image").send_keys(os.path.abspath("C:\Users\hp\Desktop\CSC303\Images\world_different_colour.jpg"))
    driver.find_element_by_id("submit-id-submit").click()

    try: self.assertEqual("Add Items to Collection", driver.find_element_by_css_selector("h3").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Collection added. Add your items to it!" in driver.find_element_by_tag_name("body").text)
    select = Select(driver.find_element_by_id("id_listings"))        
    select.select_by_visible_text("test")       
    driver.find_element_by_id("submit-id-submit").click()
    
    try: self.assertEqual("testcollection", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Changes saved!" in driver.find_element_by_tag_name("body").text)
    self.assertTrue("test" in driver.find_element_by_tag_name("body").text)
    
def deletecollection(driver,self):
    driver.find_element_by_link_text("Delete Collection").click()
    self.assertTrue("Are you sure you want to delete this collection?" in driver.find_element_by_tag_name("body").text)
    driver.find_element_by_link_text("Yes, delete").click() 
    try: self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
    except AssertionError as e: self.verificationErrors.append(str(e))
    self.assertTrue("Collection has been deleted." in driver.find_element_by_tag_name("body").text)
    driver.find_element_by_link_text("My items and collections").click()
    driver.find_element_by_link_text("test").click() 
    deleteitem(driver,self)


   
    