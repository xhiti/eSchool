from django.contrib import admin
from .models import Subject


# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'description', 'index', 'is_active', 'created_date', )

admin.site.register(Subject, SubjectAdmin)
