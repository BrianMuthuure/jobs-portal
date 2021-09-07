from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from django.urls import reverse
from django.utils import timezone

from .managers import JobManager


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='employer_logos', blank=True)
    location = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'employer'
        verbose_name_plural = 'employers'
        db_table = 'employer'

    def __str__(self):
        return f'{self.user}'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now)
    cv = models.FileField(upload_to='users_cvs', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        db_table = 'client'

    def __str__(self):
        return f'{self.user}'


class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_posted = models.DateField(default=timezone.now)

    objects = JobManager()

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        db_table = 'job'
        ordering = ['date_posted', ]

    def __str__(self):
        return f'{self.name} ({self.employer})'

    def get_absolute_url(self):
        return reverse('main:job-detail', kwargs={'pk': self.pk})


class Qualification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Qualification'
        verbose_name_plural = 'Qualifications'
        db_table = 'qualification'

    def __str__(self):
        return self.title


class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    reason_for_application = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'application'
        verbose_name = 'application'
        verbose_name_plural = 'applications'
        ordering = ['date', ]

    def __str__(self):
        return f'{self.client} '