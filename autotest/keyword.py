
from selenium.webdriver.common.keys import Keys
import os
import time
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

# browser = webdriver.Chrome(executable_path="D:\\chromedriver")
# browser.get('http://www.baidu.com')
# assert "百度" in browser.title
# elem = browser.find_element_by_id("kw")
# elem.send_keys("光荣之路")
# elem.send_keys(Keys.RETURN)
#
# time.sleep(20)
# browser.close()


# browser = webdriver.Chrome(executable_path="D:\\chromedriver")
# browser.get('https://rancher-tx.yunjiweidian.com/login')
# #assert "Log In" in browser.page_source
# time.sleep(5)
# loginElement = browser.find_element_by_id("login-username-local")
# loginElement.send_keys("develop")
#
# passwordElement = browser.find_element_by_id("login-password-local")
# passwordElement.send_keys("Rancher@123")
#
# loginButton = browser.find_element(by = "xpath", value = "//button[contains(text(),'Log In'")
# loginButton.click()
#
# # time.sleep(20)
# # browser.close()


# global_values = {}

#driver = ""

def is_xpath(exp):
    if ("//" in exp) or ("[" in exp) or ("@" in exp):
        return True
    return False

def open_browser(browser_name):
    print("!!!! going into open_browser")
    if "ie" in browser_name.lower():
        driver  = webdriver.Ie(executable_path="e:\\IEDriverServer")
    elif "chrome" in browser_name.lower():
        driver  = webdriver.Chrome(executable_path="D:\\chromedriver")
    else:
        driver = webdriver.Firefox(executable_path="e:\\geckodriver")

    return driver


def find_element(driver, locate_method,locate_exp):

    try:
        element = WebDriverWait(driver, 10).until \
        (lambda x: x.find_element(locate_method,locate_exp))
    except TimeoutException as e:
        print("*******:",locate_method,locate_exp)
        # 捕获NoSuchElementException异常
        traceback.print_exc()
        raise e
    return element


#xpath>//a[contains(text(),'密码登录')]
# def get_element(driver,locator_exp):
#     print("当前定位的section和option:",locator_exp)
#     section_name = locator_exp.split(",")[0]
#     option_name = locator_exp.split(",")[1]
#     element_locator = read_ini_file_option(
#         PageElementLocator_file_path, section_name, option_name)
#     element = find_element(
#         driver, element_locator.split(">")[0], element_locator.split(">")[1])
#     return element




def visit(url, driver=None):
    print("driver: %s" % driver)
    driver.get(url)



def input(locate_method,locate_exp,content, driver=None):
    print("driver: %s" % driver)
    print("locate_exp: %s" % locate_exp)
    if is_xpath(locate_exp):
        element = driver.find_element_by_xpath(locate_exp)
        element.send_keys(content)
    else:
        element = find_element(driver, locate_method,locate_exp)
        element.send_keys(content)


def click(locate_method,locate_exp, driver=None):
    print("driver: %s" % driver)
    if is_xpath(locate_exp):
        element = driver.find_element_by_xpath(locate_exp)
        element.click()
    else:
        element = find_element(locate_method,locate_exp)
        element.click()


def sleep(seconds):
    time.sleep(float(seconds))

def assert_word(expected_word, driver=None):
    print("driver: %s" % driver)
    assert expected_word in driver.page_source

def switch_to(locate_method,locate_exp, driver=None):
    print("driver: %s" % driver)
    if is_xpath(locate_exp):
        driver.switch_to.frame(driver.find_element_by_xpath(locate_exp))
    else:
        element = find_element(locate_method,locate_exp)
        driver.switch_to.frame(element)

def switch_back(driver=None):
    print("driver: %s" % driver)
    driver.switch_to.default_content()

def quit(driver=None):
    print("driver: %s" % driver)
    driver.quit()


# open_browser("chrome")