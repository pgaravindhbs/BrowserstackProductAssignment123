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

# def setup_browser_options():
#     options = selenium.webdriver.chrome.options.Options()
#     options.add_experimental_option("detach", True)
#     # options.add_argument(r"--user-data-dir=/Users/aravindhpg/python-selenium-browserstack/tests/C:/Users/aravindhpg/Library/Application Support/Google/Chrome/Profile 2")
#     # options.add_argument(r"--profile-directory=Profile 2")
#     options.add_argument(r"--desired_capabilities=DesiredCapabilities.CHROME")
#     return options
# Opening Chrome with my own local Chrome Profile to bypass 2FA. The alternate option is to utilise a dummy business email/password of Browserstack account
URL = 'http://localhost:4444/wd/hub'
driver = webdriver.Remote(command_executor=URL, desired_capabilities=DesiredCapabilities.CHROME)
URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()

def wait_click(xpath_location):
    WDW(driver,50).until(EC.visibility_of_element_located((By.XPATH,xpath_location))).click()

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
print("The title of the page is " + driver.title)
try:
    title = driver.title
    assert 'Dashboard' in title
    print('Assertion test passed - Live Dashboard has opened')
except Exception as e:
    print('Assertion test failed - Live dashboard did not open', format(e))
driver.get("https://live.browserstack.com/dashboard")
print("The title of the page now is " + driver.title)
try:
    title = driver.title
    assert 'Dashboard' in title
    print('Assertion test passed - Live Dashboard has opened')
except Exception as e:
    print('Assertion test failed - Live dashboard did not open', format(e))
wait_click("//*[div[contains(text(),'mac')]]")
wait_click("//*[@aria-label='Big Sur']")
wait_click("//*[@aria-label='chrome 113 latest']")

try:
    wait_click("//*[label[contains(text(),'Stop Session')]]")
    print("successfully logged into bstack live")
except Exception as e:
    print("Error : {} ".format(e))
driver.quit()
# //*[@id="lft-modal-upgrade"]

#
# options = selenium.webdriver.chrome.options.Options()
# options.add_experimental_option("detach", True)
# options.add_argument(r"--user-data-dir=/Users/aravindhpg/python-selenium-browserstack/tests/C:/Users/aravindhpg/Library/Application Support/Google/Chrome/Profile 2")
# options.add_argument(r"--profile-directory=Profile 2")
# options.add_argument(r"--command_executor='http://localhost:4444/wd/hub'")
# options.add_argument(r"--desired_capabilities=DesiredCapabilities.CHROME")
# driver = webdriver.Remote(options = options)


