#encoding=utf-8

import time
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from autotest.models import TestCaseInfo, CaseStepInfo, CaseExecuteResult, ExecuteRecord
from selenium import webdriver
from autotest.keyword import *
from .config import projectPath, screenRelativePath


def getBaiDu():
    browser = webdriver.Chrome(executable_path="D:\\chromedriver")
    browser.get('http://www.baidu.com')
    assert "百度" in browser.title
    elem = browser.find_element_by_id("kw")
    elem.send_keys("光荣之路")
    elem.send_keys(Keys.RETURN)

    time.sleep(20)
    browser.close()


def getExecuteCommand(optionKeyWord, findmethod=None, locator=None, testData=None):
    print("###### optionKeyWord: %s" % optionKeyWord)

    if findmethod:
        if locator and testData:
            command = '%s( "%s", "%s", "%s", driver=driver)'% (optionKeyWord, findmethod, locator,testData)
        elif locator and not testData:
            command = '%s("%s", "%s", driver=driver)' % (optionKeyWord, findmethod, locator)

        elif not locator and testData:
            command = '%s("%s", "%s", driver=driver)' % (optionKeyWord, findmethod, testData)
    elif testData:
        command = '%s("%s", driver=driver)' % (optionKeyWord, testData)
    else:
        command = "%s(driver=driver)" % (optionKeyWord)

    print("command: %s" % command)
    return command




#
# def captureScreen(driver, filename):
#     print("capture_screen_path: %s" % capture_screen_path)
#     # browser = webdriver.Chrome(r"D:\\chromedriver")
#     driver.set_window_size(1200, 900)
#     # browser.get("http://mail.126.com")  # Load page
#     driver.execute_script("""
#     (function () {
#       var y = 0;
#       var step = 100;
#       window.scroll(0, 0);
#
#       function f() {
#         if (y < document.body.scrollHeight) {
#           y += step;
#           window.scroll(0, y);
#           setTimeout(f, 50);
#         } else {
#           window.scroll(0, 0);
#           document.title += "scroll-done";
#         }
#       }
#
#       setTimeout(f, 1000);
#     })();
#   """)
#
#     for i in range(30):
#         if "scroll-done" in driver.title:
#             break
#         time.sleep(1)
#     begin = time.time()
#     file_path = capture_screen_path+"/"+filename+str(begin)+".png"
#     for i in range(10):
#         driver.save_screenshot(file_path)
#     end = time.time()
#     print(end - begin)
#     return file_path
#     #browser.close()



def captureScreen(driver, screenName):

    '''获取日期，如"2020-06-10,判断固定格式的日期是否存在，如"2019年\06月\10日"是否存在，如果不存在，新建一个，获取该路径，如果存在，则取该路径
        文件名格式：年月日时分秒+执行id+步骤id+".png"，如20200610224637-127-6.png
    '''

    print("projectPath: %s" %projectPath)
    print("screenRelativePath: %s" % screenRelativePath)

    year, month, day = time.strftime("%Y-%m-%d").split("-")
    print(year, month,day)
    relativeDatePath = os.path.join("%s年"%year,"%s月"%month,"%s日"%day)
    print("relativeDatePath: %s" % relativeDatePath)
    absoluteDatePath = os.path.join(projectPath, screenRelativePath, relativeDatePath)
    print("datePath: %s" % absoluteDatePath)
    print("os.path.exists(absoluteDatePath): %s" % os.path.exists(absoluteDatePath))
    if not os.path.exists(absoluteDatePath):
        os.makedirs(absoluteDatePath)
        print("os.path.exists(datePath): %s" % os.path.exists(absoluteDatePath))
    # # os.makedirs()
    # browser = webdriver.Chrome(r"D:\\chromedriver")
    # browser.set_window_size(1200, 900)
    # browser.get("http://mail.126.com")  # Load page
    picturePath = os.path.join(absoluteDatePath, screenName) + '.png'
    print("picturePath: %s" % picturePath)

    try:
        st =time.time()
        driver.get_screenshot_as_file(picturePath)
        et = time.time()
        print("total time: %s" %(et - st))
    except Exception  as e:
        print("error occurs: %s" % e)
    relativeScreenPath = os.path.join(screenRelativePath, relativeDatePath, screenName ) + '.png'
    print("relativePath: %s" % relativeScreenPath)
    return relativeScreenPath



