import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#<form id=loginmenu>

class PrinterLogicLoginTest(unittest.TestCase) :
    def setUp(self): #starts the browser, make sure PrinterLogic is in the title
        #chrome_options = Options()
        #chrome_options.add_argument("headless")
        #self.driver = webdriver.Chrome("./chromedriver.exe",options=chrome_options)
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver.get("https://jsaller.printercloud.com/admin")
        self.assertIn("PrinterLogic",self.driver.title)
    
    def getLoginFields(self): #grab the username and password fields, clear and return them
        userField = self.driver.find_element_by_id("relogin_user")
        userField.clear()
        pwdField = self.driver.find_element_by_id("relogin_password")
        pwdField.clear()
        return userField,pwdField

    def submit(self): #click the login button
        submitButton = self.driver.find_element_by_id("admin-login-btn")
        submitButton.click()

    def test_1_valid_login(self): #valid username, valid password COMPLETE
        userField,pwdField = self.getLoginFields()
        userField.send_keys("jsaller")
        pwdField.send_keys("12Parsecs")
        self.submit()
        WebDriverWait(self.driver,10).until(expected_conditions.presence_of_element_located((By.ID,"tabsetpage")))
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertGreater(len(mainpane.text),0)
        #"tabsetpage" does not exist on the page until the successful login
        #waits up to 10 seconds for tabsetpage to appear

    def test_2_bad_password(self): #valid username, invalid password COMPLETE
        userField,pwdField = self.getLoginFields()
        userField.send_keys("jsaller")
        pwdField.send_keys("password")
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Verifying login information, please wait...")
        time.sleep(2)
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)

    def test_3_bad_username(self): #invalid username, valid password COMPLETE
        userField,pwdField = self.getLoginFields()
        userField.send_keys("admin")
        pwdField.send_keys("12Parsecs")
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Verifying login information, please wait...") 
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)

    def test_4_bad_username_and_password(self): #invalid username, invalid password
        userField,pwdField = self.getLoginFields()
        userField.send_keys("admin")
        pwdField.send_keys("password")
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Verifying login information, please wait...")
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)

    def test_5_empty_fields(self): #Username and password not entered
        self.getLoginFields()
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Please enter your username and password:")

    def test_6_empty_username(self): #username not entered
        userField,pwdField = self.getLoginFields()
        pwdField.send_keys("12Parsecs")
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Please enter your username and password:")

    def test_7_empty_password(self): #password not entered
        userField,pwdField = self.getLoginFields()
        userField.send_keys("jsaller")
        self.submit()
        mainpane = self.driver.find_element_by_id("mainpane")
        self.assertEqual(len(mainpane.text),0)
        loginText = self.driver.find_element_by_id("logintext")
        self.assertEqual(loginText.text,"Please enter your username and password:")
        


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()


#<input id="relogin_user" type="text" autocapitalize="off" autocorrect="off" onkeydown="return helper.handle_special_input(event,'relogin_password');">
#<div id="logintext" class="" style="font-weight: bold;"></div>
#<input id="relogin_password" type="password" autocapitalize="off" autocorrect="off" onkeydown="return helper.handle_special_input(event,'relogin');">