# Generated by Django 2.2.13 on 2020-06-23 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword_name', models.CharField(max_length=300)),
                ('params', models.CharField(max_length=300, null=True)),
                ('kw_description', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '关键字表',
                'verbose_name_plural': '关键字表',
            },
        ),
        migrations.CreateModel(
            name='ModuleInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('module_name', models.CharField(max_length=50, verbose_name='模块名称')),
                ('test_user', models.CharField(max_length=50, verbose_name='测试负责人')),
                ('simple_desc', models.CharField(max_length=100, null=True, verbose_name='简要描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('other_desc', models.CharField(max_length=100, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '模块信息表',
                'verbose_name_plural': '模块信息表',
            },
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50, unique=True, verbose_name='项目名称')),
                ('responsible_name', models.CharField(max_length=20, verbose_name='项目负责人')),
                ('test_user', models.CharField(max_length=100, verbose_name='测试人员')),
                ('dev_user', models.CharField(max_length=100, verbose_name='开发人员')),
                ('simple_desc', models.CharField(max_length=100, null=True, verbose_name='简要描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('other_desc', models.CharField(max_length=100, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '项目信息表',
                'verbose_name_plural': '项目信息表',
            },
        ),
        migrations.CreateModel(
            name='TestCaseInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='用例名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='编写人员')),
                ('belong_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.ModuleInfo', verbose_name='所属模块')),
                ('belong_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autotest.ProjectInfo', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '用例表',
                'verbose_name_plural': '用例表',
            },
        ),
        migrations.CreateModel(
            name='TestReports',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report_name', models.CharField(max_length=40)),
                ('start_at', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField()),
                ('testsRun', models.IntegerField()),
                ('successes', models.IntegerField()),
                ('reports', models.TextField()),
            ],
            options={
                'verbose_name': '测试报告表',
                'verbose_name_plural': '测试报告表',
            },
        ),
        migrations.CreateModel(
            name='TestSuiteInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('suite_name', models.CharField(max_length=200, verbose_name='测试集名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='编写人员')),
                ('belong_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.ModuleInfo', verbose_name='所属模块')),
                ('belong_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='autotest.ProjectInfo', verbose_name='所属项目')),
                ('cases', models.ManyToManyField(to='autotest.TestCaseInfo', verbose_name='包含用例')),
            ],
            options={
                'verbose_name': '用例集表',
                'verbose_name_plural': '用例集表',
            },
        ),
        migrations.AddField(
            model_name='moduleinfo',
            name='belong_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.ProjectInfo', verbose_name='所属项目'),
        ),
        migrations.CreateModel(
            name='ExecuteRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('execute_id', models.IntegerField(help_text='执行id，每次批量提交的用例的execute_id是一样的，用例收集报告信息', null=True)),
                ('suite_id', models.IntegerField(blank=True, help_text='测试集id，通过提交suite执行时产生，否则为空，用于查找该用例集的历史结果', null=True)),
                ('status', models.IntegerField(help_text='0：表示未执行，1：表示已执行', null=True)),
                ('execute_result', models.CharField(max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('exception_info', models.CharField(blank=True, max_length=500, null=True)),
                ('capture_screen', models.CharField(blank=True, max_length=500, null=True)),
                ('execute_start_time', models.CharField(blank=True, max_length=300, null=True, verbose_name='执行开始时间')),
                ('execute_end_time', models.CharField(blank=True, max_length=300, null=True, verbose_name='执行结束时间')),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autotest.TestCaseInfo', verbose_name='用例信息')),
                ('execute_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='执行人员')),
            ],
            options={
                'verbose_name': '运行记录表',
                'verbose_name_plural': '运行记录表',
            },
        ),
        migrations.CreateModel(
            name='CaseStepInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('teststep', models.CharField(max_length=200, verbose_name='测试步聚序号')),
                ('testobjname', models.CharField(blank=True, max_length=200, null=True, verbose_name='测试步骤描述')),
                ('findmethod', models.CharField(blank=True, max_length=200, null=True, verbose_name='定位方式')),
                ('evelement', models.CharField(blank=True, max_length=800, null=True, verbose_name='控件表达式')),
                ('testdata', models.CharField(blank=True, max_length=200, null=True, verbose_name='测试数据')),
                ('testresult', models.BooleanField(blank=True, null=True, verbose_name='测试结果')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.TestCaseInfo', verbose_name='用例名称')),
                ('optmethod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autotest.KeyWord', verbose_name='操作关键字')),
            ],
            options={
                'verbose_name': '用例步骤表',
                'verbose_name_plural': '用例步骤表',
            },
        ),
        migrations.CreateModel(
            name='CaseExecuteResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('step_id', models.CharField(max_length=100)),
                ('step_desc', models.CharField(max_length=300)),
                ('result', models.CharField(blank=True, max_length=100, null=True, verbose_name='执行结果')),
                ('exception_info', models.CharField(blank=True, max_length=500, null=True)),
                ('capture_screen', models.CharField(blank=True, max_length=500, null=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('execute_record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autotest.ExecuteRecord', verbose_name='执行记录')),
            ],
            options={
                'verbose_name': '用例结果表',
                'verbose_name_plural': '用例结果表',
            },
        ),
    ]
