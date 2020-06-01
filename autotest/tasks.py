#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from celery import shared_task
import time
from .models import *
from .utils import getCaseSteps, runStep


# # 带参数的分布式任务
# @shared_task
# def updateData(id, info):
#     print("go into updateData function.")
#     now = time.strftime("%H:%M:%S")
#     print("now: %s" % now)
#     try:
#         PersonInfo.objects.filter(id=id).update(**info)
#         print("PersonInfo.objects.filter(id=%s): " % id,PersonInfo.objects.filter(id=id))
#         return 'Execute successfully'
#     except:
#         return 'Execute Fail'

@shared_task
def getBaiDu():
    print("gointo getBaiDu")
    browser = webdriver.Chrome(executable_path="D:\\chromedriver")
    browser.get('http://www.baidu.com')
    assert "百度" in browser.title
    elem = browser.find_element_by_id("kw")
    elem.send_keys("光荣之路")
    elem.send_keys(Keys.RETURN)

    time.sleep(20)
    #browser.close()


@shared_task
def runTestCase(case_id_list):
    '''[{'caseId': 2, 'stepStep': '1', 'testDescription': '打开谷歌浏览器', 'optionMethod': 'open_browser', 'findmethod': None, 'evelement': None, ,'testData': 'chrome'},
       {'caseId': 2, 'stepStep': '2', 'testDescription': '切换iframe', 'optionMethod': 'switch_to', 'findmethod': 'xpath', 'testData': None},
       {'caseId': 2, 'stepStep': '3', 'testDescription': '输入用户名', 'optionMethod': 'input', 'findmethod': 'xpath', 'testData': 'testman2020'}]
    '''
    caseStepList = getCaseSteps(case_id_list)

    for stepDict in caseStepList:
        caseId = stepDict["caseId"]
        caseName = TestCaseInfo.objects.get(id=caseId).name
        print("################执行用例名################： %s" % caseName)
        print("stepStep: %s" % stepDict["stepStep"])
        print("testDescription: %s" % stepDict["testDescription"])
        optionKeyWord = stepDict["optionMethod"]
        findmethod = stepDict["findmethod"]
        locator = stepDict["locator"]
        testData = stepDict["testData"]
        print("optionKeyWord: %s" % optionKeyWord)
        print("findmethod: %s" % findmethod)
        print("element: %s" % locator)
        print("testData: %s" % testData)
        runStep(optionKeyWord, findmethod, locator,testData)
