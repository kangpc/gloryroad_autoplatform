from django.contrib import admin

# Register your models here.
from autotest.models import ProjectInfo, ModuleInfo, TestCaseInfo, CaseStepInfo, KeyWord, TestSuiteInfo

admin.site.site_title = 'GloryroadPlatform'
admin.site.site_header = 'GloryroadPlatform'

@admin.register(ProjectInfo) # 把项目信息注册到Django admin后台并显示
class SetAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'responsible_name', 'test_user', 'dev_user', 'simple_desc', 'other_desc']


@admin.register(ModuleInfo) # 把模块管理注册到Django admin后台并显示
class ModelAdmin(admin.ModelAdmin):
    list_display = ['module_name', 'belong_project', 'test_user', 'test_user', 'simple_desc', 'other_desc']


@admin.register(CaseStepInfo) # 把步骤信息注册到Django admin后台并显示
class CaseStepInfoAdmin(admin.ModelAdmin):
    list_display = [ 'case', 'teststep', 'testobjname', 'optmethod', 'findmethod', 'evelement', 'testdata',  'create_time']


@admin.register(TestCaseInfo) # 把用例信息注册到Django admin后台并显示
class TestCaseInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'belong_project', 'belong_module', 'author', 'create_time', 'update_time']

@admin.register(KeyWord) # 把关键字信息注册到Django admin后台并显示
class TestCaseInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'keyword_name', 'params', 'kw_description', 'create_time', 'update_time']


@admin.register(TestSuiteInfo) # 把测试集信息注册到Django admin后台并显示
class TestCaseInfoAdmin(admin.ModelAdmin):
    # 显示多对多字段
    # 定义一个方法，遍历suite的authors，然后用列表返回
    def list_all_cases(self, obj):
        return [[a.id,a.name] for a in obj.cases.all()]

    # list_display = ['title', 'publisher', 'show_all_author']  # 用刚刚定义的方法的返回值替换cases的值
    list_display = ['id', 'suite_name', 'list_all_cases', 'belong_project', 'author', 'create_time', 'update_time']