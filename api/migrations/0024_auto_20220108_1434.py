# Generated by Django 3.2.10 on 2022-01-08 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_rename_third_period_test_grade_gradeclass_test_grade_p3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gradeclass',
            old_name='first_period_continuous_grade',
            new_name='continuous_grade_p1',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='first_period_project_grade',
            new_name='continuous_grade_p2',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='first_period_test_grade',
            new_name='continuous_grade_p3',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='second_period_continuous_grade',
            new_name='project_grade_p1',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='second_period_project_grade',
            new_name='project_grade_p2',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='second_period_test_grade',
            new_name='project_grade_p3',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='third_period_continuous_grade',
            new_name='test_grade_p1',
        ),
        migrations.RenameField(
            model_name='gradeclass',
            old_name='third_period_project_grade',
            new_name='test_grade_p2',
        ),
    ]
