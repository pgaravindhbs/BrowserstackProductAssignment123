from dotenv import load_dotenv
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains as AC
from threading import Thread

import os
BROWSERSTACK_USERNAME = os.environ.get(
    "browserstackpermanentusername")
BROWSERSTACK_ACCESS_KEY = os.environ.get(
    "browserstackpermanentaccesscode1")

URL = 'http://localhost:4444/wd/hub'
driver = webdriver.Remote(command_executor=URL,desired_capabilities=DesiredCapabilities.CHROME)
print("opened driver")

try:
    URL1 = "https://www.browserstack.com"
    driver.get(url=URL1)
    driver.maximize_window()

    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@title = 'Sign In']"))).click()
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='user_email_login']")))
    time.sleep(1)
    actions = AC(driver)
    username_location = driver.find_element(By.XPATH, "//*[@id='user_email_login']")
    username_location.clear()
    username_text = os.environ.get("browserstacktempusername1")
    actions.move_to_element(username_location).click().send_keys(username_text).perform()
    password_location = driver.find_element(By.XPATH, "//*[@id='user_password']")
    password_location.clear()
    password_text = os.environ.get("browserstacktemppassword1")
    actions.move_to_element(password_location).click().send_keys(password_text).perform()
    driver.find_element(By.XPATH, "//*[@value='Sign me in']").click()

    driver.get("https://live.browserstack.com/dashboard")
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[div[contains(text(),'mac')]]"))).click()
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Big Sur']"))).click()
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='chrome 112 ']"))).click()
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[label[contains(text(),'Stop Session')]]"))).click()
    print("successfully logged into bstack live")
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Yaay! my sample test passed"}}')

    driver.quit()
except Exception as e:
    print("Error : {} ".format(e))
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + '}}')
    driver.quit()
except NoSuchElementException as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    driver.quit()
# except Exception as err1:
#     message = "Exception: " + str(err1.__class__) + str(err1)
#     driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
#     driver.quit()
driver.quit()
