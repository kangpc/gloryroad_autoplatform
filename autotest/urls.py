
from django.urls import path
from .views import *


urlpatterns = [
    # 搜索引擎
    # path('', test, name='autotest'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('project_manage/', project_manage, name='project_manage'),
    path('module_manage/', module_manage, name='module_manage'),
    path('suite_manage/', suite_manage, name='suite_manage'),
    path('case_manage/', case_manage, name='case_manage'),
    path('casestep_manage/', casestep_manage, name='casestep_manage'),
    path('case_result_level_one/', case_result_level_one, name='case_result_level_one'),
    path('case_result_level_two/', case_result_level_two, name='case_result_level_two'),
    path('case_result_detail/', case_result_detail, name='case_result_detail'),

    path('exception_info/', exception_info, name='exception_info'),
    path('autotest_report/', autotest_report, name='autotest_report'),
    path('project_level_report/', project_level_report, name='project_level_report'),
    path('case_level_report/', case_level_report, name='case_level_report'),
    path('casesearch/', caseSearch, name='caseSearch'),
    path('stepsearch/', caseStepSearch, name='caseStepSearch'),
    # path('submit/', caseSubmit, name='caseSubmit'),
    # path('set_manage/', setviews.set_manage, name='set_manage'),
    # path('user/', setviews.set_user, name='set_user'),
    # path('caselist/', caseList, name='caseList'),
]