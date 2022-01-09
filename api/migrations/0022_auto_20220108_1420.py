# Generated by Django 3.2.10 on 2022-01-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_gradeclass_classs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradeclass',
            name='first_period_continuous_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='first_period_project_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='first_period_test_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='second_period_continuous_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='second_period_project_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='second_period_test_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='third_period_continuous_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='third_period_project_grade',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='third_period_test_grade',
            field=models.IntegerField(blank=True),
        ),
    ]