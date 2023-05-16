import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
print("All Modules are loaded")

URL = 'http://localhost:4444/wd/hub'
desired_caps = {'browserName': 'firefox'}
driver = webdriver.Remote(command_executor=URL,desired_capabilities=desired_caps)
print("opened driver")
URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()

URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()


def wait_click(xpath_location):
    WDW(driver, 50).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()


wait_click("//*[@title = 'Sign In']")

WDW(driver, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@title = 'Sign In']"))).click()
print("Quitting now")
driver.quit()