# Generated by Django 3.2.10 on 2022-01-08 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klasat', '0005_remove_class_subject'),
        ('api', '0020_auto_20220108_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeclass',
            name='classs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='klasat.class'),
            preserve_default=False,
        ),
    ]
