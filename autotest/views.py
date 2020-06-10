#encoding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os
from concurrent.futures import ThreadPoolExecutor
from django.contrib import auth
from .models import TestCaseInfo, ProjectInfo, CaseStepInfo, CaseExecuteResult, ExecuteRecord
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
        case_id_list = request.POST.getlist('testcase')
        if case_id_list:
            print("case_id_list: ", case_id_list)
            # 获取测试用例
            runTestCase.delay(case_id_list)
            # with ThreadPoolExecutor(3) as executor:
            #     executor.map(runTestCase, case_id_list)

            # runTestCase(case_id_list)

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
    testcase = TestCaseInfo.objects.get(id=caseid)
    casestep_list = CaseStepInfo.objects.all().order_by('teststep')
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


def case_result_level_one(request):

    return render(request, "case_result_level1.html")


"""
    execute_id = models.AutoField(primary_key=True)
    1 case_id = models.CharField(max_length=100, null=False)
    status = models.IntegerField(null=True, help_text="0：表示未执行，1：表示已执行")
    1 execute_result = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    1 exception_info= models.CharField(max_length=500, blank=True, null=True)
    1 capture_screen = models.CharField(max_length=500, blank=True, null=True)
    1 execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
    execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True)

     <td>{{ webcase.id }}</td>
     单独<td>{{ webcase.belong_module.module_name }}</td>
     单独<td>{{ webcase.name }}</td>
     单独<td>{{ webcase.author }}</td>
     单独<td>{{ webcase.create_time }}</td>
     <td>{{ webcase.execute_time }}</td>
     <td>{{ webcase.execute_result }}</td>
     <td>{{ webcase.exception_info }}</td>
     <td>{{ webcase.capture_screen }}</td>
"""
# 用例步骤
@login_required
def case_result_level_two(request):
    username = request.session.get('user', '')
    runStatus = request.GET.get("alreadyrun", '')
    # runStatus: 0: 待执行，1： 已执行
    if runStatus:
        print("runStatus: %s" % runStatus)
        case_recored_list = ExecuteRecord.objects.filter(status = 1).order_by('create_time') if (str(runStatus) == '1') else ExecuteRecord.objects.filter(status=0)
        print("case_recored_list: ", case_recored_list)
        case_list = []
        for record in case_recored_list:
            case_dict = {}
            case_info = TestCaseInfo.objects.filter(id = record.case_id).first()
            print("case_info: ,", case_info)
            case_dict["case_id"] = record.case_id
            case_dict["execute_result"] = '' if not record.execute_result else record.execute_result
            case_dict["exception_info"] = '' if  not record.exception_info else record.exception_info
            case_dict["capture_screen"] = '' if not record.capture_screen else record.capture_screen
            case_dict["execute_start_time"] = record.execute_start_time
            case_dict["belong_module"] = case_info.belong_module.module_name
            case_dict["name"] = case_info.name
            case_dict["author"] = case_info.author
            case_dict["create_time"] = case_info.create_time
            print("case_dict: %s" % case_dict)
            case_list.append(case_dict)

        print("case_list: %s" % case_list)
        case_account = len(case_list)
        return render(request, "case_result_level2.html", {'user': username, "cases": case_list, "caseaccounts": case_account})

def exception_info(request):
    exception_info = request.GET.get("exceptionInfo", '')
    return render(request, "exception_info.html", {"exceptionInfo": exception_info})

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


