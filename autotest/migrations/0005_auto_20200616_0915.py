# Generated by Django 2.2.13 on 2020-06-16 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0004_testsuiteinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='executerecord',
            name='suite_id',
            field=models.IntegerField(blank=True, help_text='测试集id，通过提交suite执行时产生，否则为空，用于查找该用例集的历史结果', null=True),
        ),
        migrations.AlterField(
            model_name='moduleinfo',
            name='belong_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.ProjectInfo', verbose_name='所属项目'),
        ),
        migrations.AlterField(
            model_name='moduleinfo',
            name='other_desc',
            field=models.CharField(max_length=100, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='projectinfo',
            name='other_desc',
            field=models.CharField(max_length=100, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='projectinfo',
            name='responsible_name',
            field=models.CharField(max_length=20, verbose_name='项目负责人'),
        ),
    ]