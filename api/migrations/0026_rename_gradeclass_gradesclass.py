# Generated by Django 3.2.10 on 2022-01-08 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('klasat', '0005_remove_class_subject'),
        ('api', '0025_auto_20220108_1443'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GradeClass',
            new_name='GradesClass',
        ),
    ]
