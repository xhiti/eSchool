# Generated by Django 3.2.10 on 2021-12-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_gradevalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradevalue',
            name='value',
            field=models.IntegerField(),
        ),
    ]
