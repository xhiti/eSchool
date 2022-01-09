from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from api.helpers.mainClassStudentDetails import PrintStudentDetails
from api.helpers.mainClassParentsList import PrintParentDetails
from api.helpers.mainClassStatistics import PrintStatistics
from api.helpers.class8AStatistics import PrintStatistics8A
from api.helpers.class8DStatistics import PrintStatistics8D
from api.helpers.class8EStatistics import PrintStatistics8E
from api.helpers.class9EStatistics import PrintStatistics9E
from .models import Subject, Student, Period, GradeType, Parent, Grade, GradeClass, StudentClass, GradeValue
from klasat.models import Class


# Create your views here.
def lendet(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    context = {
        'subjects': subjects
    }
    return render(request, 'subjects.html', context)


def shto_lende(request):
    if request.method == "POST":
        title = request.POST['title']

        if title is None or title == "":
            messages.error(request, 'Emërtimi i lëndës nuk mund të jetë bosh!')
        else:
            title = str(title).capitalize()
            initials = title[0:3]
            initials = str(initials).upper()
            code = str(title).replace(" ", "-")
            code = "AZ-" + code.upper() + "-8"
            existing_subjects = Subject.objects.all().filter(code=code, is_active=True).count()

        description = request.POST['description']
        if description is None or description == "":
            messages.error(request, 'Përshkrimi i lëndës nuk mund të jetë bosh!')
        else:
            description = str(description).capitalize()

        index = request.POST['index']
        if index is None or index == "":
            messages.error(request, 'Index-i i lëndës nuk mund të jetë bosh!')
        else:
            index = str(index).capitalize()
            exisiting_index = Subject.objects.all().filter(index=index, is_active=True).count()

        if existing_subjects > 0 or exisiting_index > 0:
            messages.error(request, 'Ekziston një tjetër lëndë me këtë emërtim/index në sistem!')
        else:
            Subject.objects.create(code=code, title=title, initials=initials, description=description, index=index)
            messages.success(request, 'Lënda u shtua me sukses!')
            return redirect('subjects')
    return render(request, 'add-subject.html')


def fshi_lende(request, code):
    Subject.objects.filter(code=code).update(is_active=False, is_deleted=True)
    messages.success(request, 'Lënda u fshi me sukses!')
    return redirect('subjects')


def modifiko_lende(request, code):
    subject_details = Subject.objects.filter(code=code, is_active=True).first()
    context = {
        'subject_details': subject_details
    }

    if request.method == "POST":
        title = request.POST['title']
        if title is None or title == "":
            messages.error(request, 'Emërtimi i lëndës nuk mund të jetë bosh!')
        else:
            title = str(title).capitalize()
            initials = title[0:3]
            initials = str(initials).upper()
            new_code = str(title).replace(" ", "-")
            new_code = "AZ-" + new_code.upper() + "-8"
            existing_subjects = Subject.objects.all().filter(code=new_code, is_active=True).exclude(code=code).count()

        description = request.POST['description']
        if description is None or description == "":
            messages.error(request, 'Përshkrimi i lëndës nuk mund të jetë bosh!')
        else:
            description = str(description).capitalize()

        index = request.POST['index']
        if index is None or index == "":
            messages.error(request, 'Index-i i lëndës nuk mund të jetë bosh!')
        else:
            index = str(index).capitalize()
            exisiting_index = Subject.objects.all().filter(index=index, is_active=True).exclude(code=code).count()

        if existing_subjects > 0 or exisiting_index > 0:
            messages.error(request, 'Ekziston një tjetër lëndë me këtë emërtim/index në sistem!')
        else:
            Subject.objects.filter(code=code).update(code=new_code, title=title, initials=initials, description=description, index=index)
            messages.success(request, 'Lënda u modifikua me sukses!')
            return redirect('subjects')
    return render(request, 'edit-subject.html', context)


def nxenesit(request):
    students = Student.objects.all().filter(is_active=True).order_by('name')
    context = {
        'students': students
    }
    return render(request, 'students.html', context)


def shto_nxenes(request):
    if request.method == "POST":
        code = ""
        existing_students = 0
        exisiting_nid = 0
        exisiting_amze_number = 0

        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')
        else:
            name = str(name).capitalize()
            existing_students = Student.objects.all().filter(code=code, is_active=True).count()

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')
        else:
            surname = str(surname).capitalize()

        code = str(name).replace(" ", "-") + "-" + str(surname).replace(" ", "-")
        code = "AZ-" + code.upper() + "-8-D"

        if code == " " or code is None:
            messages.error(request, 'Një gabim ndodhi gjatë regjsitrimit të nxënësit!')
        else:
            code = code

        father_name = request.POST['father_name']
        if father_name is None or father_name == "":
            messages.error(request, 'Atësia e nxënësit nuk mund të jetë bosh!')
        else:
            father_name = str(father_name).capitalize()

        birth_place = request.POST['birth_place']
        if birth_place is None or birth_place == "":
            messages.error(request, 'Vendlindja e nxënësit nuk mund të jetë bosh!')
        else:
            birth_place = str(birth_place).capitalize()

        birth_date = request.POST['birth_date']
        if birth_date is None or birth_date == "":
            messages.error(request, 'Datëlindja e nxënësit nuk mund të jetë bosh!')
        else:
            birth_date = birth_date

        sex = request.POST['gender']
        if sex is None or sex == "":
            messages.error(request, 'Gjinia e nxënësit nuk mund të jetë bosh!')
        else:
            sex = sex

        nid = request.POST['nid']
        if nid is None or nid == "":
            messages.error(request, 'NID-i i nxënësit nuk mund të jetë bosh!')
        else:
            nid = str(nid).upper()
            exisiting_nid = Student.objects.all().filter(nid=nid, is_active=True).count()

        amze_number = request.POST['amze_number']
        if amze_number is None or amze_number == "":
            messages.error(request, 'Numri i amzës i nxënësit nuk mund të jetë bosh!')
        else:
            amze_number = str(amze_number).upper()
            exisiting_amze_number = Student.objects.all().filter(amze_number=amze_number, is_active=True).count()

        class_code = 'KLGJ-KLASA-8-D'
        class_id = Class.objects.all().filter(code=class_code).first()

        if existing_students > 0 or exisiting_nid > 0 or exisiting_amze_number > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këtë emër/NID në sistem!')
        else:
            Student.objects.create(
                code=code,
                name=name,
                surname=surname,
                father_name=father_name,
                nid=nid,
                birth_place=birth_place,
                birth_date=birth_date,
                sex=sex,
                class_id=class_id,
                amze_number=amze_number
            )
            messages.success(request, 'Nxënësi u shtua me sukses!')
            return redirect('students')
    return render(request, 'add-student.html')


def fshi_nxenes(request, code):
    Student.objects.filter(code=code).update(is_active=False, is_deleted=True)
    messages.success(request, 'Nxënësi u fshi me sukses!')
    return redirect('students')


def info_nxenes(request, code):
    current_student = Student.objects.filter(code=code, is_active=True).first()
    periods = Period.objects.all().order_by('index')
    print("Current Student: " + str(current_student))
    context = {
        'current_student': current_student,
        'periods': periods
    }
    return render(request, 'student-details.html', context)


def printo_nxenes(request, code):
    Student.objects.filter(code=code).first()
    return redirect('students')


def modifiko_nxenes(request, code):
    student_details = Student.objects.filter(code=code, is_active=True).first()

    context = {
        'student_details': student_details
    }

    if request.method == "POST":
        new_code = ""
        new_amze_number = ""

        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')
        else:
            name = str(name).capitalize()
            existing_students = Student.objects.all().filter(code=code, is_active=True).exclude(code=code).count()

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')
        else:
            surname = str(surname).capitalize()

        new_code = str(name).replace(" ", "-") + "-" + str(surname).replace(" ", "-")
        new_code = "AZ-" + new_code.upper() + "-8-D"

        if new_code == " " or new_code is None:
            messages.error(request, 'Një gabim ndodhi gjatë modifikimit të nxënësit!')
        else:
            new_code = new_code

        father_name = request.POST['father_name']
        if father_name is None or father_name == "":
            messages.error(request, 'Atësia e nxënësit nuk mund të jetë bosh!')
        else:
            father_name = str(father_name).capitalize()

        birth_place = request.POST['birth_place']
        if birth_place is None or birth_place == "":
            messages.error(request, 'Vendlindja e nxënësit nuk mund të jetë bosh!')
        else:
            birth_place = str(birth_place).capitalize()

        sex = request.POST['gender']
        if sex is None or sex == "":
            messages.error(request, 'Gjinia e nxënësit nuk mund të jetë bosh!')
        else:
            sex = sex

        nid = request.POST['nid']
        if nid is None or nid == "":
            messages.error(request, 'NID-i i nxënësit nuk mund të jetë bosh!')
        else:
            nid = str(nid).upper()
            exisiting_nid = Student.objects.all().filter(nid=nid, is_active=True).exclude(code=code).count()

        new_amze_number = request.POST['amze_number']
        if new_amze_number is None or new_amze_number == "":
            messages.error(request, 'Numri i amzës i nxënësit nuk mund të jetë bosh!')
        else:
            new_amze_number = str(new_amze_number).upper()
            exisiting_amze_number = Student.objects.all().filter(amze_number=new_amze_number, is_active=True).exclude(code=code).count()

        class_code = 'KLGJ-KLASA-8-D'
        class_id = Class.objects.all().filter(code=class_code).first()

        if existing_students > 0 or exisiting_nid > 0 or exisiting_amze_number > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këtë emër/NID në sistem!')
        else:
            Student.objects.filter(code=code).update(
                code=new_code,
                name=name,
                surname=surname,
                father_name=father_name,
                nid=nid,
                birth_place=birth_place,
                sex=sex,
                class_id=class_id,
                amze_number=new_amze_number
            )
            messages.success(request, 'Nxënësi u modifikua me sukses!')
            return redirect('students')

    return render(request, 'edit-student.html', context)


def prinderit(request):
    parents = Parent.objects.all().filter(is_active=True).order_by('name')
    context = {
        'parents': parents
    }
    return render(request, 'parents.html', context)


def shto_prind(request):
    students = Student.objects.all().filter(is_active=True).order_by('name')

    context = {
        'students': students
    }

    if request.method == "POST":

        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i prindërit nuk mund të jetë bosh!')
        else:
            name = str(name).capitalize()

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i prindërit nuk mund të jetë bosh!')
        else:
            surname = str(surname).capitalize()

        student = request.POST['student']
        if student is None or student == "":
            messages.error(request, 'Nxënësi nuk mund të jetë bosh!')
        else:
            student = Student.objects.all().filter(code=student).first()
            student_id = student.id

        nid = request.POST['nid']
        if nid is None or nid == "":
            messages.error(request, 'NID i prindërit nuk mund të jetë bosh!')
        else:
            nid = str(nid).upper()

        phone_number = request.POST['phone_number']
        if phone_number is None or phone_number == "":
            messages.error(request, 'Nr. i celularit i prindërit nuk mund të jetë bosh!')
        else:
            phone_number = str(phone_number)

        code = str(name).replace(" ", "-") + "-" + str(surname).replace(" ", "-") + "-" + str(student.name).replace(" ", "-")
        code = "AZ-" + code.upper() + "-8-D"
        Parent.objects.create(
            code=code,
            name=name,
            surname=surname,
            student_id=student_id,
            nid=nid,
            phone_number=phone_number
        )
        messages.success(request, 'Lënda u shtua me sukses!')
        return redirect('parents')
    return render(request, 'add-parents.html', context)


def modifiko_prind(request, code):
    parent_details = Parent.objects.all().filter(code=code, is_active=True).first()
    students = Student.objects.all().filter(is_active=True).order_by('name')
    current_student = Student.objects.all().filter(id=parent_details.student_id).first()
    current_student_code = current_student.code

    context = {
        'students': students,
        'parent_details': parent_details,
        'current_student_code': current_student_code
    }

    if request.method == "POST":

        new_name = request.POST['name']
        if new_name is None or new_name == "":
            messages.error(request, 'Emri i prindërit nuk mund të jetë bosh!')
        else:
            new_name = str(new_name).capitalize()

        new_surname = request.POST['surname']
        if new_surname is None or new_surname == "":
            messages.error(request, 'Mbiemri i prindërit nuk mund të jetë bosh!')
        else:
            new_surname = str(new_surname).capitalize()

        nid = request.POST['nid']
        if nid is None or nid == "":
            messages.error(request, 'NID i prindërit nuk mund të jetë bosh!')
        else:
            nid = str(nid).upper()

        phone_number = request.POST['phone_number']
        if phone_number is None or phone_number == "":
            messages.error(request, 'Nr. i celularit i prindërit nuk mund të jetë bosh!')
        else:
            phone_number = str(phone_number)

        new_code = str(new_name).replace(" ", "-") + "-" + str(new_surname).replace(" ", "-") + "-" + str(current_student.name).replace(" ", "-")
        new_code = "AZ-" + new_code.upper() + "-8-D"
        Parent.objects.filter(code=code).update(
            code=new_code,
            name=new_name,
            surname=new_surname,
            nid=nid,
            phone_number=phone_number
        )
        messages.success(request, 'Prindi u modifikua me sukses!')
        return redirect('parents')

    return render(request, 'edit-parent.html', context)


def fshi_prind(request, code):
    Parent.objects.filter(code=code).update(is_active=False, is_deleted=True)
    messages.success(request, 'Prindi u fshi me sukses!')
    return redirect('parents')


def shto_note(request):
    students = Student.objects.all().filter(is_active=True).order_by('name')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    grade_types = GradeType.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().order_by('index')
    grade_values = GradeValue.objects.all().order_by('id')

    context = {
        'students': students,
        'subjects': subjects,
        'grade_types': grade_types,
        'grade_values': grade_values,
        'periods': periods
    }

    is_valid_student = False
    is_valid_subject = False
    is_valid_grade_type = False
    is_valid_grade = False
    is_valid_period = False

    if request.method == 'POST':

        student = request.POST['student']
        if student is None or student == "":
            messages.error(request, 'Studenti nuk mund të jetë bosh!')
        else:
            student = Student.objects.all().filter(code=student).first()
            student_id = student.id
            is_valid_student = True

        subject = request.POST['subject']
        if subject is None or subject == "":
            messages.error(request, 'Lënda nuk mund të jetë bosh!')
        else:
            subject = Subject.objects.all().filter(code=subject).first()
            subject_id = subject.id
            is_valid_subject = True

        period = request.POST['period']
        if period is None or period == "":
            messages.error(request, 'Periudha nuk mund të jetë bosh!')
        else:
            period = Period.objects.all().filter(code=period).first()
            period_id = period.id
            is_valid_period = True

        grade_type = request.POST['grade_type']
        if grade_type is None or grade_type == "":
            messages.error(request, 'Tipi i vlerësimit nuk mund të jetë bosh!')
        else:
            grade_type = GradeType.objects.all().filter(code=grade_type).first()
            grade_type_id = grade_type.id
            is_valid_grade_type = True

        grade = request.POST['grade']
        if grade is None or grade == "":
            messages.error(request, 'Nota nuk mund të jetë bosh!')
        else:
            grade = GradeValue.objects.all().filter(code=grade).first()
            grade_id = grade.id
            is_valid_grade = True

        if is_valid_student is True and is_valid_subject is True and is_valid_grade_type is True and is_valid_grade is True and is_valid_period is True:

            existing_grade = Grade.objects.all().filter(
                grade_type_id=grade_type_id,
                student_id=student_id,
                period_id=period_id,
                subject_id=subject_id,
            ).count()

            if existing_grade > 0:
                messages.error(request, 'Ekziston një notë me kqto specifika në sistem!')
            else:
                Grade.objects.create(
                    grade_id=grade_id,
                    grade_type_id=grade_type_id,
                    student_id=student_id,
                    period_id=period_id,
                    subject_id=subject_id,
                )
                return redirect('statistics')

    return render(request, 'add-grades.html', context)


def statistika(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().filter(is_active=True).order_by('index')

    context = {
        'subjects': subjects,
        'periods': periods
    }

    return render(request, 'statistics.html', context)


def printo_liste_detyrimi(request):
    students = Student.objects.all().filter(is_active=True).order_by('name')
    return PrintStudentDetails.printMainClassStudentDetails(students)


def printo_liste_prinderish(request):
    parents = Parent.objects.all().filter(is_active=True).order_by('student__name')
    return PrintParentDetails.printMainClassParentDetails(parents)


def printo_statistike_vjetore_klasa_kujdestari(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics.printMainClassStatisticFullYear(subjects)


def printo_statistike_periudha_1_klasa_kujdestari(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics.printMainClassStatisticFirstPeriod(subjects)


def printo_statistike_periudha_2_klasa_kujdestari(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics.printMainClassStatisticSecondPeriod(subjects)


def printo_statistike_periudha_3_klasa_kujdestari(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics.printMainClassStatisticThirdPeriod(subjects)


def printo_statistike_vjetore_8A(request):
    grades = GradeClass.objects.all().filter(classs_id__id=1, is_active=True).order_by('student__name')
    return PrintStatistics8A.print8AStatisticFullYear(grades)


def printo_statistike_periudha_1_8A(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8A.print8AStatisticFirstPeriod()


def printo_statistike_periudha_2_8A(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8A.print8AStatisticSecondPeriod()


def printo_statistike_periudha_3_8A(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8A.print8AStatisticThirdPeriod()


def printo_statistike_vjetore_8D(request):
    grades = GradeClass.objects.all().filter(classs_id__id=3, is_active=True).order_by('student__name')
    return PrintStatistics8D.print8DStatisticFullYear(grades)


def printo_statistike_periudha_1_8D(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8D.print8DStatisticFirstPeriod()


def printo_statistike_periudha_2_8D(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8D.print8DStatisticSecondPeriod()


def printo_statistike_periudha_3_8D(request):
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    return PrintStatistics8D.print8DStatisticThirdPeriod()


def printo_statistike_vjetore_8E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=4, is_active=True).order_by('student__name')
    return PrintStatistics8E.print8EStatisticFullYear(grades)


def printo_statistike_periudha_1_8E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=4, is_active=True).order_by('student__name')
    return PrintStatistics8E.print8EStatisticFirstPeriod()


def printo_statistike_periudha_2_8E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=4, is_active=True).order_by('student__name')
    return PrintStatistics8E.print8EStatisticSecondPeriod()


def printo_statistike_periudha_3_8E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=4, is_active=True).order_by('student__name')
    return PrintStatistics8E.print8EStatisticThirdPeriod()


def printo_statistike_vjetore_9E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=5, is_active=True).order_by('student__name')
    return PrintStatistics9E.print9EStatisticFullYear(grades)


def printo_statistike_periudha_1_9E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=5, is_active=True).order_by('student__name')
    return PrintStatistics9E.print9EStatisticFirstPeriod()


def printo_statistike_periudha_2_9E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=5, is_active=True).order_by('student__name')
    return PrintStatistics9E.print9EStatisticSecondPeriod()


def printo_statistike_periudha_3_9E(request):
    grades = GradeClass.objects.all().filter(classs_id__id=5, is_active=True).order_by('student__name')
    return PrintStatistics9E.print9EStatisticThirdPeriod()


def klasa_8_a(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=1).order_by('name')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().filter(is_active=True).order_by('index')

    grade_class = GradeClass.objects.all().filter(is_active=True, classs_id__id=1).order_by('student__name')

    context = {
        'grade_class': grade_class,
        'student_classes': student_classes,
        'subjects': subjects,
        'periods': periods
    }
    return render(request, 'class-8-a.html', context)


def klasa_8_a_shto_nxenes(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')

        name = str(name).capitalize()
        surname = str(surname).capitalize()
        code = "8-A-" + name + "-" + surname
        class_code = get_object_or_404(Class, id=1).code
        counter = StudentClass.objects.filter(code=code).count()

        if counter > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këto të dhëna në sistem!')
        else:

            class_id = get_object_or_404(Class, id=1)

            StudentClass.objects.create(
                code=code,
                name=name,
                surname=surname,
                class_id=class_id
            )
            return redirect('class-8-a')

    return render(request, 'add-student-8-a.html')


def klasa_8_a_shto_note(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=1).order_by('name')

    context = {
        'student_classes': student_classes
    }

    if request.method == 'POST':
        student_id = request.POST['student_id']
        if student_id is None or student_id == '':
            messages.success(request, 'Zgjidhni një nxënës!')
        elif student_id == '0' or student_id == 0:
            messages.success(request, 'Zgjidhni një nxënës!')
        else:
            student_id = student_id

        code = '8-A-GRADE-FOR-STUDENT-' + str(student_id)

        vlv_period_1 = request.POST['vlv_period_1']
        if vlv_period_1 is None or vlv_period_1 == '':
            vlv_period_1 = 0

        vlp_period_1 = request.POST['vlp_period_1']
        if vlp_period_1 is None or vlp_period_1 == '':
            vlp_period_1 = 0

        vlt_period_1 = request.POST['vlt_period_1']
        if vlt_period_1 is None or vlt_period_1 == '':
            vlt_period_1 = 0

        vlv_period_2 = request.POST['vlv_period_2']
        if vlv_period_2 is None or vlv_period_2 == '':
            vlv_period_2 = 0

        vlp_period_2 = request.POST['vlp_period_2']
        if vlp_period_2 is None or vlp_period_2 == '':
            vlp_period_2 = 0

        vlt_period_2 = request.POST['vlt_period_2']
        if vlt_period_2 is None or vlt_period_2 == '':
            vlt_period_2 = 0

        vlv_period_3 = request.POST['vlv_period_3']
        if vlv_period_3 is None or vlv_period_3 == '':
            vlv_period_3 = 0

        vlp_period_3 = request.POST['vlp_period_3']
        if vlp_period_3 is None or vlp_period_3 == '':
            vlp_period_3 = 0

        vlt_period_3 = request.POST['vlt_period_3']
        if vlt_period_3 is None or vlt_period_3 == '':
            vlt_period_3 = 0

        counter = GradeClass.objects.filter(code=code, student_id=student_id, classs_id=get_object_or_404(Class, id=1).id, is_active=True).count()
        if counter > 0:
            GradeClass.objects.filter(
                code=code, student_id=student_id, classs_id=get_object_or_404(Class, id=1).id
            ).update(
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u modifikuan me sukses!')
            return redirect('class-8-a')
        else:
            GradeClass.objects.create(
                code=code,
                student_id=student_id,
                classs_id=get_object_or_404(Class, id=1).id,
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u shtuan me sukses!')
            return redirect('class-8-a')
    return render(request, 'add-grade-8-a.html', context)


def klasa_8_d(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=3).order_by('name')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().filter(is_active=True).order_by('index')

    grade_class = GradeClass.objects.all().filter(is_active=True, classs_id__id=3).order_by('student__name')

    context = {
        'grade_class': grade_class,
        'student_classes': student_classes,
        'subjects': subjects,
        'periods': periods
    }
    return render(request, 'class-8-d.html', context)


def klasa_8_d_shto_nxenes(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')

        class_code = get_object_or_404(Class, id=3).code
        counter = StudentClass.objects.filter(name=name, surname=surname, class_id__code=class_code).count()

        if counter > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këto të dhëna në sistem!')
        else:
            name = str(name).capitalize()
            surname = str(surname).capitalize()
            code = "8-D-" + name + surname

            class_id = get_object_or_404(Class, id=3)

            StudentClass.objects.create(
                code=code,
                name=name,
                surname=surname,
                class_id=class_id
            )
            return redirect('class-8-d')
    return render(request, 'add-student-8-d.html')


def klasa_8_d_shto_note(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=3).order_by('name')

    context = {
        'student_classes': student_classes
    }

    if request.method == 'POST':
        student_id = request.POST['student_id']
        if student_id is None or student_id == '':
            messages.success(request, 'Zgjidhni një nxënës!')
        elif student_id == '0' or student_id == 0:
            messages.success(request, 'Zgjidhni një nxënës!')
        else:
            student_id = student_id

        code = '8-D-GRADE-FOR-STUDENT-' + str(student_id)

        vlv_period_1 = request.POST['vlv_period_1']
        if vlv_period_1 is None or vlv_period_1 == '':
            vlv_period_1 = 0

        vlp_period_1 = request.POST['vlp_period_1']
        if vlp_period_1 is None or vlp_period_1 == '':
            vlp_period_1 = 0

        vlt_period_1 = request.POST['vlt_period_1']
        if vlt_period_1 is None or vlt_period_1 == '':
            vlt_period_1 = 0

        vlv_period_2 = request.POST['vlv_period_2']
        if vlv_period_2 is None or vlv_period_2 == '':
            vlv_period_2 = 0

        vlp_period_2 = request.POST['vlp_period_2']
        if vlp_period_2 is None or vlp_period_2 == '':
            vlp_period_2 = 0

        vlt_period_2 = request.POST['vlt_period_2']
        if vlt_period_2 is None or vlt_period_2 == '':
            vlt_period_2 = 0

        vlv_period_3 = request.POST['vlv_period_3']
        if vlv_period_3 is None or vlv_period_3 == '':
            vlv_period_3 = 0

        vlp_period_3 = request.POST['vlp_period_3']
        if vlp_period_3 is None or vlp_period_3 == '':
            vlp_period_3 = 0

        vlt_period_3 = request.POST['vlt_period_3']
        if vlt_period_3 is None or vlt_period_3 == '':
            vlt_period_3 = 0

        counter = GradeClass.objects.filter(code=code, student_id=student_id,
                                            classs_id=get_object_or_404(Class, id=3).id, is_active=True).count()
        if counter > 0:
            GradeClass.objects.filter(
                code=code, student_id=student_id, classs_id=3
            ).update(
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u modifikuan me sukses!')
            return redirect('class-8-d')
        else:
            GradeClass.objects.create(
                code=code,
                student_id=student_id,
                classs_id=3,
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u shtuan me sukses!')
            return redirect('class-8-d')
    return render(request, 'add-grade-8-d.html', context)


def klasa_8_e(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=4).order_by('name')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().filter(is_active=True).order_by('index')

    grade_class = GradeClass.objects.all().filter(is_active=True, classs_id__id=4).order_by('student__name')

    context = {
        'grade_class': grade_class,
        'student_classes': student_classes,
        'subjects': subjects,
        'periods': periods
    }
    return render(request, 'class-8-e.html', context)


def klasa_8_e_shto_nxenes(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')

        class_code = get_object_or_404(Class, id=4).code
        counter = StudentClass.objects.filter(name=name, surname=surname, class_id__code=class_code).count()

        if counter > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këto të dhëna në sistem!')
        else:
            name = str(name).capitalize()
            surname = str(surname).capitalize()
            code = "8-E-" + name + surname

            class_id = get_object_or_404(Class, id=4)

            StudentClass.objects.create(
                code=code,
                name=name,
                surname=surname,
                class_id=class_id
            )
            return redirect('class-8-e')
    return render(request, 'add-student-8-e.html')


def klasa_8_e_shto_note(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=4).order_by('name')

    context = {
        'student_classes': student_classes
    }

    if request.method == 'POST':
        student_id = request.POST['student_id']
        if student_id is None or student_id == '':
            messages.success(request, 'Zgjidhni një nxënës!')
        elif student_id == '0' or student_id == 0:
            messages.success(request, 'Zgjidhni një nxënës!')
        else:
            student_id = student_id

        code = '8-E-GRADE-FOR-STUDENT-' + str(student_id)

        vlv_period_1 = request.POST['vlv_period_1']
        if vlv_period_1 is None or vlv_period_1 == '':
            vlv_period_1 = 0

        vlp_period_1 = request.POST['vlp_period_1']
        if vlp_period_1 is None or vlp_period_1 == '':
            vlp_period_1 = 0

        vlt_period_1 = request.POST['vlt_period_1']
        if vlt_period_1 is None or vlt_period_1 == '':
            vlt_period_1 = 0

        vlv_period_2 = request.POST['vlv_period_2']
        if vlv_period_2 is None or vlv_period_2 == '':
            vlv_period_2 = 0

        vlp_period_2 = request.POST['vlp_period_2']
        if vlp_period_2 is None or vlp_period_2 == '':
            vlp_period_2 = 0

        vlt_period_2 = request.POST['vlt_period_2']
        if vlt_period_2 is None or vlt_period_2 == '':
            vlt_period_2 = 0

        vlv_period_3 = request.POST['vlv_period_3']
        if vlv_period_3 is None or vlv_period_3 == '':
            vlv_period_3 = 0

        vlp_period_3 = request.POST['vlp_period_3']
        if vlp_period_3 is None or vlp_period_3 == '':
            vlp_period_3 = 0

        vlt_period_3 = request.POST['vlt_period_3']
        if vlt_period_3 is None or vlt_period_3 == '':
            vlt_period_3 = 0

        counter = GradeClass.objects.filter(code=code, student_id=student_id,
                                            classs_id=get_object_or_404(Class, id=4).id, is_active=True).count()
        if counter > 0:
            GradeClass.objects.filter(
                code=code, student_id=student_id, classs_id=4
            ).update(
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u modifikuan me sukses!')
            return redirect('class-8-e')
        else:
            GradeClass.objects.create(
                code=code,
                student_id=student_id,
                classs_id=4,
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u shtuan me sukses!')
            return redirect('class-8-e')
    return render(request, 'add-grade-8-e.html', context)


def klasa_9_e(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=5).order_by('name')
    subjects = Subject.objects.all().filter(is_active=True).order_by('index')
    periods = Period.objects.all().filter(is_active=True).order_by('index')

    grade_class = GradeClass.objects.all().filter(is_active=True, classs_id__id=5).order_by('student__name')

    context = {
        'grade_class': grade_class,
        'student_classes': student_classes,
        'subjects': subjects,
        'periods': periods
    }
    return render(request, 'class-9-e.html', context)


def klasa_9_e_shto_nxenes(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name is None or name == "":
            messages.error(request, 'Emri i nxënësit nuk mund të jetë bosh!')

        surname = request.POST['surname']
        if surname is None or surname == "":
            messages.error(request, 'Mbiemri i nxënësit nuk mund të jetë bosh!')

        class_code = get_object_or_404(Class, id=5).code
        counter = StudentClass.objects.filter(name=name, surname=surname, class_id__code=class_code).count()

        if counter > 0:
            messages.error(request, 'Ekziston një tjetër nxënës me këto të dhëna në sistem!')
        else:
            name = str(name).capitalize()
            surname = str(surname).capitalize()
            code = "9-E-" + name + surname

            class_id = get_object_or_404(Class, id=5)

            StudentClass.objects.create(
                code=code,
                name=name,
                surname=surname,
                class_id=class_id
            )
            return redirect('class-9-e')
    return render(request, 'add-student-9-e.html')


def klasa_9_e_shto_note(request):
    student_classes = StudentClass.objects.all().filter(is_active=True, class_id__id=5).order_by('name')

    context = {
        'student_classes': student_classes
    }

    if request.method == 'POST':
        student_id = request.POST['student_id']
        if student_id is None or student_id == '':
            messages.success(request, 'Zgjidhni një nxënës!')
        elif student_id == '0' or student_id == 0:
            messages.success(request, 'Zgjidhni një nxënës!')
        else:
            student_id = student_id

        code = '9-E-GRADE-FOR-STUDENT-' + str(student_id)

        vlv_period_1 = request.POST['vlv_period_1']
        if vlv_period_1 is None or vlv_period_1 == '':
            vlv_period_1 = 0

        vlp_period_1 = request.POST['vlp_period_1']
        if vlp_period_1 is None or vlp_period_1 == '':
            vlp_period_1 = 0

        vlt_period_1 = request.POST['vlt_period_1']
        if vlt_period_1 is None or vlt_period_1 == '':
            vlt_period_1 = 0

        vlv_period_2 = request.POST['vlv_period_2']
        if vlv_period_2 is None or vlv_period_2 == '':
            vlv_period_2 = 0

        vlp_period_2 = request.POST['vlp_period_2']
        if vlp_period_2 is None or vlp_period_2 == '':
            vlp_period_2 = 0

        vlt_period_2 = request.POST['vlt_period_2']
        if vlt_period_2 is None or vlt_period_2 == '':
            vlt_period_2 = 0

        vlv_period_3 = request.POST['vlv_period_3']
        if vlv_period_3 is None or vlv_period_3 == '':
            vlv_period_3 = 0

        vlp_period_3 = request.POST['vlp_period_3']
        if vlp_period_3 is None or vlp_period_3 == '':
            vlp_period_3 = 0

        vlt_period_3 = request.POST['vlt_period_3']
        if vlt_period_3 is None or vlt_period_3 == '':
            vlt_period_3 = 0

        counter = GradeClass.objects.filter(code=code, student_id=student_id,
                                            classs_id=get_object_or_404(Class, id=5).id, is_active=True).count()
        if counter > 0:
            GradeClass.objects.filter(
                code=code, student_id=student_id, classs_id=5
            ).update(
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u modifikuan me sukses!')
            return redirect('class-9-e')
        else:
            GradeClass.objects.create(
                code=code,
                student_id=student_id,
                classs_id=5,
                continuous_grade_p1=float(vlv_period_1),
                project_grade_p1=float(vlp_period_1),
                test_grade_p1=float(vlt_period_1),
                continuous_grade_p2=int(vlv_period_2),
                project_grade_p2=int(vlp_period_2),
                test_grade_p2=int(vlt_period_2),
                continuous_grade_p3=int(vlv_period_3),
                project_grade_p3=int(vlp_period_3),
                test_grade_p3=int(vlt_period_3)
            )
            messages.success(request, 'Të dhënat u shtuan me sukses!')
            return redirect('class-9-e')
    return render(request, 'add-grade-9-e.html', context)
