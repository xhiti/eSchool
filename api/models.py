from django.db import models
from django.urls import reverse
from klasat.models import Class


# Create your models here.
class Subject(models.Model):
    code = models.CharField(blank=True, max_length=20)
    title = models.CharField(max_length=20)
    initials = models.CharField(max_length=3, blank=True)
    description = models.CharField(blank=True, max_length=100)
    index = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('edit-subject', args=[str(self.code)])

    def get_delete_url(self):
        return reverse('delete-subject', args=[str(self.code)])


class Period(models.Model):
    code = models.CharField(blank=True, max_length=20)
    title = models.CharField(max_length=20)
    description = models.CharField(blank=True, max_length=100)
    index = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GradeType(models.Model):
    code = models.CharField(blank=True, max_length=20)
    title = models.CharField(max_length=20)
    description = models.CharField(blank=True, max_length=100)
    initials = models.CharField(blank=True, max_length=3)
    index = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    code = models.CharField(blank=True, max_length=100)
    nid = models.CharField(blank=True, max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    father_name = models.CharField(max_length=20)
    email = models.CharField(max_length=255, blank=True)
    birth_date = models.CharField(max_length=255, blank=True)
    birth_place = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=1, blank=True)
    amze_number = models.CharField(max_length=50, blank=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name + " " + self.surname

    def get_info_url(self):
        return reverse('info-student', args=[str(self.code)])

    def get_edit_url(self):
        return reverse('edit-student', args=[str(self.code)])

    def get_delete_url(self):
        return reverse('delete-student', args=[str(self.code)])

    def get_print_url(self):
        return reverse('print-student', args=[str(self.code)])


class StudentCharacteristics(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class StudentAbsences(models.Model):
    code = models.CharField(max_length=100)
    reasonable = models.CharField(max_length=5)
    unreasonable = models.CharField(max_length=5)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Parent(models.Model):
    code = models.CharField(blank=True, max_length=100)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=255, blank=True)
    nid = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse('edit-parent', args=[str(self.code)])

    def get_delete_url(self):
        return reverse('delete-parent', args=[str(self.code)])


class StudentClass(models.Model):
    code = models.CharField(blank=True, max_length=100)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name + " " + self.surname

    # def get_info_url(self):
    #     return reverse('info-student', args=[str(self.code)])
    #
    # def get_edit_url(self):
    #     return reverse('edit-student', args=[str(self.code)])
    #
    # def get_delete_url(self):
    #     return reverse('delete-student', args=[str(self.code)])


class GradeValue(models.Model):
    code = models.CharField(blank=True, max_length=20)
    value = models.IntegerField()
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.value


class Grade(models.Model):
    grade = models.ForeignKey(GradeValue, on_delete=models.CASCADE)
    grade_type = models.ForeignKey(GradeType, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GradeClass(models.Model):
    code = models.CharField(blank=True, max_length=50)
    student = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    classs = models.ForeignKey(Class, on_delete=models.CASCADE)
    continuous_grade_p1 = models.IntegerField(blank=True, default=0)
    project_grade_p1 = models.IntegerField(blank=True, default=0)
    test_grade_p1 = models.IntegerField(blank=True, default=0)
    continuous_grade_p2 = models.IntegerField(blank=True, default=0)
    project_grade_p2 = models.IntegerField(blank=True, default=0)
    test_grade_p2 = models.IntegerField(blank=True, default=0)
    continuous_grade_p3 = models.IntegerField(blank=True, default=0)
    project_grade_p3 = models.IntegerField(blank=True, default=0)
    test_grade_p3 = models.IntegerField(blank=True, default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_average(self):
        continuous_grade_average = (self.continuous_grade_p1 + self.continuous_grade_p2 + self.continuous_grade_p3) / 3
        project_grade_average = (self.project_grade_p1 + self.project_grade_p2 + self.project_grade_p3) / 3
        test_grade_average = (self.test_grade_p1 + self.test_grade_p2 + self.test_grade_p3) / 3
        full_average = (continuous_grade_average * 0.4) + (project_grade_average * 0.2) + (test_grade_average * 0.4)
        return round(full_average, 2)

    def get_round_grade(self):
        continuous_grade_average = (self.continuous_grade_p1 + self.continuous_grade_p2 + self.continuous_grade_p3) / 3
        project_grade_average = (self.project_grade_p1 + self.project_grade_p2 + self.project_grade_p3) / 3
        test_grade_average = (self.test_grade_p1 + self.test_grade_p2 + self.test_grade_p3) / 3
        full_average = (continuous_grade_average * 0.4) + (project_grade_average * 0.2) + (test_grade_average * 0.4)
        return round(full_average)

