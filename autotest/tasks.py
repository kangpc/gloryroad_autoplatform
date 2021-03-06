#encoding=utf-8
from __future__ import absolute_import, unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
from celery import shared_task
import time
from .models import *
from django.contrib.auth.models import User
from .utils import getExecuteCommand, captureScreen
from .keyword import *
import threading


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
#
# @shared_task
# def runTestCase(case_id_list):
#     print("case_id_list: ", case_id_list)
#     # 获取当前时间点时间戳，用于存储各个用例执行记录的执行id（相同）
#     execute_id = int(time.time())
#     print("execute_id: %s" % execute_id)
#     for caseId in case_id_list:
#         # 获取测试用例
#         caseExecute.delay(execute_id, caseId)
#         # with ThreadPoolExecutor(3) as executor:
#         #     executor.map(runTestCase, case_id_list)
#     print("&&&&&所有用例执行完毕！！")


@shared_task
def runSuite(*suite_id_list):
    if suite_id_list:
        print("case_id_list: ", suite_id_list)
        #获取当前时间点时间戳，用于存储各个用例执行记录的执行id（相同）
        execute_id = int(time.time())
        print("execute_id: %s" % execute_id)

        suite_id_case_id_dict = {}  # {'1': [1,2,3,4], '2': [1,3,4]}
        for suite_id in suite_id_list:
            case_id_list = []
            suiteInfo = TestSuiteInfo.objects.filter(id=suite_id).first()
            if suiteInfo:
                include_cases = suiteInfo.include_cases
                print("include_cases: %s" % include_cases)
                include_cases = eval(include_cases)  # [['1', '登录12306邮箱'], ['2', '登录12306邮箱用例1']]
                print("include_cases: %s" % include_cases)
                # 获取测试用例id列表
                for case in include_cases:
                    case_id_list.append(case[0])  # [1, 2]
                print("case_id_list: %s" % case_id_list)
                # 获取suiteid和用例列表的对应字典
                suite_id_case_id_dict[suite_id] = case_id_list  # {'1': [1,2,3,4], '2': [1,3,4]}
        print("suite_id_case_id_dict: %s" % suite_id_case_id_dict)
        for suite_id, case_id_list in suite_id_case_id_dict.items():  # 遍历suiteid和用例列表关联字典，传入用例执行函数，在执行记录表里记录执行记录和suiteid的关系
            print("case_id_list in for statement: %s" % case_id_list)
            # 获取测试用例
            for case_id in case_id_list:
                runTestCase.delay(execute_id, case_id, 'admin', suite_id)
            # with ThreadPoolExecutor(3) as executor:
            #     executor.map(runTestCase, case_id_list)
    print("定时任务运行完毕！！")



@shared_task
# 获取测试用例
def runTestCase(execute_id, caseId, username, suiteId=None):
    try:
        # 存储用例执行记录表（executerecord）
        print("#################用例开始执行#################")
        testCaseInfo = TestCaseInfo.objects.filter(id=int(caseId)).first()
        user = User.objects.filter(username=username).first()
        execute_record = ExecuteRecord()
        execute_record.case = testCaseInfo
        execute_record.status = 0 # 未执行
        execute_record.execute_user = user # 执行记录关联用户
        # 存储executerecord表的execute_id，存储规则：不会重复的时间戳int(time.time())
        execute_record.execute_id = execute_id  # 当前所有执行记录的执行id是同一个

        print("suiteId: %s" % suiteId)
        if suiteId:
            execute_record.suite_id = suiteId
        try:
            execute_record.save() # 一条数据保存一次
        except Exception as e:
            error_msg = traceback.format_exc()
            print("执行记录表保存出错，信息为： %s" % error_msg)
        print("execute_record.case: %s" % execute_record.case)
        print("execute_record.case_id: %s" % execute_record.case_id)
        # execute_id_list.append(execute_record.execute_id)
        caseSteps = CaseStepInfo.objects.filter(case_id = int(caseId)).order_by("teststep")
        print("caseSteps: ", caseSteps)
        case_result = {}  # 结果字典{"step1": "pass", "step2": "fail"}

        # 执行用例的每一个步骤
        for caseStep in caseSteps:
            print("$$$$$$caseStep %s: %s" % (caseStep.teststep, caseStep.testobjname))
            # 存CaseExecuteResult表
            case_execute_result = CaseExecuteResult()
            case_execute_result.execute_record = execute_record
            case_execute_result.step_id = caseStep.teststep
            case_execute_result.step_desc = caseStep.testobjname
            case_execute_result.save() # 保存表
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
                # 获取执行命令
                execute_command = getExecuteCommand(optionKeyWord, findmethod, locator, testData)

                if int(caseStep.teststep) == 1: # 执行到第一步，写入执行开始时间
                    print("第一条步骤，写入执行开始时间")
                    execute_record.execute_start_time = time.strftime("%Y-%m-%d %H:%M:%S")

                # 执行用例
                try:
                    if "open_browser" in execute_command:
                        execute_command = '%s("%s")' % (optionKeyWord, testData)
                        driver = eval(execute_command)
                    else:
                        eval(execute_command)
                except Exception as e:
                    error_msg = traceback.format_exc()
                    print("command 执行出错，错误信息如下：\n%s \n%s \n%s" % ('*'*40, error_msg, '*'*40))
                    file_name = time.strftime("%Y%m%d%H%M%S") + str(case_execute_result.execute_record_id) + "-" + str(case_execute_result.step_id)
                    capture_screen_path = captureScreen(driver, file_name)
                    execute_record.exception_info = error_msg
                    execute_record.capture_screen = capture_screen_path
                    case_execute_result.exception_info = error_msg
                    case_execute_result.capture_screen = capture_screen_path
                    case_result[caseStep.teststep] = 'fail'
                    print("case_result1: %s" % case_result)
                    case_execute_result.result = "fail"

                    try:
                        case_execute_result.save()  # 存结果表
                    except Exception as e:
                        print("结果表保存出错： %s" % e)
                    break  # 跳出当前用例的执行


                case_result[caseStep.teststep] = 'pass'
                case_execute_result.result = "pass"
                print("case_result1: %s" % case_result)
                try:
                    case_execute_result.save()  # 存结果表
                except Exception as e:
                    print("结果表保存出错： %s" % e)


            except Exception as e:
                error_msg = traceback.format_exc()
                print("步骤执行错误： %s" % error_msg)
                file_name = str(case_execute_result.execute_id) + "-"+str(case_execute_result.step_id)
                capture_screen_path = captureScreen(driver, file_name)
                # 执行记录表存储异常和截图信息
                execute_record.exception_info = error_msg
                execute_record.capture_screen = capture_screen_path
                # 用例执行结果表存储异常和截图信息
                case_execute_result.exception_info = error_msg
                case_execute_result.capture_screen = capture_screen_path
                case_result[caseStep.teststep] = 'fail'
                print("case_result1: %s" % case_result)
                case_execute_result.result = "fail"

                try:
                    case_execute_result.save() # 存结果表
                except Exception as e:
                    print("结果表保存出错： %s" % e)
                break # 跳出当前用例的执行

        print("case_result: %s" % case_result)

        # 如果用例的步骤都是通过的，则用例执行结果为pass
        if (len(set(case_result.values())) == 1) and (list(set(case_result.values()))[0]== 'pass'):
            print("用例执行结果成功！")
            execute_record.execute_result = 'pass'
        else:
            execute_record.execute_result = 'fail'
            print("用例(case_id:%s) 执行结果失败！"% execute_record.case_id)
        execute_record.execute_end_time = time.strftime("%Y-%m-%d %H:%M:%S")
        execute_record.status = 1 # 更新用例执行状态为已执行

        try:
            # 保存
            execute_record.save()
        except Exception as e:
            print("执行结果表保存结果失败: %s" % e)

    except Exception as e:
        error_msg =  traceback.format_exc()
        print("用例执行出错，信息为： %s" % error_msg)
    # print("execute_id_list: %s" % execute_id_list)
    # return execute_id_list
    print("当前用例：[%s] 执行完毕！" % testCaseInfo)

