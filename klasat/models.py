from django.db import models
from django.urls import reverse


# Create your models here.
class Class(models.Model):
    code = models.CharField(blank=True, max_length=20)
    title = models.CharField(max_length=20)
    description = models.CharField(blank=True, max_length=100)
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=13)
    # slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('edit-class', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('delete-class', args=[str(self.id)])
