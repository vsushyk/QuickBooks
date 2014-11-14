__author__ = 'volodymyr'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from qbo_automation.methods import clear, send_keys, click, create_payment, create_location, create_account, create_item
import time


class QBOCompany():
    def __init__(self, company_id):
        QBOCompany.sign_up(self, company_id)
        QBOCompany.company_address(self)
        QBOCompany.company_industry(self, company_id)
        QBOCompany.create_location(self, company_id)
        QBOCompany.create_payments(self)
        QBOCompany.create_accounts(self)
        QBOCompany.create_items(self)
        QBOCompany.create_sales_tax(self)
        QBOCompany.set_settings(self)
        print("Congratulations! Your QBO company was created and set up for detailed integration.")
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
            "Restaurant, Caterer, or Bar")
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
        print("QBO account successfully created. Your login is vlad.adds" + str(
            qbo_company_number) + "@gmail.com. And password is revelup1")

    def create_location(self, qbo_company_number):
        create_location(self, qbo_company_number)

    def create_payments(self):
        driver = self.driver
        driver.refresh()
        driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
        driver.find_element_by_link_text("All Lists").click()
        driver.find_element_by_link_text("Payment Methods").click()
        list_of_payments = ["Visa", "MC", "American Express", "Discover", "Debit Card", "Gift Card", "Other", "Payout"]
        for payment in list_of_payments:
            if list_of_payments.index(payment) <= 3:
                create_payment(self, "credit", payment)
            else:
                create_payment(self, "non_credit", payment)

    def create_accounts(self):
        driver = self.driver
        driver.refresh()
        driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "All Lists")))
        driver.find_element_by_link_text("All Lists").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Chart of Accounts")))
        driver.find_element_by_link_text("Chart of Accounts").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//tr/td/span[text()='Sales']")))

        create_account(self, "Other Current Assets", "Assets Account")
        create_account(self, "Other Current Liabilities", "Liabilities Account")
        create_account(self, "Accounts payable (A/P)", "Accounts Payable")

    def create_items(self):
        driver = self.driver
        driver.refresh()
        driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
        # element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "All Lists")))
        # driver.find_element_by_link_text("All Lists").click()
        driver.find_element_by_xpath("//a[text()='Products and Services']").click()

        create_item(self, "Short", "Sales")
        create_item(self, "Employee Service", "Sales")
        create_item(self, "Rounding Delta", "Sales")
        create_item(self, "Surcharge", "Sales")
        create_item(self, "Service Charge", "Sales")
        create_item(self, "Item Discount", "Discounts")
        create_item(self, "Order Discount", "Discounts")
        create_item(self, "Coupon Discount", "Discounts")
        create_item(self, "Discount Refund", "Discounts")

    def create_sales_tax(self):
        driver = self.driver
        driver.get("https://qbo.intuit.com/app/salestax")
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Set Up Sales Tax Rates']")))
        click(self, "xpath", "//span[text()='Set Up Sales Tax Rates']")
        clear(self, "xpath", "(//div[@class='taxNameCol'])[1]")
        send_keys(self, "xpath", "(//div[@class='taxNameCol'])[1]", "Sales Tax")
        clear(self, "xpath", "(//div[@class='taxAgencyCol']/div/div[3]/input)[1]")
        send_keys(self, "xpath", "(//div[@class='taxAgencyCol']/div/div[3]/input)[1]", "IRS")
        clear(self, "xpath", "(//div[@class='taxRateCol']/div/div[2]/input)[1]")
        send_keys(self, "xpath", "(//div[@class='taxRateCol']/div/div[2]/input)[1]", "10")
        click(self, "xpath", "//span[text()='Save']")
        time.sleep(5)

    def set_settings(self):
        driver = self.driver
        driver.refresh()
        driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Company Settings")))
        driver.find_element_by_link_text("Company Settings").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Sales")))
        driver.find_element_by_link_text("Sales").click()
        driver.find_element_by_xpath("//div[text()='Products and services']").click()
        driver.find_element_by_xpath("//input[@data-qbo-bind='checked: trackQuantityOnHand, visible:!readSalesItems']").click()
        driver.find_element_by_xpath("(//div[@class='tableCell settingContent']/button[text()='Save'])[9]").click()
        driver.find_element_by_xpath("//button[text()='OK']").click()
        print("Inventory is turned on")
        driver.refresh()
        driver.find_element_by_link_text("Expenses").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-qbo-bind='visible:supportPurchaseOrder']/div[text()='Purchase orders']")))
        driver.find_element_by_xpath("//div[@data-qbo-bind='visible:supportPurchaseOrder']/div[text()='Purchase orders']").click()
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@data-qbo-bind='checked: hasPurchaseOrder, visible:!readPurchaseOrder']")))
        driver.find_element_by_xpath("//input[@data-qbo-bind='checked: hasPurchaseOrder, visible:!readPurchaseOrder']").click()
        driver.find_element_by_xpath("(//div[@class='tableCell settingContent tracking settingSpacer']/button[text()='Save'])[2]").click()
        driver.find_element_by_xpath("//button[text()='OK']").click()
        print("Purchase Orders are turned on")

if __name__ == "__main__":
    QBOCompany(29)
