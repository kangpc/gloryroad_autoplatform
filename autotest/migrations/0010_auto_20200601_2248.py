# Generated by Django 2.2.1 on 2020-06-01 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0009_auto_20200601_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseexecuteresult',
            name='execute_end_time',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='执行结束时间'),
        ),
        migrations.AlterField(
            model_name='caseexecuteresult',
            name='execute_start_time',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='执行开始时间'),
        ),
        migrations.AlterField(
            model_name='caseexecuteresult',
            name='result',
            field=models.CharField(max_length=100, null=True, verbose_name='执行结果'),
        ),
    ]
