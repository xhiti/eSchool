# Generated by Django 3.2.10 on 2021-12-19 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('klasat', '0004_remove_class_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='subject',
        ),
    ]
