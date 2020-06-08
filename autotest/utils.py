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
def runTestCase(case_id_list):
    print("case_id_list: %s" % case_id_list)
    # case_list = []
    # [{"caseId":1, "testStep": 1, "testDescription":"打开谷歌浏览器"， "optionMethod": "open_browser","findmethod": "xpath", "element": None, "testData": ""chrome}],
    # caseid}
    # case_step_list = []
    # execute_id_list = []
    for caseId in case_id_list:
        try:
            # 存储用例执行记录表（executerecord）
            print("#################保存执行表#################")
            execute_record = ExecuteRecord()
            execute_record.case_id = caseId
            execute_record.status = 0  # 未执行
            execute_record.save()  # 一条数据保存一次
            # execute_id_list.append(execute_record.execute_id)
            caseSteps = CaseStepInfo.objects.filter(case_id=int(caseId)).order_by("teststep")
            print("caseSteps: ", caseSteps)
            case_result = {}  # 结果字典{"step1": "pass", "step2": "fail"}

            # 执行用例的每一个步骤
            for caseStep in caseSteps:
                print("$$$$$$caseStep %s: %s" % (caseStep.teststep, caseStep))
                # 存CaseExecuteResult表
                case_execute_result = CaseExecuteResult()
                case_execute_result.execute_id = execute_record.execute_id
                case_execute_result.step_id = caseStep.teststep
                case_execute_result.step_desc = caseStep.testobjname
                case_execute_result.save()  # 保存表
                try:
                    # 执行用例
                    # 执行时，更新执行记录表（ExecuteRecord）,执行结束后，更新执行结束时间(execute_end_time)以及执行结果(status、execute_result、capture_screen)
                    optionKeyWord = caseStep.optmethod.keyword_name
                    findmethod = caseStep.findmethod
                    locator = caseStep.evelement
                    testData = caseStep.testdata
                    print("optionKeyWord: %s" % optionKeyWord)
                    print("findmethod: %s" % findmethod)
                    print("element: %s" % locator)
                    print("testData: %s" % testData)
                    execute_command = getExecuteCommand(optionKeyWord, findmethod, locator, testData)
                    if "open_browser" in execute_command:
                        execute_command = '%s("%s")' % (optionKeyWord, testData)
                        print("execute_command:%s" % execute_command)
                        try:
                            driver = eval(execute_command)
                        except Exception as e:
                            print("command 执行出错： %s" % e)
                    else:
                        print("execute_command:%s" % execute_command)
                        try:
                            eval(execute_command)
                        except Exception as e:
                            print("command 执行出错： %s" % e)

                    if int(caseStep.teststep) == 1:  # 执行到第一步，写入执行开始时间
                        print("第一条步骤，写入执行开始时间")
                        execute_record.execute_start_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    case_result[caseStep.teststep] = 'pass'
                    case_execute_result.result = "pass"
                    print("case_result1: %s" % case_result)
                    try:
                        case_execute_result.save()  # 存结果表
                    except Exception as e:
                        print("结果表保存出错： %s" % e)

                except Exception as e:
                    print("步骤执行错误： %s" % e)
                    capture_screen_path = captureScreen()
                    execute_record.exception_info = e
                    case_result[caseStep.teststep] = 'fail'
                    print("case_result1: %s" % case_result)
                    case_execute_result.result = "fail"

                    try:
                        case_execute_result.save()  # 存结果表
                    except Exception as e:
                        print("结果表保存出错： %s" % e)
                    break  # 跳出当前用例的执行

            print("case_result: %s" % case_result)
            # 如果用例的步骤都是通过的，则用例执行结果为pass
            if (len(set(case_result.values())) == 1) and (list(set(case_result.values()))[0] == 'pass'):
                print("用例执行结果成功！")
                execute_record.execute_result = 'pass'
            else:
                execute_record.execute_result = 'fail'
                print("用例执行结果失败！")
            execute_record.execute_end_time = time.strftime("%Y-%m-%d %H:%M:%S")
            execute_record.status = 1  # 更新用例执行状态为已执行

            try:
                # 保存
                execute_record.save()
            except Exception as e:
                print("执行结果表保存结果失败: %s" % e)

        except Exception as e:
            print("用例执行出错，信息为： %s" % e)
    # print("execute_id_list: %s" % execute_id_list)
    # return execute_id_list
    print("&&&&&用例执行完毕！")

    #print("case_step_list: %s" % case_step_list)
    #return case_step_list


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


def captureScreen():
    pass
    return 1


#
# def runTestCase(execute_id_list):
#     '''[{'caseId': 2, 'stepStep': '1', 'testDescription': '打开谷歌浏览器', 'optionMethod': 'open_browser', 'findmethod': None, 'evelement': None, ,'testData': 'chrome'},
#        {'caseId': 2, 'stepStep': '2', 'testDescription': '切换iframe', 'optionMethod': 'switch_to', 'findmethod': 'xpath', 'testData': None},
#        {'caseId': 2, 'stepStep': '3', 'testDescription': '输入用户名', 'optionMethod': 'input', 'findmethod': 'xpath', 'testData': 'testman2020'}]
#     '''
#     caseStepList = getCaseSteps(case_id_list)
#     resultDict = {}
#     for stepDict in caseStepList:
#         caseId = stepDict["caseId"]
#         caseName = TestCaseInfo.objects.get(id=caseId).name
#         print("################执行用例名################： %s" % caseName)
#         print("stepStep: %s" % stepDict["stepStep"])
#         print("testDescription: %s" % stepDict["testDescription"])
#         # 更新用例执行结果(executerecord)
#         """
#             execute_id = models.AutoField(primary_key=True)
#             case_id = models.CharField(max_length=100, null=False)
#             status = models.IntegerField(null=True, help_text="0：表示未执行，1：表示已执行")
#             execute_result = models.CharField(max_length=100, null=True)
#             create_time = models.DateTimeField('创建时间', auto_now_add=True)
#             exception_info= models.CharField(max_length=500, blank=True, null=True)
#             capture_screen = models.CharField(max_length=500, blank=True, null=True)
#             execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
#             execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True)
#         """
#
#
#         # 执行时，更新执行记录表（ExecuteRecord）的执行开始时间（execute_start_time）、执行结束后，更新执行结束时间(execute_end_time)以及执行结果(status、execute_result、capture_screen)
#         case_result = {}  # 结果字典{"step1": "pass", "step2": "fail"}
#         # stepDict = {}
#         # stepDict["caseId"] = int(caseId)
#         # stepDict["testStep"] = caseStep.teststep
#         # stepDict["testDescription"] = caseStep.testobjname
#         # stepDict["optionMethod"] = caseStep.optmethod.keyword_name
#         # stepDict["findmethod"] = caseStep.findmethod
#         # stepDict["locator"] = caseStep.evelement
#         # stepDict["testData"] = caseStep.testdata
#
#         optionKeyWord = stepDict["optionMethod"]
#         findmethod = stepDict["findmethod"]
#         locator = stepDict["locator"]
#         testData = stepDict["testData"]
#         print("optionKeyWord: %s" % optionKeyWord)
#         print("findmethod: %s" % findmethod)
#         print("element: %s" % locator)
#         print("testData: %s" % testData)
#
#     # # 执行时，更新执行记录表（ExecuteRecord）的执行开始时间（execute_start_time）、执行结束后，更新执行结束时间(execute_end_time)以及执行结果(status、execute_result、capture_screen)
#     #     optionKeyWord = caseStep.optmethod.keyword_name
#     #     findmethod = caseStep.findmethod
#     #     locator = caseStep.evelement
#     #     testData = caseStep.testdata
#     #     print("optionKeyWord: %s" % optionKeyWord)
#     #     print("findmethod: %s" % findmethod)
#     #     print("element: %s" % locator)
#     #     print("testData: %s" % testData)
#     #     execute_command = getExecuteCommand(optionKeyWord, findmethod, locator, testData)
#     #     try:
#     #         eval(execute_command)
#     #         case_result[caseId] = 'pass'
#     #         case_execute_result.result = "pass"
#
#     # except Exception as e:
#     #     capture_screen_path = captureScreen()
#     #     execute_record.exception_info = e
#     #
#     #     case_result[caseId] = 'fail'
#     #     case_execute_result.result = "fail"
#     #     break  # 该步骤运行失败，跳出该用例的执行
#
#     print("resultDict： %s" % resultDict)
#     return resultDict
#


