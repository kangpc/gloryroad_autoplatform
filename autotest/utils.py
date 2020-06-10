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
                print("$$$$$$caseStep %s: %s" % (caseStep.teststep, caseStep))
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
                        print("command 执行出错： %s" % e)
                        file_name = str(case_execute_result.execute_id) + "-" + str(case_execute_result.step_id)
                        capture_screen_path = captureScreen(driver, file_name)

                        execute_record.exception_info = e
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
                    print("步骤执行错误： %s" % e)
                    file_name = str(case_execute_result.execute_id) + "-"+str(case_execute_result.step_id)
                    capture_screen_path = captureScreen(driver, file_name)
                    print("capture_screen_path: %s" % capture_screen_path)

                    execute_record.exception_info = e
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
                print("用例执行结果失败！")
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

