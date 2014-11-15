__author__ = 'volodymyr'

import sys
sys.path.append('..')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from qbo_automation.methods import clear, send_keys
import time


class QBOCompany():
    def __init__(self, company_id):
        QBOCompany.sign_up(self, company_id)
        QBOCompany.company_address(self)
        QBOCompany.company_industry(self, company_id)
        pass

    def sign_up(self, company_id):
        self.driver = webdriver.Firefox()
        self.base_url = "https://quickbooks.intuit.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url + "/start/core_sui?bc=USP-TDN/")
        clear(self, "id", "userFirstName")
        send_keys(self, "id", "userFirstName", "QBO")
        driver.find_element_by_id("userLastName").clear()
        driver.find_element_by_id("userLastName").send_keys("Company" + str(company_id))
        driver.find_element_by_id("userEmail").clear()
        driver.find_element_by_id("userEmail").send_keys("qbo.company" + str(company_id) + "@gmail.com")
        driver.find_element_by_id("confirmUserEmail").clear()
        driver.find_element_by_id("confirmUserEmail").send_keys("qbo.company" + str(company_id) + "@gmail.com")
        driver.find_element_by_id("userPassword").clear()
        driver.find_element_by_id("userPassword").send_keys("revelup1")
        driver.find_element_by_id("confirmUserPassword").clear()
        driver.find_element_by_id("confirmUserPassword").send_keys("revelup1")
        driver.find_element_by_id("newUserSubmitButton").click()
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, "Continue to Trial")))
        driver.find_element_by_link_text("Continue to Trial").click()
        element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='column tableCell']/div[2]/div/input")))

    def company_address(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@class='column tableCell']/div[2]/div/input").clear()
        driver.find_element_by_xpath("//div[@class='column tableCell']/div[2]/div/input").send_keys("123 Street St")
        driver.find_element_by_xpath("//div[@class='column tableCell']/div[3]/div/input").clear()
        driver.find_element_by_xpath("//div[@class='column tableCell']/div[3]/div/input").send_keys("San Francisco")
        driver.find_element_by_xpath("//div[@class='column tableCell']/div[4]/div/div/div[1]").click()
        driver.find_element_by_xpath("//td[text()='CA']").click()
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: postalCode']").clear()
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: postalCode']").send_keys("94133")
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: phoneNumber']").clear()
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: phoneNumber']").send_keys("(415)888-7777")
        driver.find_element_by_xpath("//button[@class='primary']").click()

    def company_industry(self, qbo_company_number):
        driver = self.driver
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-qbo-bind='value: industryName']")))
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: industryName']").clear()
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: industryName']").send_keys(
            "Retail Trade")
        driver.find_element_by_xpath("//input[@data-qbo-bind='value: industryName']").send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//form[@id='dijit_form_Form_1']/div[3]/div[1]/div[1]").click()
        driver.find_element_by_xpath('//td[text()="Products and services"]').click()
        driver.find_element_by_xpath("//form[@id='dijit_form_Form_1']/div[4]/div[1]/div[1]").click()
        driver.find_element_by_xpath('//td[text()="Sole proprietor"]').click()
        driver.find_element_by_xpath("//ul/li[1]/input[1]").click()
        driver.find_element_by_xpath("//ul/li[2]/input[1]").click()
        driver.find_element_by_xpath("//button[@class='primary']").click()
        wait = WebDriverWait(driver, 100)
        element = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='primary']")))
        driver.find_element_by_xpath("//button[@class='primary']").click()
        print("QBO account successfully created. Your login is qbo.company" + str(
            qbo_company_number) + "@gmail.com. And password is revelup1")
        time.sleep(20)


if __name__ == "__main__":
    QBOCompany()
