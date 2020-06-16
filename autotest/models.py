from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProjectInfo(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    responsible_name = models.CharField('项目负责人', max_length=20, null=False)
    test_user = models.CharField('测试人员', max_length=100, null=False)
    dev_user = models.CharField('开发人员', max_length=100, null=False)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    other_desc = models.CharField('备注', max_length=100, null=True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = '项目信息表'
        verbose_name_plural = '项目信息表'


class ModuleInfo(models.Model):
    id = models.AutoField(primary_key=True)
    module_name = models.CharField('模块名称', max_length=50, null=False)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, verbose_name='所属项目')
    test_user = models.CharField('测试负责人', max_length=50, null=False)
    simple_desc = models.CharField('简要描述', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    other_desc = models.CharField('备注', max_length=100, null=True)

    def __str__(self):
        return self.module_name

    class Meta:
        verbose_name = '模块信息表'
        verbose_name_plural = '模块信息表'


class TestCaseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('用例名称', max_length=50, null=False)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.SET_NULL, verbose_name='所属项目',blank=True, null=True)
    belong_module = models.ForeignKey(ModuleInfo, on_delete=models.CASCADE, verbose_name='所属模块')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='编写人员',blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例表'
        verbose_name_plural = '用例表'


class TestSuiteInfo(models.Model):
    id = models.AutoField(primary_key=True)
    suite_name = models.CharField('测试集名称', max_length=200, null=False)
    include_cases = models.CharField('包含用例id列表', max_length=200, null=False)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.SET_NULL, verbose_name='所属项目',blank=True, null=True)
    belong_module = models.ForeignKey(ModuleInfo, on_delete=models.CASCADE, verbose_name='所属模块')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='编写人员',blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.suite_name

    class Meta:
        verbose_name = '用例集表'
        verbose_name_plural = '用例集表'

class KeyWord(models.Model):
    id = models.AutoField(primary_key=True)
    keyword_name = models.CharField(max_length=300, null=False)
    params = models.CharField(max_length=300, null=True)
    kw_description = models.TextField(null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.keyword_name

    class Meta:
        verbose_name = "关键字表"
        verbose_name_plural = '关键字表'

class CaseStepInfo(models.Model):
    id = models.AutoField(primary_key=True)
    case = models.ForeignKey(TestCaseInfo, on_delete=models.CASCADE, verbose_name='用例名称') # 步骤信息对应于用例信息，级联关系
    teststep = models.CharField('测试步聚序号', max_length=200)  # 测试步聚
    testobjname = models.CharField('测试步骤描述', max_length=200, blank=True, null=True)  # 测试对象名称描述
    optmethod = models.ForeignKey(KeyWord, on_delete=models.CASCADE, blank=True, null=True, verbose_name='操作关键字')  # 操作方法
    findmethod = models.CharField('定位方式', max_length=200, blank=True, null=True)  # 定位方式
    evelement = models.CharField('控件表达式', max_length=800, blank=True, null=True)  # 控件元素
    testdata = models.CharField('测试数据', max_length=200, blank=True, null=True)  # 测试数据
    testresult = models.BooleanField('测试结果', blank=True, null=True)  # 测试结果
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return self.teststep

    class Meta:
        verbose_name = '用例步骤表'
        verbose_name_plural = '用例步骤表'


class ExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    execute_id =  models.IntegerField(null=True, help_text="执行id，每次批量提交的用例的execute_id是一样的，用例收集报告信息")
    execute_user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='执行人员', blank=True, null=True)
    case = models.ForeignKey(TestCaseInfo, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用例信息') # 执行记录对应于用例信息，级联关系
    status = models.IntegerField(null=True, help_text="0：表示未执行，1：表示已执行")
    execute_result = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    exception_info= models.CharField(max_length=500, blank=True, null=True) # 可以不要了
    capture_screen = models.CharField(max_length=500, blank=True, null=True) # 可以不要了
    execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
    execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "运行记录表"
        verbose_name_plural = '运行记录表'

class CaseExecuteResult(models.Model):
    id = models.AutoField(primary_key=True)
    execute_record = models.ForeignKey(ExecuteRecord, on_delete=models.CASCADE, blank=True, null=True, verbose_name='执行记录')
    step_id = models.CharField(max_length=100, null=False)
    step_desc = models.CharField(max_length=300, null=False)
    result = models.CharField('执行结果',max_length=100, blank=True, null=True)
    exception_info = models.CharField(max_length=500, blank=True, null=True)
    capture_screen = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "用例结果表"
        verbose_name_plural = '用例结果表'

class TestReports(models.Model):
    id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=40, null=False)
    start_at = models.CharField(max_length=40, null=True)
    status = models.BooleanField()
    testsRun = models.IntegerField()
    successes = models.IntegerField()
    reports = models.TextField()

    def __str__(self):
        return self.report_name

    class Meta:
        verbose_name = "测试报告表"
        verbose_name_plural = '测试报告表'
