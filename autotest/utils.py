#encoding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from autotest.models import TestCaseInfo, CaseStepInfo, CaseExecuteResult, ExecuteRecord
from autotest.keyword import *

def getBaiDu():
    browser = webdriver.Chrome(executable_path="D:\\chromedriver")
    browser.get('http://www.baidu.com')
    assert "百度" in browser.title
    elem = browser.find_element_by_id("kw")
    elem.send_keys("光荣之路")
    elem.send_keys(Keys.RETURN)

    time.sleep(20)
    browser.close()


# 获取测试用例
def getCaseSteps(case_id_list):
    print("case_id_list: %s" % case_id_list)
    #case_list = []
    # [{"caseId":1, "stepStep": 1, "testDescription":"打开谷歌浏览器"， "optionMethod": "open_browser","findmethod": "xpath", "element": None, "testData": ""chrome}],
    # caseid}
    case_step_list = []
    for caseId in case_id_list:
        try:
            case = TestCaseInfo.objects.filter(id = int(caseId))
            caseSteps = CaseStepInfo.objects.filter(case_id = int(caseId)).order_by("teststep")
            print("caseSteps: ", caseSteps)
            for caseStep in caseSteps:
                stepDict = {}
                stepDict["caseId"] = int(caseId)
                stepDict["stepStep"] = caseStep.teststep
                stepDict["testDescription"] = caseStep.testobjname
                stepDict["optionMethod"] = caseStep.optmethod.keyword_name
                stepDict["findmethod"] = caseStep.findmethod
                stepDict["locator"] = caseStep.evelement
                stepDict["testData"] = caseStep.testdata
                case_step_list.append(stepDict)
            print("case_step_list: ", case_step_list)
        except:
            print("error occurs")
    print("case_step_list: %s" % case_step_list)
    return case_step_list


def runStep(optionKeyWord, findmethod=None, locator=None, testData=None):
    print("###### optionKeyWord: %s" % optionKeyWord)

    if findmethod:
        if locator and testData:
            command = '%s("%s", "%s", "%s")'% (optionKeyWord, findmethod, locator,testData)
        elif locator and not testData:
            command = '%s("%s", "%s")' % (optionKeyWord, findmethod, locator)

        elif not locator and testData:
            command = '%s("%s", "%s")' % (optionKeyWord, findmethod, testData)
    elif testData:
        command = '%s("%s")' % (optionKeyWord, testData)
    else:
        command = "%s()" % (optionKeyWord)

    print("command: ", command)
    try:
        eval(command)
        return True
        #time.sleep(4)
    except Exception as e:
        print("runStep Error !!: %s" % e)



def runTestCase(case_id_list):
    '''[{'caseId': 2, 'stepStep': '1', 'testDescription': '打开谷歌浏览器', 'optionMethod': 'open_browser', 'findmethod': None, 'evelement': None, ,'testData': 'chrome'},
       {'caseId': 2, 'stepStep': '2', 'testDescription': '切换iframe', 'optionMethod': 'switch_to', 'findmethod': 'xpath', 'testData': None},
       {'caseId': 2, 'stepStep': '3', 'testDescription': '输入用户名', 'optionMethod': 'input', 'findmethod': 'xpath', 'testData': 'testman2020'}]
    '''
    caseStepList = getCaseSteps(case_id_list)
    resultDict = {}
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
        if runStep(optionKeyWord, findmethod, locator,testData):
            resultDict[caseId] = 'pass'
        else:
            resultDict[caseId] = 'fail'
    print("resultDict： %s" % resultDict)
    return resultDict



