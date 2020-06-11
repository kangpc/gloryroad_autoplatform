#encoding=utf-8
from __future__ import absolute_import, unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
from celery import shared_task
import time
from .models import *
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


@shared_task
# 获取测试用例
def runTestCase(case_id_list):
    print("case_id_list: %s" % case_id_list)
    #case_list = []
    # [{"caseId":1, "testStep": 1, "testDescription":"打开谷歌浏览器"， "optionMethod": "open_browser","findmethod": "xpath", "element": None, "testData": ""chrome}],
    # caseid}
    #case_step_list = []
    # execute_id_list = []
    for caseId in case_id_list:
        try:
            # 存储用例执行记录表（executerecord）
            print("#################保存执行表#################")
            execute_record = ExecuteRecord()
            execute_record.case_id = caseId
            execute_record.status = 0 # 未执行
            execute_record.save() # 一条数据保存一次
            # execute_id_list.append(execute_record.execute_id)
            caseSteps = CaseStepInfo.objects.filter(case_id = int(caseId)).order_by("teststep")
            print("caseSteps: ", caseSteps)
            case_result = {}  # 结果字典{"step1": "pass", "step2": "fail"}

            # 执行用例的每一个步骤
            for caseStep in caseSteps:
                print("$$$$$$caseStep %s: %s" % (caseStep.teststep, caseStep.testobjname))
                # 存CaseExecuteResult表
                case_execute_result = CaseExecuteResult()
                case_execute_result.execute_id = execute_record.execute_id
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
                        print("command 执行出错： %s" % error_msg)
                        file_name = time.strftime("%Y%m%d%H%M%S") + str(case_execute_result.execute_id) + "-" + str(case_execute_result.step_id)
                        capture_screen_path = captureScreen(driver, file_name)

                        execute_record.exception_info = error_msg
                        execute_record.capture_screen = capture_screen_path
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

                    execute_record.exception_info = error_msg
                    execute_record.capture_screen = capture_screen_path
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
            print("用例执行出错，信息为： %s" % e)
    # print("execute_id_list: %s" % execute_id_list)
    # return execute_id_list
    print("&&&&&用例执行完毕！")

