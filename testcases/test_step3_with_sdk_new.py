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


#Setting up Browsers basis Browser name and whether to load default profile or not. Loading default profile will bypass 2FA. If not this, then dummy business email/password is used to bypass 2FA
browser = "firefox"
defaultProfile = "no"
print("Now testing for the combination of", browser, "with default profile as", defaultProfile)
URL = 'http://localhost:4444/wd/hub'
# if browser == "chrome":
# Using selenium.webdriver.chrome.options gave an error for IE Browserstack. hence using an older way of invoking browser. This appears to be a problem with SDK
options = selenium.webdriver.IeOptions()
options.add_argument(r"--desired_capabilities=DesiredCapabilities.IE")

driver = webdriver.Remote(command_executor=URL, options=options)
print("This", browser, "has been initiated with default profile as", defaultProfile)

print("# Test case -", browser,"-",defaultProfile)
#below command sets up the browser and defaultProfile

URL = "https://browserstack.com"
driver.get(url=URL)
#sometimes the elements are not visible in the default window size. Hence we are maximizing the window
driver.maximize_window()
WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@title = 'Sign In']"))).click()
#if we are not loading the defaultProfile or for Safari browsers, we have to login with dummy creds. For defaultProfile in Chrome and Firefox, logging in via Browserstack google profile bypasses the 2FA
WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@id='user_email_login']")))
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

#This checks if we have actualled logged into a profile. The account menu toggle appears when we login
WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-menu-toggle']")))
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
driver.get(url=URL)
WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@id='automate_cross_product_explore']")))
print("The title of the page now is " + driver.title)
try:
    title = driver.title
    assert 'Dashboard' in title
    print('Assertion test passed - Live Dashboard has opened')
except Exception as e: \
     print('Assertion test failed - Live dashboard did not open', format(e))
#For all test cases, we are defaulting to Ventura Mac OS chrome instances in Live Dashboard
WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[div[contains(text(),'mac')]]"))).click()

WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@aria-label='Ventura']"))).click()

try:
    #The below blocks check if the browser is disabled. The browsers get disabled for trial accounts. We check if the modal-upgrade appears that mentions that the trial is over. We close our test case loop then and there
    if (driver.find_element(By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
                "class") == "browser-version-list__element browser-version-list__element--disabled" or driver.find_element(By.XPATH, "//*[@aria-label='chrome 110 ']").get_attribute(
            "class") == "browser-version-list__element browser-version-list__element--selected browser-version-list__element--disabled"):
        WDW(driver, 30).until(EC.visibility_of_element_located((By.XPATH,"//*[@aria-label='chrome 110 ']"))).click()
        if driver.find_elements(By.XPATH, "//*[@id='lft-modal-upgrade']"):
            print("Expired my trial limits for this browser and hence exiting the test case")
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Expired my trial limits for this browser and hence exiting the test case"}}')
            print("----------------")
            driver.quit()
            exit()

    #For first time browsers or for browserstack official logins, we wait until the toolbar drag button is visible and then we stop session
    WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@aria-label='chrome 110 ']"))).click()
    WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[@aria-label='toolbar drag button']")))
    if driver.find_elements(By.XPATH,"//*[label[contains(text(),'Stop Session')]]") or WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH,"//*[label[contains(text(),'Stop Session')]]"))):
        WDW(driver,30).until(EC.visibility_of_element_located((By.XPATH, "//*[label[contains(text(),'Stop Session')]]"))).click()
        print("Successfully logged into Live Dashboard and exited")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully logged in and out of Bstack"}}')
        print("----------------")
        driver.quit()

except Exception as e:
    print("Could not find Stop Live session due to some reason or session did not initiate correctly")
    print("Error final : {} ".format(e))
    driver.quit()


