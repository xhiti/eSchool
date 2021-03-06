# Generated by Django 3.2.10 on 2022-01-08 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20220108_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradeclass',
            name='continuous_grade_p2',
        ),
        migrations.RemoveField(
            model_name='gradeclass',
            name='continuous_grade_p3',
        ),
        migrations.RemoveField(
            model_name='gradeclass',
            name='project_grade_p2',
        ),
        migrations.RemoveField(
            model_name='gradeclass',
            name='project_grade_p3',
        ),
        migrations.RemoveField(
            model_name='gradeclass',
            name='test_grade_p2',
        ),
        migrations.RemoveField(
            model_name='gradeclass',
            name='test_grade_p3',
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='continuous_grade_p1',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='project_grade_p1',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='gradeclass',
            name='test_grade_p1',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
