# Generated by Django 3.2.10 on 2021-12-19 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_parent_studentclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20)),
                ('grade', models.IntegerField(max_length=20)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('grade_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gradetype')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.period')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.studentclass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20)),
                ('grade', models.IntegerField(max_length=20)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('grade_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gradetype')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.period')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.subject')),
            ],
        ),
    ]
