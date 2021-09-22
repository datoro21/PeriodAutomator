from os import X_OK
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

# defines Chrome location and chromedriver for Selenium. maximizes window
Chrome = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="C:\\Users\\ToroCD01\\AppData\\Local\\Programs\\Python\\Python39\\chromedriver.exe")
driver.maximize_window()

# directs Chrome to SC website
driver.get("https://uat-supplychain.compass-usa.com/Registration/Login?ReturnUrl=%2FCanada")

# clicks on "Supply Chain" button
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='ic-button-text v-button-text']"))).click()

# enters credentials to login to SC
#region
UserName = driver.find_element_by_name('UserName')
UserName.send_keys("username")
Password = driver.find_element_by_name('Password')
Password.send_keys("password")
driver.find_element_by_css_selector('[class="submit"]').click()
#endregion

path_to_csv = ("C:\\Users\\ToroCD01\\Desktop\\Python\\Period URLs.csv")
driver.implicitly_wait(30)

def refresh_with_alert(driver):
    try: 
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except TimeoutException:
        print("OK - No reload alert from Chrome.")

with open(path_to_csv, 'r') as mycsv:
    reader = csv.reader(mycsv)
    for row in reader:
        urlstring = row[0]
        driver.get(urlstring)
        driver.find_element_by_css_selector('[class="k-widget k-dropdown ic-can-be-dirty"]').click()
        time.sleep(1)

        # VARIABLES
        ExtMonth = str('January 2022')

        # changes expiration period according to entered text and saves
        ddelement = driver.find_element_by_xpath("//*[text()='" + ExtMonth + "']")
        action = ActionChains(driver)
        action.click(on_element=ddelement).perform()
        current_url = driver.current_url
        driver.find_element(By.ID, "ButtonSave").click()
        driver.find_element(By.ID, "ButtonSave").click()
        refresh_with_alert(driver)
        
        # opens corresponding core and creates next period
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='ManufacturerCoreTerm/Edit/']")))
        time.sleep(1)
