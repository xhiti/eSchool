from django.contrib import admin
from .models import Class


# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'description', 'is_active', 'created_date', )
    # prepopulated_fields = {'slug': ('title', )}

admin.site.register(Class, ClassAdmin)
