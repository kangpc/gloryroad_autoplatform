#encoding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os
import time
from concurrent.futures import ThreadPoolExecutor
from django.contrib import auth
from .models import TestCaseInfo, ProjectInfo, CaseStepInfo, CaseExecuteResult, ExecuteRecord, ModuleInfo, TestSuiteInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .utils import runTestCase
from .tasks import runTestCase
from .config import projectPath, screenRelativePath

# Create your views here.

# from .tasks import getBaiDu, runTestCase


# 测试全选
def caseList(request):
    case_list = TestCaseInfo.objects.all()

    return render(request, "testCheckAll.html")


# 搜索功能
@login_required
def caseSearch(request):
    username = request.session.get('user', '') # 从session获取用户
    search_caseName = request.GET.get('casename', '')
    case_list = TestCaseInfo.objects.filter(name__icontains=search_caseName)
    return render(request, 'case_manage.html', {'user': username, 'cases': case_list})

# @login_required
# def caseSubmit(request):
#     if request.method == "POST":
#         case_id_list = request.POST.getlist('testcase')
#         if case_id_list:
#             print("case_id_list: ", case_id_list)
#             response = HttpResponseRedirect('caseSubmit/')
#         else:
#             print("no case_id_list")
#             return HttpResponse("fail")


@login_required
def caseStepSearch(request):
    username = request.session.get('user','') # 读取session
    search_caseName = request.GET.get('caseName', '')
    caseStep_list = CaseStepInfo.objects.filter(case__name__contains=search_caseName)
    print("caseStep_list: %s" % caseStep_list)
    return render(request, 'casestep_manage.html', {'user': username, 'casesteps': caseStep_list})

# 用例管理
@login_required
def case_manage(request):
    if request.method == "POST":
        username = request.session.get('user', '')
        print("username: %s" % username)
        case_id_list = request.POST.getlist('testcase')
        if case_id_list:
            print("case_id_list: ", case_id_list)
            # 获取当前时间点时间戳，用于存储各个用例执行记录的执行id（相同）
            execute_id = int(time.time())
            print("execute_id: %s" % execute_id)
            for caseId in case_id_list:
                # 获取测试用例
                runTestCase.delay(execute_id, caseId, username)
                # with ThreadPoolExecutor(3) as executor:
                #     executor.map(runTestCase, case_id_list)
            return HttpResponse("ok")
        else:
            print("no case_id_list")
            return HttpResponse("fail")
    else:
        case_list = TestCaseInfo.objects.all()
        case_account = TestCaseInfo.objects.all().count() # 统计产品数
        username = request.session.get('user', '')
        paginator = Paginator(case_list, 8) # 生成Paginator对象，设置每页显示8条记录
        page = request.GET.get('page', 1) # 获取当前的页码数，默认为第一页
        currentPage = int(page) # 把获取的当前页数转成整数类型
        try:
            case_list = paginator.page(currentPage) # 获取当前页数的记录列表
        except PageNotAnInteger:
            case_list = paginator.page(1) # 如果输入的页数不是整数，则显示第一页内容
        except EmptyPage:
            case_list = paginator.page(paginator.num_pages) # 如果输入的页数不在系统的页数中，则显示最后一页
        return render(request, "case_manage.html", {'user': username, "cases": case_list, "caseaccounts": case_account})


# 用例步骤
@login_required
def casestep_manage(request):
    username = request.session.get('user', '')
    caseid = request.GET.get('webcase.id', None)
    print("caseid: %s" % caseid)
    testcase = TestCaseInfo.objects.get(id=caseid)
    casestep_list = CaseStepInfo.objects.filter(case_id=caseid).order_by('teststep')
    print("casestep_list: ", casestep_list)
    paginator = Paginator(casestep_list, 8) # 生成paginator对象，设置每页显示8条记录
    page = request.GET.get('page', 1) # 获取当前的页码数，默认为第一页
    currentPage = int(page) # 把获取的当前页码数转成整数类型

    try:
        casestep_list = paginator.page(currentPage)  # 获取当前页数的记录列表
    except PageNotAnInteger:
        casestep_list = paginator.page(1)  # 如果输入的页数不是整数，则显示第一页内容
    except EmptyPage:
        casestep_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中，则显示最后一页

    return render(request, "casestep_manage.html", {"user": username, "testcase": testcase, "casesteps": casestep_list})



# 用例步骤
@login_required
def suite_manage(request):
    if request.method == "POST":
        username = request.session.get('user', '')
        print("username: %s" % username)
        suite_id_list = request.POST.getlist('testsuite')
        if suite_id_list:
            print("case_id_list: ", suite_id_list)
            # 获取当前时间点时间戳，用于存储各个用例执行记录的执行id（相同）
            execute_id = int(time.time())
            print("execute_id: %s" % execute_id)

            suite_id_case_id_dict = {} # {'1': [1,2,3,4], '2': [1,3,4]}
            for suite_id in suite_id_list:
                case_id_list = []
                suiteInfo = TestSuiteInfo.objects.filter(id=suite_id).first()
                # include_cases = suiteInfo.include_cases
                include_cases = suiteInfo.cases.all()
                print("include_cases: %s" % include_cases)
                # include_cases = eval(include_cases)  # [['1', '登录12306邮箱'], ['2', '登录12306邮箱用例1']]
                # print("include_cases: %s" % include_cases)
                # 获取测试用例id列表
                for case in include_cases:
                    case_id_list.append(case.id) # [1, 2]
                print("case_id_list: %s" % case_id_list)
                # 获取suiteid和用例列表的对应字典
                suite_id_case_id_dict[suite_id] = case_id_list #  {'1': [1,2,3,4], '2': [1,3,4]}
            print("suite_id_case_id_dict: %s" % suite_id_case_id_dict)
            for suite_id, case_id_list in suite_id_case_id_dict.items(): # 遍历suiteid和用例列表关联字典，传入用例执行函数，在执行记录表里记录执行记录和suiteid的关系
                print("case_id_list in for statement: %s" % case_id_list)
                # 获取测试用例
                for case_id in case_id_list:
                    runTestCase.delay(execute_id, case_id, username, suite_id)
                # with ThreadPoolExecutor(3) as executor:
                #     executor.map(runTestCase, case_id_list)
            return HttpResponse("ok")
        else:
            print("no case_id_list")
            return HttpResponse("fail")
    elif request.method == 'GET':
        username = request.session.get('user', '')
        testsuite_data = TestSuiteInfo.objects.all()
        suite_list = []
        for suite in testsuite_data:
            suite_dict = {}
            suite_dict['id'] = suite.id
            suite_dict['suite_name'] = suite.suite_name
            suite_dict['belong_project'] = suite.belong_project.project_name
            suite_dict['belong_module'] = suite.belong_module.module_name
            print("suite.cases.all(): %s" % suite.cases.all())
            # include_cases = eval(suite.include_cases) # [['1', '登录12306邮箱'], ['2', '登录12306邮箱用例1']]
            include_cases = suite.cases.all() # [['1', '登录12306邮箱'], ['2', '登录12306邮箱用例1']]
            print("include_cases: %s" % include_cases)
            include_cases_list = []
            for case in include_cases:
                include_cases_dict = {}
                include_cases_dict['case_id'] =  case.id
                include_cases_dict['case_desc'] =  case.name
                include_cases_list.append(include_cases_dict)
            print("include_cases_list: %s" % include_cases_list)

            suite_dict['include_cases'] = len(include_cases_list) # 暂时取列表的长度，include_cases_list保留
            suite_dict['create_time'] = suite.create_time
            suite_dict['update_time'] = suite.update_time
            suite_list.append(suite_dict)
        print("suite_list: %s" % suite_list)

        paginator = Paginator(suite_list, 8) # 生成paginator对象，设置每页显示8条记录
        page = request.GET.get('page', 1) # 获取当前的页码数，默认为第一页
        currentPage = int(page) # 把获取的当前页码数转成整数类型

        try:
            casestep_list = paginator.page(currentPage)  # 获取当前页数的记录列表
        except PageNotAnInteger:
            casestep_list = paginator.page(1)  # 如果输入的页数不是整数，则显示第一页内容
        except EmptyPage:
            casestep_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中，则显示最后一页

        return render(request, "suite_manage.html", {"user": username, "testsuites": suite_list})



def case_result_level_one(request):

    return render(request, "case_result_level1.html")


# 用例结果
@login_required
def case_result_level_two(request):
    username = request.session.get('user', '')
    runStatus = request.GET.get("alreadyrun", '')
    suiteId = request.GET.get("suiteid", '')
    historySuiteId = request.GET.get("historysuiteid", '')
    # runStatus: 0: 待执行，1： 已执行
    if runStatus:
        print("runStatus: %s" % runStatus)
        case_recored_list = ExecuteRecord.objects.filter(status = 1).order_by('-create_time') if (str(runStatus) == '1') else ExecuteRecord.objects.filter(status=0)
        print("case_recored_list: ", case_recored_list)
        case_list = []
        success_num = 0  # 获取成功用例数，用于填充echart图
        fail_num = 0  # 存储失败用例数，用于填充echart图
        for record in case_recored_list:
            case_dict = {}
            case_info = TestCaseInfo.objects.filter(id = record.case_id).first()
            print("case_info: ,", case_info)
            case_dict["case_id"] = record.case_id
            case_dict["execute_record_id"] = record.id
            case_dict["execute_result"] = '' if not record.execute_result else record.execute_result
            case_dict["exception_info"] = '' if  not record.exception_info else record.exception_info
            case_dict["capture_screen"] = '' if not record.capture_screen else record.capture_screen
            case_dict["execute_start_time"] = record.execute_start_time
            case_dict["belong_module"] = case_info.belong_module.module_name
            case_dict["name"] = case_info.name
            case_dict["author"] = case_info.author
            case_dict["create_time"] = case_info.create_time
            print("case_dict: %s" % case_dict)
            if record.execute_result == "pass":
                success_num += 1
            else:
                fail_num += 1
            print("case_dict: %s" % case_dict)
            case_list.append(case_dict)

        print("case_list: %s" % case_list)
        case_account = len(case_list)

        #分页：
        paginator = Paginator(case_list, 8) # 生成Paginator对象，设置每页显示8条记录
        page = request.GET.get('page', 1) # 获取当前的页码数，默认为第一页
        currentPage = int(page) # 把获取的当前页数转成整数类型
        try:
            case_list = paginator.page(currentPage) # 获取当前页数的记录列表
        except PageNotAnInteger:
            case_list = paginator.page(1) # 如果输入的页数不是整数，则显示第一页内容
        except EmptyPage:
            case_list = paginator.page(paginator.num_pages) # 如果输入的页数不在系统的页数中，则显示最后一页

        return render(request, "case_result_level2.html", {'user': username, "cases": case_list, "caseaccounts": case_account, "successnumber": success_num, "failnumber": fail_num})

    if suiteId: # 如果请求中含有suiteid参数
        print("suiteId: %s" % suiteId)
        suite_info = TestSuiteInfo.objects.filter(id=suiteId).first()
        # include_cases = eval(suite_info.include_cases)  # [['1', '登录12306邮箱'], ['2', '登录12306邮箱用例1']]
        include_cases = suite_info.cases.all()
        print("include_cases: %s" % include_cases)
        case_id_list = []
        for case in include_cases:
            case_id_list.append(case.id)
        print("case_id_list: %s" % case_id_list)
        # 通过max获取executerecord表中用例id对应的最大的execute_id，即获取到最新的执行记录
        execute_id_in_execute_record = max([record.execute_id for record in ExecuteRecord.objects.filter(case_id = case_id_list[0])]) # 因为case_id_list中所有的用例本次执行的execute_id是一样的，所以用一个case来获取execute_id就可以了
        print("execute_id_in_execute_record: %s" % execute_id_in_execute_record)

        # 用获取到的execute_id反过来查找对应的所有的执行记录，每一条记录即是一条case的执行记录，结果即查到本次提交的测试集中所有用例的最新的执行结果记录了
        execute_record_data = ExecuteRecord.objects.filter(execute_id=execute_id_in_execute_record).all()
        print("execute_record_data: %s" % execute_record_data)
        case_list = []
        success_num = 0 # 获取成功用例数，用于填充echart图
        fail_num = 0 # 存储失败用例数，用于填充echart图
        for record in execute_record_data: # 组合所有执行记录的信息，填充到模板中
            case_dict = {}
            case_info = TestCaseInfo.objects.filter(id = record.case_id).first()
            print("case_info: ", case_info)
            case_dict["case_id"] = record.case_id
            case_dict["execute_record_id"] = record.id
            case_dict["execute_result"] = '' if not record.execute_result else record.execute_result
            case_dict["exception_info"] = '' if  not record.exception_info else record.exception_info
            case_dict["capture_screen"] = '' if not record.capture_screen else record.capture_screen
            case_dict["execute_start_time"] = record.execute_start_time
            case_dict["belong_module"] = case_info.belong_module.module_name
            case_dict["name"] = case_info.name
            case_dict["author"] = case_info.author
            case_dict["create_time"] = case_info.create_time
            if record.execute_result == "pass":
                success_num += 1
            else:
                fail_num += 1
            print("case_dict: %s" % case_dict)
            case_list.append(case_dict)

        print("case_list: %s" % case_list)
        case_account = len(case_list)
        return render(request, "case_result_level2.html", {'user': username, "cases": case_list, "caseaccounts": case_account, "successnumber": success_num, "failnumber": fail_num, "suiteid": suiteId})

    if historySuiteId: # 如果请求中含有historySuiteId参数,则获取该suiteid对应的所有的用例结果
        print("historySuiteId: %s" % historySuiteId)
        # 获取到historySuiteId对应的executerecord表中的suite_id为historySuiteId的所有数据，获取用例每一条数据的exetuterrecord_id和case_id，传给result_level_two页面，然后再result_level_two页面把exetuterrecord_id传给执行详情获取步骤信息
        execute_record_data = ExecuteRecord.objects.filter(suite_id = historySuiteId).all()
        print("execute_record_data: %s" % execute_record_data)
        # execute_record_list = [{"execute_record_id": 1, "case_id": 1}, {"execute_record_id": 2, "case_id": 2}]
        execute_record_list = []
        for record_data in execute_record_data:
            record_dict = {}
            record_dict["execute_record_id"] = record_data.id
            record_dict["case_id"] = record_data.case_id
            record_dict["execute_record_id"] = record_data.id
            execute_record_list.append(record_dict)
        print("execute_record_list: %s" % execute_record_list)

        case_list = []
        success_num = 0 # 获取成功用例数，用于填充echart图
        fail_num = 0 # 存储失败用例数，用于填充echart图
        for record in execute_record_data: # 组合所有执行记录的信息，填充到模板中
            case_dict = {}
            case_info = TestCaseInfo.objects.filter(id = record.case_id).first()
            print("case_info: ", case_info)
            case_dict["case_id"] = record.case_id
            case_dict["execute_record_id"] = record.id
            case_dict["execute_result"] = '' if not record.execute_result else record.execute_result
            case_dict["exception_info"] = '' if  not record.exception_info else record.exception_info
            case_dict["capture_screen"] = '' if not record.capture_screen else record.capture_screen
            case_dict["execute_start_time"] = record.execute_start_time
            case_dict["belong_module"] = case_info.belong_module.module_name
            case_dict["name"] = case_info.name
            case_dict["author"] = case_info.author
            case_dict["create_time"] = case_info.create_time
            if record.execute_result == "pass":
                success_num += 1
            else:
                fail_num += 1
            print("case_dict: %s" % case_dict)
            case_list.append(case_dict)

        print("case_list: %s" % case_list)
        case_account = len(case_list)
        return render(request, "case_result_level2.html", {'user': username, "cases": case_list, "caseaccounts": case_account, "successnumber": success_num, "failnumber": fail_num, "suiteid": suiteId})




# 用例步骤
@login_required
def case_result_detail(request):
    username = request.session.get('user', '')
    caseId = request.GET.get("caseid", '')
    execute_record_id =  request.GET.get("execute_record_id", "")

    if caseId:
        print("caseId: %s" % caseId)
        if execute_record_id: # 如果有execute_id，直接取caseexecuteresult中改execute_id的数据作为执行详情步骤信息
            print("execute_record_id: %s" % execute_record_id)
            case_execute_result_list = CaseExecuteResult.objects.filter(execute_record_id=execute_record_id).order_by('step_id')
            print("case_execute_result_list: %s" % case_execute_result_list)
            caseStepResultList = []
            for stepResult in case_execute_result_list:
                step_result_dict = {}
                step_result_dict["step_id"] = stepResult.step_id
                step_result_dict["step_desc"] = stepResult.step_desc
                step_result_dict["step_result"] = stepResult.result
                step_result_dict["create_time"] = stepResult.create_time
                step_result_dict["exception_info"] = '' if not stepResult.exception_info else stepResult.exception_info
                step_result_dict["capture_screen"] = '' if not stepResult.capture_screen else stepResult.capture_screen

                print("step_result_dict: %s" % step_result_dict)
                caseStepResultList.append(step_result_dict)
        else: # 如果没有execute_record_id，则用case_id找最新的执行记录
            # 先找到executerecord表中该用例id的最新执行主键id，然后通过该主键id到caseexeuteresult中找execute_record_id为该主键id的记录
            case_record_data = ExecuteRecord.objects.filter(case_id = caseId)
            print("case_record_data: %s" % case_record_data)
            case_record_id = max([record.id for record in ExecuteRecord.objects.filter(case_id = caseId)])
            print("case_record_id: %s" % case_record_id)
            case_execute_result_list = CaseExecuteResult.objects.filter(execute_record_id = case_record_id).order_by('step_id')
            print("case_execute_result_list: %s" % case_execute_result_list)
            caseStepResultList = []
            for stepResult in case_execute_result_list:
                step_result_dict = {}
                step_result_dict["step_id"] = stepResult.step_id
                step_result_dict["step_desc"] = stepResult.step_desc
                step_result_dict["step_result"] = stepResult.result
                step_result_dict["create_time"] = stepResult.create_time
                step_result_dict["exception_info"] = '' if not stepResult.exception_info else stepResult.exception_info
                step_result_dict["capture_screen"] = '' if not stepResult.capture_screen else stepResult.capture_screen

                print("step_result_dict: %s" % step_result_dict)
                caseStepResultList.append(step_result_dict)

        print("caseStepResultList: %s" % caseStepResultList)
        case_account = len(caseStepResultList)
        return render(request, "case_result_detail.html", {'user': username, "casesteps": caseStepResultList, "caseaccounts": case_account})



def exception_info(request):
    print("request.POST: %s" % request.POST)
    exception_info = request.GET.get("exceptionInfo", '')
    print("exception_info: %s" % exception_info)
    return render(request, "exception_info.html", {"exceptionInfo": exception_info})

def project_level_report(request):

    return render(request, "project_level_report.html")

def autotest_report(request):

    return render(request, "autotest_report.html")

def case_level_report(request):

    return render(request, "case_level_report.html")

def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error'})
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

def test(request):
    return render(request, 'atest.html')

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def project_manage(request):
    username = request.session.get('user', '')
    project_list = ProjectInfo.objects.all()
    return render(request, "project_manage.html", {'user': username, "projects": project_list})

def module_manage(request):
    if request.GET:
        projectId = request.GET.get('projectid', '')
        if projectId:
            print("projectId: %s" % projectId)
            username = request.session.get('user', '')
            module_list = ModuleInfo.objects.filter(belong_project__id=projectId)
            return render(request, "module_manage.html", {'user': username, "modules": module_list})

# def test(request):
#     # 传递参数并执行异步任务
#     id = request.GET.get('id', 1)
#     print("id: %s" % id)
#     info = dict(name='XIAXIAOXU', age=20, hireDate='2020-05-10')
#     updateData(id, info)
#     return HttpResponse("Change the data for id: %s successfully" % id)


# def runTestCase(request):
#     test_cases = TestCaseInfo.objects.all()
#     if request.method == 'POST':
#         getBaiDu.delay()
#     return render(request, 'testcase.html', locals())


def testList(request):

    return render(request, 'test_list.html')

def addCase(request):

    return render(request, 'add_case.html')


