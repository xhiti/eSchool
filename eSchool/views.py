from django.shortcuts import render
from klasat.models import Class
from api.models import Subject, StudentClass


def index(request):
    no_classes = Class.objects.all().filter(is_active=True).count()
    no_subjects = Subject.objects.all().filter(is_active=True).count()
    no_students = StudentClass.objects.all().filter(is_active=True).count()
    context = {
        'no_classes': no_classes,
        'no_subjects': no_subjects,
        'no_students': no_students
    }
    return render(request, 'index.html', context)


def error(request):
    return render(request, 'error-404.html')
