__author__ = 'volodymyr'

import sys
sys.path.append('..')
from qbo_automation.methods import clear, send_keys, click, create_payment, create_location, create_account, create_item
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class QBO_Company_detailed_setup():
    def __init__(self, company_id):
        QBO_Company_detailed_setup.log_in(self, company_id)
        QBO_Company_detailed_setup.create_location(self, company_id)
        QBO_Company_detailed_setup.create_payments(self)
        QBO_Company_detailed_setup.create_accounts(self)
        QBO_Company_detailed_setup.create_items(self)
        # QBO_Company_detailed_setup.create_sales_tax(self) # selenium cannot find button by xpath locator. Need to be fixed before uncommenting
        QBO_Company_detailed_setup.set_settings(self)

    def log_in(self, qbo_company_number):
        self.driver = webdriver.Firefox()
        self.base_url = "https://qbo.intuit.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.get(self.base_url + "/app/homepage")
        self.driver.find_element_by_id("login").send_keys("qbo.company" + str(qbo_company_number) + "@gmail.com")
        self.driver.find_element_by_id("password").send_keys("revelup1")
        self.driver.find_element_by_id("LoginButton").click()

    def create_location(self, qbo_company_number):
        create_location(self, qbo_company_number)

    def create_payments(self):
        driver = self.driver
        driver.refresh()
        driver.find_element_by_xpath("(//button[@class='global-header-item-button']/span[@class='label'])[4]").click()
        driver.find_element_by_link_text("All Lists").click()
        driver.find_element_by_link_text("Payment Methods").click()
        list_of_payments = ["Visa", "MC", "Amex", "Discover", "Debit Card", "Gift Card", "Other", "PayPal"]
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
        driver.refresh()

        create_account(self, "Other Current Assets", "Assets Account")
        create_account(self, "Other Current Liabilities", "Liabilities Account")
        create_account(self, "Accounts payable (A/P)", "Accounts Payable")

    def create_items(self):
        driver = self.driver
        driver.get("https://qbo.intuit.com/app/items")
        driver.refresh()

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
        # wait = WebDriverWait(driver, 5)
        # element = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='setupActionBar']/span[2]/span/span/span[text()='Set Up Sales Tax Rates']")))
        element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='setupActionBar']/span[2]/span")))
        # driver.find_element_by_id("pageContent").send_keys(Keys.TAB)
        # driver.find_element_by_id("pageContent").send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//div[@class='setupActionBar']/span[2]/span").click()
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
        driver.find_element_by_xpath("//button[text()='Done']").click()
        print("Purchase Orders are turned on")


if __name__ == "__main__":
    QBO_Company_detailed_setup()