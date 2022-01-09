from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Class
from api.models import Subject, StudentClass


# Create your views here.
def klasat(request):
    classes = Class.objects.all().filter(is_active=True).order_by('code')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    no_student_8_a = StudentClass.objects.all().filter(is_active=True, class_id=1).count()
    no_student_8_d = StudentClass.objects.all().filter(is_active=True, class_id=3).count()
    no_student_8_e = StudentClass.objects.all().filter(is_active=True, class_id=4).count()
    no_student_9_e = StudentClass.objects.all().filter(is_active=True, class_id=5).count()

    students = [
        no_student_8_a, no_student_8_d, no_student_8_e, no_student_9_e
    ]

    context = {
        'classes': classes,
        'subjects': subjects,
        'students': students
    }
    return render(request, 'classes.html', context)


def shto_klase(request):
    if request.method == "POST":
        title = request.POST['title']
        if title is None or title == "":
            messages.error(request, 'Emërtimi i klasës nuk mund të jetë bosh!')
        else:
            title = str(title).capitalize()
            code = str(title).replace("KLASA", " ")
            code = str(code).replace(" ", "-")
            code = "KLGJ-" + code.upper() + ""
            existing_classes = Class.objects.all().filter(code=code, is_active=True).count()

        description = request.POST['description']
        if description is None or description == "":
            messages.error(request, 'Përshkrimi i klasës nuk mund të jetë bosh!')
        else:
            description = str(description).capitalize()

        subject = Subject.objects.filter(code='AZ-GJUHË-SHQIPE-8').first()

        if existing_classes > 0:
            messages.error(request, 'Ekziston një tjetër klasë me këtë emërtim në sistem!')
        else:
            Class.objects.create(code=code, title=title, description=description, subject=subject)
            messages.success(request, 'Klasa u shtua me sukses!')
            return redirect('classes')

    return render(request, 'add-class.html')


def fshi_klase(request, pk):
    Class.objects.filter(id=pk).update(is_active=False, is_deleted=True)
    messages.success(request, 'Klasa u fshi me sukses!')
    return redirect('classes')


def modifiko_klase(request, pk):
    class_details = Class.objects.filter(id=pk, is_active=True).first()
    context = {
        'class_details': class_details
    }

    if request.method == "POST":
        title = request.POST['title']
        if title is None or title == "":
            messages.error(request, 'Emërtimi i klasës nuk mund të jetë bosh!')
        else:
            title = str(title).capitalize()
            code = str(title).replace("KLASA", " ")
            code = str(code).replace(" ", "-")
            code = "KLGJ-" + code.upper() + ""
            existing_classes = Class.objects.all().filter(code=code, is_active=True).exclude(id=pk).count()

        description = request.POST['description']
        if description is None or description == "":
            messages.error(request, 'Përshkrimi i klasës nuk mund të jetë bosh!')
        else:
            description = str(description).capitalize()

        subject = Subject.objects.filter(code='AZ-GJUHË-SHQIPE-8').first()

        if existing_classes > 0:
            messages.error(request, 'Ekziston një tjetër klasë me këtë emërtim në sistem!')
        else:
            Class.objects.filter(id=pk).update(code=code, title=title, description=description, subject=subject)
            messages.success(request, 'Klasa u modifikua me sukses!')
            return redirect('classes')
    return render(request, 'edit-class.html', context)
