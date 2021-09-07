from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employer, Job, Client, Application


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmployerCreationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['location', 'logo']


class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name']


class ApplicantCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ClientCreationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=
                                    forms.DateInput(attrs=
                                                    {'class': 'form-control', 'placeholder': 'select date',
                                                     'type': 'date'}))
    cv = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}))

    class Meta:
        model = Client
        fields = ['date_of_birth', 'cv']


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [ 'reason_for_application']

    def save(self, commit=True):
        application = super(ApplicationForm, self).save()
        if Application.objects.filter(client=self.cleaned_data['client'], job=self.cleaned_data['job']).exists():
            raise forms.ValidationError("This application already exists")
        if commit:
            application.save()

        return application

