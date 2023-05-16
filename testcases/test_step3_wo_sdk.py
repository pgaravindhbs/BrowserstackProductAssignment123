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
        "buildName": "browserstack-build-PGA 4",
        "sessionName": "BStack parallel python PGA",
        "browserName": "safari",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "11",
        "buildName": "browserstack-build-PGA 4",
        "sessionName": "BStack parallel python PGA",
        "browserName": "firefox",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "buildName": "browserstack-build-PGA 4",
        "sessionName": "BStack parallel python PGA",
        "browserName": "chrome",
        "browserVersion": "latest"
    },
    {"os": "Windows",
        "osVersion": "10",
        "buildName": "browserstack-build-PGA 4",
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

def open_link(driver, URL):
    driver.get(url=URL)

def window_maximize (driver):
    driver.maximize_window()

#This method is Selenium Webdriver method (WDW - WebdriverWait) until visibility of element is located. Post visibility it clicks
def wait_click(driver, xpath_location):
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()

#This method is Selenium Webdriver method (WDW - WebdriverWait) until visibility of element is located. Used for checking if the page elements loaded correctly
def wait_until_visible(driver, xpath_location):
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, xpath_location)))

#not used in this py file
def wait_until_invisible(driver, xpath_location):
    WDW(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, xpath_location)))

#logs into browserstack via dummy business email ID. The business email ID and possword are defined as environmental variables
def login_bstack(driver):
    wait_until_visible(driver,"//*[@id='user_email_login']")
    # time.sleep(1)
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
    print("logged in")

def run_session(cap):
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"] + str(time.time()),
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        'debug': 'true',  # to enable visual logs
        'networkLogs': 'true',  # to enable network logs to be logged
        'consoleLogs': 'info'  # to enable console logs at the info level. You can also use other log levels here

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
        print("# Test case -", cap["osVersion"],"-", cap["browserName"])
        # below command sets up the browser and defaultProfile
        URL1 = "https://browserstack.com"
        open_link(driver, URL1)
        # sometimes the elements are not visible in the default window size. Hence we are maximizing the window
        window_maximize(driver)
        wait_click(driver, "//*[@title = 'Sign In']")
        # if we are not loading the defaultProfile or for Safari browsers, we have to login with dummy creds. For defaultProfile in Chrome and Firefox, logging in via Browserstack google profile bypasses the 2FA
        login_bstack(driver)
        # This checks if we have actualled logged into a profile. The account menu toggle appears when we login
        wait_until_visible(driver, "//*[@id='account-menu-toggle']")
        print("The title of the page after logging in is " + driver.title)
        # Different browsers, Default profile combinations lead to different pages post login. Certain combinations open Automate dashboard and certain open the live dashboard.
        try:
            title = driver.title
            assert 'Dashboard' in title
            print('Assertion test passed - Live Dashboard has opened')
        except Exception as e:
            print('Assertion test failed - Live dashboard did not open', format(e))
        # We are explicitly going to live dashboard to ensure we are in the right page for next set of functions
        URL1 = 'https://live.browserstack.com/dashboard'
        open_link(driver, URL1)
        wait_until_visible(driver, "//*[@id='automate_cross_product_explore']")
        print("The title of the page now is " + driver.title)
        try:
            title = driver.title
            assert 'Dashboard' in title
            print('Assertion test passed - Live Dashboard has opened')
        except Exception as e: \
            print('Assertion test failed - Live dashboard did not open', format(e))
        # For all test cases, we are defaulting to Ventura Mac OS chrome instances in Live Dashboard
        wait_click(driver, "//*[div[contains(text(),'mac')]]")

        wait_click(driver, "//*[@aria-label='Ventura']")

        try:
            # The below blocks check if the browser is disabled. The browsers get disabled for trial accounts. We check if the modal-upgrade appears that mentions that the trial is over. We close our test case loop then and there
            if (driver.find_element(By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
                "class") == "browser-version-list__element browser-version-list__element--disabled" or driver.find_element(
            By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
            "class") == "browser-version-list__element browser-version-list__element--selected browser-version-list__element--disabled"):
                wait_click(driver, "//*[@aria-label='chrome 110 ']")
                if driver.find_elements(By.XPATH, "//*[@id='lft-modal-upgrade']"):
                    print("Expired my trial limits for this browser and hence exiting the test case")
                    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Expired my trial limits for this browser and hence exiting the test case"}}')

                    print("----------------")
                    driver.quit()
                    return
            # For first time browsers or for browserstack official logins, we wait until the toolbar drag button is visible and then we stop session
            wait_click(driver, "//*[@aria-label='chrome 110 ']")
            wait_until_visible(driver, "//*[@aria-label='toolbar drag button']")
            if driver.find_elements(By.XPATH, "//*[label[contains(text(),'Stop Session')]]") or wait_until_visible(driver,
                                                                                                               "//*[label[contains(text(),'Stop Session')]]"):
                wait_click(driver, "//*[label[contains(text(),'Stop Session')]]")
                print("Successfully logged into Live Dashboard and exited")
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully logged in and logged out of Bstack"}}')

                print("----------------")
                driver.quit()
                return
        except Exception as e:
            print("Could not find Stop Live session due to some reason or session did not initiate correctly")
            print("Error final : {} ".format(e))
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