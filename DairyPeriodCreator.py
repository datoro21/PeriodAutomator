# UAT TESTING ONLY

# The main goal of this program is to go into Dairy Cores indicated by URL on 'Dairy URL Cores.csv'
# Once in the core, the program instantly clicks 'Create Period'. For USA dairy, there is no need to expire
# the last period because periods are built month to month so the only process needed is to go into the Core,
# create new periods, enter comment, drop new period on CSV, and move on to the next.

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

path_to_csv = ("C:\\Users\\ToroCD01\\Desktop\\Python\\Dairy URL Cores.csv")
driver.implicitly_wait(30)

with open(path_to_csv, 'r') as mycsv:
    reader = csv.reader(mycsv)
    for row in reader:
        urlstring = row[0]
        driver.get(urlstring)

        # VARIABLES
        FuturePeriodExp = str('August 2021')
        NewPeriodComment = str('Code Test')
        
        # opens core and creates next period
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='ButtonCreatePeriod']"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "NoExpiration"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By. XPATH, "//*[@class='k-widget k-dropdown v-width']"))).click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//div[@id='DistCoreTermExpirationPeriodKey-list']//li[text()='" + FuturePeriodExp + "']").click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By. XPATH, "//*[@class='k-widget k-dropdown WiderDropDown']"))).send_keys(Keys.DOWN)
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ButtonCreatePeriodSave"))).click()
        time.sleep(0.5)
        driver.refresh()
        WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, "AddCommentButton"))).click()
        time.sleep(0.5)
        driver.find_element(By.ID, "commentText").click()
        action2 = ActionChains(driver)
        action2.send_keys(NewPeriodComment)
        action2.perform()
        time.sleep(0.5)
        driver.find_element(By.ID, "CommentSaveButton").click()
        time.sleep(0.5)

        MCP = driver.find_element_by_xpath("//*[@id='TransactionPeriodGrid']/div[3]/table/tbody/tr[1]/td[1]/a")

        with open("New Periods.csv","a+", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([MCP.text])
