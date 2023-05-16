import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    import selenium.webdriver.chrome.options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait as WDW
    from selenium.webdriver.support import expected_conditions as EC
    print("All Modules are loaded")
except Exception as e:
    print("Error : {} ".format(e))


def setup_browser_options():
    options = selenium.webdriver.chrome.options.Options()
    options.add_experimental_option("detach", True)
    options.add_argument(r"--user-data-dir=/Users/aravindhpg/python-selenium-browserstack/tests/C:/Users/aravindhpg/Library/Application Support/Google/Chrome/Profile 2")
    options.add_argument(r"--profile-directory=Profile 2")
    return options
# Opening Chrome with my own local Chrome Profile to bypass 2FA. The alternate option is to utilise a dummy business email/password of Browserstack account
driver = webdriver.Chrome(options=setup_browser_options())
URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()

def wait_click(xpath_location):
    WDW(driver,25).until(EC.visibility_of_element_located((By.XPATH,xpath_location))).click()

wait_click("//*[@title = 'Sign In']")
WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-menu-toggle']")))
print("The title of the page is " + driver.title)
try:
    title = driver.title
    assert 'Dashboard' in title
    print('Assertion test passed - Live Dashboard has opened')
except Exception as e:
    print('Assertion test failed - Live dashboard did not open', format(e))
driver.get("https://live.browserstack.com/dashboard")
WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='automate_cross_product_explore']")))
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
    WDW(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="lft-modal-upgrade"]')))
    print("Expired my trial limits for this browser")
except Exception as e:
    print("Errored out at modal check : {} ".format(e))
try:
    WDW(driver, 25).until(
        EC.visibility_of_element_located((By.XPATH, "//*[label[contains(text(),'Stop Session')]]"))).click()
    print("Successfully logged into Live Dashboard and exited")
    driver.quit()

except Exception as e:
    print("Could not find Stop session due to some reason")
    print("Error final : {} ".format(e))
try:
    WDW(driver, 25).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[label[contains(text(),'Stop Session')]]")))
    print("Could not login to Live as trial expired")

except Exception as e:
    print("Could not login to Live due to error or driver quitted")
    print("Error final : {} ".format(e))
driver.quit()

# try:
#     wait_until_invisible(driver, "//*[label[contains(text(),'Stop Session')]]")
#     print("Could not login to Live as trial expired")
# except Exception as e:
#     print("Could not login to Live due to error or driver quitted")
#     print("Error final : {} ".format(e))

# print("The title of the page is " + driver.title)
# try:
#     title = driver.title
#     assert 'Dashboard' in title
#     print('Assertion test passed - Live Dashboard has opened')
# except Exception as e:
#     print('Assertion test failed - Live dashboard did not open', format(e))
# driver.get("https://live.browserstack.com/dashboard")
# print("The title of the page now is " + driver.title)
# try:
#     title = driver.title
#     assert 'Dashboard' in title
#     print('Assertion test passed - Live Dashboard has opened')
# except Exception as e:
#     print('Assertion test failed - Live dashboard did not open', format(e))
# wait_click("//*[div[contains(text(),'mac')]]")
# wait_click("//*[@aria-label='Big Sur']")
# wait_click("//*[@aria-label='chrome 113 latest']")
#
# try:
#     wait_click("//*[label[contains(text(),'Stop Session')]]")
#     print("successfully logged into bstack live")
# except Exception as e:
#     print("Error : {} ".format(e))
# driver.quit()


