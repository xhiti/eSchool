# Generated by Django 3.2.10 on 2021-12-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_grade_gradeclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
