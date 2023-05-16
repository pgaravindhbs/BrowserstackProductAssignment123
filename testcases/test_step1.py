import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import selenium.webdriver.chrome.options
import selenium.webdriver.firefox.options
import selenium.webdriver.safari.options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC

username_text = os.environ.get("browserstacktempusername1")
password_text = os.environ.get("browserstacktemppassword1")

#Setting up Browsers basis Browser name and whether to load default profile or not. Loading default profile will bypass 2FA. If not this, then dummy business email/password is used to bypass 2FA
def setup_browser_driver(browser, defaultProfile):
    print("Now testing for the combination of", browser, "with default profile as", defaultProfile)
    if browser == "chrome":
        options = selenium.webdriver.chrome.options.Options()
        options.add_experimental_option("detach", True)

        if defaultProfile == "yes":
            options.add_argument(
                r"--user-data-dir=/Users/aravindhpg/python-selenium-browserstack/tests/C:/Users/aravindhpg/Library/Application Support/Google/Chrome/Profile 2")
            options.add_argument(r"--profile-directory=Profile 2")
            print("Loading Default profile of ", browser)
        driver = webdriver.Chrome(options=options)


    elif browser == "firefox":
        options = selenium.webdriver.firefox.options.Options()

        if defaultProfile == "yes":
            options.add_argument("-profile")
            options.add_argument("/Users/aravindhpg/Library/Application Support/Firefox/Profiles/gj9o1pz6.aravindhpg")
            print("Loading Default profile of ", browser)

        driver = webdriver.Firefox(options=options)


    elif browser == "safari":
        options = selenium.webdriver.safari.options.Options()
        driver = webdriver.Safari(options=options)
        print("Safari has no option to set default browser profile and hence we will try logging in via dummy business email ID")

    else:
        options = selenium.webdriver.chrome.options.Options()
        driver = webdriver.Chrome(options=options)
        print("We are initiating chrome as the default browser if no input is provided correctly")

    print("This", browser, "has been initiated with default profile as", defaultProfile)
    return driver

def open_link(driver, URL):
    driver.get(url=URL)

def window_maximize (driver):
    driver.maximize_window()

#This method is Selenium Webdriver method (WDW - WebdriverWait) until visibility of element is located. Post visibility it clicks
def wait_click(driver, xpath_location):
    WDW(driver, 50).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()

#This method is Selenium Webdriver method (WDW - WebdriverWait) until visibility of element is located. Used for checking if the page elements loaded correctly
def wait_until_visible(driver, xpath_location):
    WDW(driver, 50).until(EC.visibility_of_element_located((By.XPATH, xpath_location)))

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
    # username_text = os.environ.get("browserstacktempusername1")
    actions.move_to_element(username_location).click().send_keys(username_text).perform()
    password_location = driver.find_element(By.XPATH, "//*[@id='user_password']")
    password_location.clear()
    # password_text = os.environ.get("browserstacktemppassword1")
    actions.move_to_element(password_location).click().send_keys(password_text).perform()
    driver.find_element(By.XPATH, "//*[@value='Sign me in']").click()
    print("logged in")

def step1(browser, defaultProfile):
    print("# Test case -", browser,"-",defaultProfile)
    #below command sets up the browser and defaultProfile
    driver = setup_browser_driver(browser, defaultProfile)
    URL = "https://browserstack.com"
    open_link(driver,URL)
    #sometimes the elements are not visible in the default window size. Hence we are maximizing the window
    window_maximize(driver)
    wait_click(driver, "//*[@title = 'Sign In']")
    #if we are not loading the defaultProfile or for Safari browsers, we have to login with dummy creds. For defaultProfile in Chrome and Firefox, logging in via Browserstack google profile bypasses the 2FA
    if defaultProfile=="no" or browser=="safari":
        login_bstack(driver)
    #This checks if we have actualled logged into a profile. The account menu toggle appears when we login
    wait_until_visible(driver, "//*[@id='account-menu-toggle']")
    print("The title of the page after logging in is " + driver.title)
    #Different browsers, Default profile combinations lead to different pages post login. Certain combinations open Automate dashboard and certain open the live dashboard.
    try:
        title = driver.title
        assert 'Dashboard' in title
        print('Assertion test passed - Live Dashboard has opened')
    except Exception as e:
        print('Assertion test failed - Live dashboard did not open', format(e))
    #We are explicitly going to live dashboard to ensure we are in the right page for next set of functions
    URL = 'https://live.browserstack.com/dashboard'
    open_link(driver, URL)
    wait_until_visible(driver, "//*[@id='automate_cross_product_explore']")
    print("The title of the page now is " + driver.title)
    try:
        title = driver.title
        assert 'Dashboard' in title
        print('Assertion test passed - Live Dashboard has opened')
    except Exception as e:\
        print('Assertion test failed - Live dashboard did not open', format(e))
    #For all test cases, we are defaulting to Ventura Mac OS chrome instances in Live Dashboard
    wait_click(driver, "//*[div[contains(text(),'mac')]]")

    wait_click(driver, "//*[@aria-label='Ventura']")

    try:
        #The below blocks check if the browser is disabled. The browsers get disabled for trial accounts. We check if the modal-upgrade appears that mentions that the trial is over. We close our test case loop then and there
        if (driver.find_element(By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
                "class") == "browser-version-list__element browser-version-list__element--disabled" or driver.find_element(By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
                "class") == "browser-version-list__element browser-version-list__element--selected browser-version-list__element--disabled"):
            wait_click(driver, "//*[@aria-label='chrome 110 ']")
            if driver.find_elements(By.XPATH, "//*[@id='lft-modal-upgrade']"):
                print("Expired my trial limits for this browser and hence exiting the test case")
                print("----------------")
                driver.quit()
                return
        #For first time browsers or for browserstack official logins, we wait until the toolbar drag button is visible and then we stop session
        wait_click(driver, "//*[@aria-label='chrome 110 ']")
        wait_until_visible(driver, "//*[@aria-label='toolbar drag button']")
        if driver.find_elements(By.XPATH,"//*[label[contains(text(),'Stop Session')]]") or wait_until_visible(driver, "//*[label[contains(text(),'Stop Session')]]"):
            wait_click(driver, "//*[label[contains(text(),'Stop Session')]]")
            print("Successfully logged into Live Dashboard and exited")
            print("----------------")
            driver.quit()
            return
    except Exception as e:
        print("Could not find Stop Live session due to some reason or session did not initiate correctly")
        print("Error final : {} ".format(e))
        driver.quit()

#We initiate all combinations of browser and default profile
step1("chrome", "yes")
step1("chrome", "no")
step1("firefox", "yes")
step1("firefox", "no")
step1("safari", "yes")
step1("safari", "no")
