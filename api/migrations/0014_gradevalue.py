# Generated by Django 3.2.10 on 2021-12-20 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_parent_nid'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20)),
                ('value', models.IntegerField(max_length=20)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
