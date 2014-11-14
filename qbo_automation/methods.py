__author__ = 'volodymyr'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



    # self.driver.execute_script("window.promptResponse=prompt('Please enter QBO Company number.','QBO Company')")
    # a = self.driver.execute_script("var win = this.browserbot.getUserWindow(); return win.promptResponse")
    # return a


def log_in(self, qbo_company_number):
    self.driver = webdriver.Firefox()
    self.base_url = "https://qbo.intuit.com/"
    self.verificationErrors = []
    self.accept_next_alert = True
    self.driver.get(self.base_url + "/app/homepage")
    self.driver.find_element_by_id("login").send_keys("qbo.company" + str(qbo_company_number) + "@gmail.com")
    self.driver.find_element_by_id("password").send_keys("revelup1")
    self.driver.find_element_by_id("LoginButton").click()


def clear(self, loc_type, loc):
    driver = self.driver
    if loc_type == "id":
        driver.find_element_by_id(loc).clear()
    elif loc_type == "xpath":
        driver.find_element_by_xpath(loc).clear()
    elif loc_type == "link":
        driver.find_element_by_link_text(loc).clear()
    else:
        print "No such a method exist in WebDriver"


def send_keys(self, loc_type, loc, txt):
    driver = self.driver
    if loc_type == "id":
        driver.find_element_by_id(loc).send_keys(txt)
    elif loc_type == "xpath":
        driver.find_element_by_xpath(loc).send_keys(txt)
    elif loc_type == "link":
        driver.find_element_by_link_text(loc).send_keys(txt)
    else:
        print "No such a method exist in WebDriver"


def click(self, loc_type, loc):
    driver = self.driver
    if loc_type == "id":
        driver.find_element_by_id(loc).click()
    elif loc_type == "xpath":
        driver.find_element_by_xpath(loc).click()
    elif loc_type == "link":
        driver.find_element_by_link_text(loc).click()
    else:
        print "No such a method exist in WebDriver"


def create_location(self, loc_num):
    driver = self.driver
    time.sleep(5)
    driver.refresh()
    driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
    time.sleep(2)
    driver.find_element_by_link_text("All Lists").click()
    driver.find_element_by_link_text("Locations").click()
    driver.find_element_by_css_selector("button.button.primary").click()
    driver.find_element_by_xpath("//div[@class='row']/div[1]/input").click()
    driver.find_element_by_xpath("//div[@class='row']/div[1]/input").send_keys("Location" + str(loc_num))
    driver.find_element_by_xpath("//button[text()='Save']").click()


def create_payment(self, credit_or_not, payment_name):
    driver = self.driver
    # driver.refresh()  <--- IDK if it's needed. Sometime it broke in this moment.
    if credit_or_not == "credit":
        driver.find_element_by_css_selector("button.button.primary").click()
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").clear()
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").send_keys(payment_name + " Payment")
        driver.find_element_by_xpath("//input[@data-qbo-bind='checked:creditCard']").click()
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").send_keys(Keys.RETURN)
    elif credit_or_not == "non_credit":
        driver.find_element_by_css_selector("button.button.primary").click()
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").clear()
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").send_keys(payment_name + " Payment")
        driver.find_element_by_xpath("//div[@class='form']/div[@class='row']/div[1]/input[1]").send_keys(Keys.RETURN)


def create_account(self, acc_cat, acc_name):
    driver = self.driver
    driver.find_element_by_css_selector("button.button.primary").click()
    driver.find_element_by_xpath("//span[text()='Accounts receivable (A/R)']").click()
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='dijit_form_Select_0_dropdown']/table/tbody/tr/td[text()='" + acc_cat + "']")))
    driver.find_element_by_xpath("//div[@id='dijit_form_Select_0_dropdown']/table/tbody/tr/td[text()='" + acc_cat + "']").click()
    if acc_cat == "Accounts payable (A/P)":
        pass
    else:
        driver.find_element_by_xpath("//select/option[text()='" + acc_cat + "']").click()
    driver.find_element_by_xpath("//div[@class='tableCell main-column']/div[1]/div[1]/div[@class='row']/div[1]/input[1]").click()
    driver.find_element_by_xpath("//div[@class='tableCell main-column']/div[1]/div[1]/div[@class='row']/div[1]/input[1]").send_keys(acc_name)
    driver.find_element_by_xpath("//div[@class='tableCell main-column']/div[1]/div[1]/div[@class='row']/div[1]/input[1]").click()
    driver.find_element_by_xpath("//button[@data-qbo-id='save']").click()
    print(acc_name + " created")


def create_item(self, item_name, income_account):
    driver = self.driver
    driver.find_element_by_css_selector("button.button.primary").click()
    driver.find_element_by_xpath("//div[@class='tableCell nameCell']/div/input[@name='name']").click()
    driver.find_element_by_xpath("//div[@class='tableCell nameCell']/div/input[@name='name']").send_keys(item_name)
    driver.find_element_by_xpath("//div[@class='tableCell nameCell']/div/input[@name='name']").click()
    driver.find_element_by_xpath("//div[@class='row salesAccountIdPane']/div[1]/input[1]").clear()
    driver.find_element_by_xpath("//div[@class='row salesAccountIdPane']/div[1]/input[1]").send_keys(income_account)
    driver.find_element_by_xpath("//div[@class='row salesAccountIdPane']/div[1]/input[1]").send_keys(Keys.ENTER)
    driver.find_element_by_xpath("//button[@data-qbo-id='save']").click()
    print(item_name + "item is created")