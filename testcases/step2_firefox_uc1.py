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
    options.add_argument(r"--desired_capabilities=DesiredCapabilities.FIREFOX")
    return options


# Opening Chrome with my own local Chrome Profile to bypass 2FA. The alternate option is to utilise a dummy business email/password of Browserstack account
URL = 'http://localhost:4444/wd/hub'
driver = webdriver.Remote(command_executor=URL, options=setup_browser_options())
URL = "https://browserstack.com"
driver.get(url=URL)
driver.maximize_window()


def wait_click(xpath_location):
    WDW(driver, 25).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()


wait_click("//*[@title = 'Sign In']")
driver.get("https://live.browserstack.com/dashboard")
wait_click("//*[div[contains(text(),'mac')]]")
wait_click("//*[@aria-label='Big Sur']")
wait_click("//*[@aria-label='chrome 113 latest']")

try:
    wait_click("//*[label[contains(text(),'Stop Session')]]")
    print("successfully logged into bstack live")
except Exception as e:
    print("Error : {} ".format(e))
driver.quit()
#
# options = selenium.webdriver.firefox.options.Options()
# options.add_argument("-profile")
# options.add_argument("/Users/aravindhpg/Library/Application Support/Firefox/Profiles/gj9o1pz6.aravindhpg")
# options.add_argument(r"--command_executor='http://localhost:4444/wd/hub'")
# options.add_argument(r"--desired_capabilities=DesiredCapabilities.FIREFOX")
# driver = webdriver.Remote(options = options)
#
# URL = "https://browserstack.com"
# driver.get(url=URL)
# print(driver.page_source)
# print ("logging into Browserstack")
#
# driver.find_element(By.LINK_TEXT,"Sign in").click()
# print("signed into browserstack")
#
# driver.find_element(By.LINK_TEXT,"Live").click()
# print("Sleeping now")
# time.sleep(120)
# driver.quit()

