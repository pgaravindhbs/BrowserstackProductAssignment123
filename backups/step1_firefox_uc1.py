import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    import selenium.webdriver.firefox.options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait as WDW
    from selenium.webdriver.support import expected_conditions as EC
    print("All Modules are loaded")
except Exception as e:
    print("Error : {} ".format(e))

def setup_browser_options():
    options = selenium.webdriver.firefox.options.Options()
    options.add_argument("-profile")
    options.add_argument("/Users/aravindhpg/Library/Application Support/Firefox/Profiles/gj9o1pz6.aravindhpg")
    return options
# Opening Firefox with my own local Firefox Profile to bypass 2FA. The alternate option is to utilise a dummy business email/password of Browserstack account
driver = webdriver.Firefox(options=setup_browser_options())
URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()

def wait_click(xpath_location):
    WDW(driver,25).until(EC.visibility_of_element_located((By.XPATH,xpath_location))).click()

wait_click("//*[@title = 'Sign In']")
print("The title of the page is " + driver.title)
try:
    title = driver.title
    assert 'Dashboard' in title
    print('Assertion test passed - Live Dashboard has opened')
except Exception as e:
    print('Assertion test failed - Live dashboard did not open', format(e))
wait_click("//*[@id='live_cross_product_explore']")
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


