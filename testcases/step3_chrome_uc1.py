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
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains as AC
from threading import Thread

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get(
    "BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.environ.get(
    "BROWSERSTACK_ACCESS_KEY")
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"

capabilities = [
    {
        "os": "OS X",
        "osVersion": "Monterey",
        "buildName": "browserstack-build-PGA 3",
        "sessionName": "BStack parallel python PGA",
        "browserName": "safari",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "11",
        "buildName": "browserstack-build-PGA 3",
        "sessionName": "BStack parallel python PGA",
        "browserName": "firefox",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "buildName": "browserstack-build-PGA 3",
        "sessionName": "BStack parallel python PGA",
        "browserName": "chrome",
        "browserVersion": "latest"
    },
    {"os": "Windows",
        "osVersion": "10",
        "buildName": "browserstack-build-PGA 3",
        "sessionName": "BStack parallel python PGA",
        "browserName": "internet explorer",
        "browserVersion": "latest"
     }
]


def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
        "internet explorer": IEOptions()
    }
    return switcher.get(browser, ChromeOptions())


def run_session(cap):
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    if "deviceName" in cap:
        bstack_options['deviceName'] = cap["deviceName"]
    bstack_options["source"] = "python:sample-main:v1.1"
    if cap['browserName'] in ['ios']:
        cap['browserName'] = 'safari'
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    if cap['browserName'].lower() == 'samsung':
        options.set_capability('browserName', 'samsung')
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
    try:
        URL1 = "https://www.browserstack.com"
        driver.get(url=URL1)
        driver.maximize_window()

        def wait_click(xpath_location):
            WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()

        wait_click("//*[@title = 'Sign In']")

        def login_bstack():
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

        login_bstack()
        # wait_click("//*[@id='live_cross_product_explore']")
        wait_click("//*[@aria-label='Big Sur']")
        wait_click("//*[@aria-label='chrome 113 latest']")

        try:
            wait_click("//*[label[contains(text(),'Stop Session')]]")
            print("successfully logged into bstack live")
        except Exception as e:
            print("Error : {} ".format(e))
        driver.quit()
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err1:
        message = "Exception: " + str(err1.__class__) + str(err1)
    #     driver.execute_script(
    #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    # # Stop the driver
    driver.quit()


for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()