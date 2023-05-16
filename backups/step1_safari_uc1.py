import os
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    import selenium.webdriver.safari.options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait as WDW
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains as AC
    print("All Modules are loaded")
except Exception as e:
    print("Error module: {} ".format(e))

def setup_browser_options():
    options = selenium.webdriver.safari.options.Options()
    return options
# Safari does not support profile. The alternate option is to utilise a dummy business email/password of Browserstack account
driver = webdriver.Safari(options=setup_browser_options())

try:
    URL = "https://browserstack.com"
    driver.get(url=URL)
    driver.maximize_window()


    def wait_click(xpath_location):
        WDW(driver, 50).until(EC.visibility_of_element_located((By.XPATH, xpath_location))).click()


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
    # wait_click("//*[@title = 'Sign In']")
    # wait_click("//*[@id='live_cross_product_explore']")
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
            EC.invisibility_of_element_located((By.XPATH, "//*[label[contains(text(),'Stop Session')]]")))
        print("Could not login to Live as trial expired")

    except Exception as e:
        print("Could not login to Live due to error")
        print("Error final : {} ".format(e))
    driver.quit()

except Exception as e:
    print("Error final : {} ".format(e))
    driver.quit()
# driver.find_element(By.LINK_TEXT, "Sign in").click()
# WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='user_email_login']")))
# input_URL = driver.find_element(By.XPATH, "//*[@id='user_email_login']")
# input_URL.clear()
# input_URL.send_keys("delerik894@pixiil.com")
# input_URL = driver.find_element(By.XPATH, "//*[@id='user_password']")
# input_URL.clear()
# input_URL.send_keys("password@123")
# driver.find_element(By.XPATH, "//*[@value='Sign me in']").click()
# print("signed into browserstack")
# time.sleep(2)
# driver.find_element(By.LINK_TEXT,"Live").click()
# print("opened live dashboard")
# WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Big Sur"]'))).click()
# print("selected Big Sur")
# WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="chrome 113 latest"]'))).click()
# print("selected Chrome 113 Latest")
# print("Sleeping finally now")
# time.sleep(20)
# driver.quit()
#
