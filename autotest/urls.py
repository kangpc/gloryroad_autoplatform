
from django.urls import path
from .views import *


urlpatterns = [

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
    path('base/', base, name='base'),
    path('test/', test, name='test'),
    # 目前先不用
    path('autotest_report/', autotest_report, name='autotest_report'),
    path('project_level_report/', project_level_report, name='project_level_report'),
    path('case_level_report/', case_level_report, name='case_level_report'),
    path('casesearch/', caseSearch, name='caseSearch'),
    path('stepsearch/', caseStepSearch, name='caseStepSearch'),

]