import time
import os

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
    print("Error : {} ".format(e))

def setup_browser_options():
    options = selenium.webdriver.safari.options.Options()
    options.add_argument(r"--desired_capabilities=DesiredCapabilities.SAFARI")
    return options
# Safari does not support profile. The alternate option is to utilise a dummy business email/password of Browserstack account
URL = 'http://localhost:4444/wd/hub'
driver = webdriver.Remote(command_executor=URL,options=setup_browser_options())

try:
    URL = "https://browserstack.com"
    driver.get(url=URL)
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
    # wait_click("//*[@title = 'Sign In']")
    # wait_click("//*[@id='live_cross_product_explore']")
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
# options = selenium.webdriver.safari.options.Options()
# options.add_argument('--disable-blink-features=AutomationControlled')
# # options.add_argument("-profile")
# # options.add_argument("/Users/aravindhpg/Library/Application Support/Firefox/Profiles/gj9o1pz6.aravindhpg")
# options.add_argument(r"--command_executor='http://localhost:4444/wd/hub'")
# options.add_argument(r"--desired_capabilities=DesiredCapabilities.SAFARI")
# driver = webdriver.Remote(options = options)
#
# URL = "https://browserstack.com"
# driver.get(url=URL)
# print(driver.page_source)
# print ("logging into Browserstack")
# driver.maximize_window()
#
# driver.find_element(By.LINK_TEXT,"Sign in").click()
# print("signed into browserstack")
# time.sleep(200)
# #
# # driver.find_element(By.LINK_TEXT,"Live").click()
# # print("Sleeping now")
# # time.sleep(20)
# # driver.quit()

