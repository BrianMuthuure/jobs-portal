from django.contrib import admin

from .models import Employer, Client, Job, Qualification, Application


admin.site.register(Application)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'registration_date']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'cv']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['employer', 'name', 'date_posted']


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ['job', 'title']