# UAT TESTING ONLY

# The main goal of this program is to expire current periods provided by a URL in a CSV file according to an input month,
# then going to the Core termset and creating a new period which begins the month after the current one has been expired.
# The expiration date of the new period is also an input. The program then creates a new period and assigns a comment in 
# Supply Chain. Once completed, the program will loop through any other URLs provided in the CSV referenced on the code.
# Once completed, the program shuts down and periods are created.

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
        WebDriverWait(driver, 10).until(EC.alert_is_present())
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
        CurrentPeriodExp = str('September 2022')
        FuturePeriodExp = str('December 2022')
        NewPeriodComment = str('Code Test')

        # changes expiration period according to entered text and saves
        ddelement = driver.find_element_by_xpath("//*[text()='" + CurrentPeriodExp + "']")
        action = ActionChains(driver)
        action.click(on_element=ddelement).perform()
        current_url = driver.current_url
        driver.find_element(By.ID, "ButtonSave").click()
        driver.find_element(By.ID, "ButtonSave").click()
        refresh_with_alert(driver)
        
        # opens corresponding core and creates next period
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='ManufacturerCoreTerm/Edit/']")))
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "a[href*='ManufacturerCoreTerm/Edit/']").click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='ButtonCreatePeriod']"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "NoExpiration"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By. XPATH, "//*[@class='k-widget k-dropdown shorterDropDown']"))).click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//div[@id='MfrCoreTermExpirationPeriodKey-list']//li[text()='" + FuturePeriodExp + "']").click()
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
