from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .models import Job, Employer, Qualification
from .forms import *


def home(request):
    return render(request, 'home.html')


class JobListView(ListView):
    model = Job
    context_object_name = 'jobs'
    template_name = 'jobs/job_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(JobListView, self).get_context_data(*args, **kwargs)
        return context


def add_employer(request):
    if request.method == 'POST':
        u_form = UserRegistrationForm(request.POST)
        e_form = EmployerCreationForm(request.POST, request.FILES)
        if u_form.is_valid() and e_form.is_valid():
            user = u_form.save()
            user.save()
            employee = e_form.save(commit=False)
            employee.user = user
            employee.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            group = Group.objects.get(name='Employers')
            user.groups.add(group)
            return redirect('/')
    else:
        u_form = UserRegistrationForm()
        e_form = EmployerCreationForm()
    context = {
        'u_form': u_form,
        'e_form': e_form
    }
    return render(request, 'employers/registration.html', context)


def add_client(request):
    if request.method == 'POST':
        a_form = ApplicantCreationForm(request.POST)
        c_form = ClientCreationForm(request.POST, request.FILES)
        if a_form.is_valid() and c_form.is_valid():
            user = a_form.save()
            user.save()
            client = c_form.save(commit=False)
            client.user = user
            client.save()
            username = a_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            group = Group.objects.get(name='Clients')
            user.groups.add(group)
            return redirect('/')
    else:
        a_form = ApplicantCreationForm()
        c_form = ClientCreationForm()
    context = {
        'u_form': a_form,
        'e_form': c_form
    }
    return render(request, 'clients/client_registration.html', context)


def create_job(request):
    job = Job.objects.none()
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        if form.is_valid():
            employer = request.user
            job = Job(
                employer=get_object_or_404(Employer, user=employer),
                name=form.cleaned_data.get('name'),
                date_posted=timezone.now(),
            )
            job.save()
            messages.success(request, 'Job was posted successfully')
            return redirect('main:jobs')
    else:
        form = JobCreationForm()
    context = {
        'form': form
    }
    return render(request, 'jobs/job_form.html', context)


class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['qualifications'] = Qualification.objects.filter(job=self.object)
        return context


def add_qualification(request, pk):
    QualificationFormSET = inlineformset_factory(Job, Qualification, fields=('title', ), extra=6, can_delete=True)
    job = Job.objects.get(id=pk)

    formset = QualificationFormSET(queryset=Qualification.objects.all(), instance=job)
    if request.method == 'POST':
        formset = QualificationFormSET(request.POST, instance=job)
        if formset.is_valid():
            if request.user == job.employer.user:
                formset.save()
                print(job.employer)
                print(request.user)
                messages.success(request, "You have added qualifications successfully")
                return redirect(reverse('main:job-detail', kwargs={'pk': pk}))
    context = {
        'form': formset,
    }
    return render(request, 'jobs/qualification.html', context)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Job
    form_class = JobCreationForm
    template_name = 'jobs/job_form.html'
    success_message = 'This Job was updated successfully'

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.employer.user:
            return True
        return False


def apply(request, pk):
    job = Job.objects.get(id=pk)
    form = ApplicationForm(initial={'job': job})
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():

            client = request.user
            application = Application(
                client=get_object_or_404(Client, user=client),
                job=get_object_or_404(Job, id=pk),
                reason_for_application=form.cleaned_data.get('reason_for_application'),
                date=timezone.now(),
            )
            application_qs = Application.objects.filter(client__user=client, job=job)
            if application_qs.exists():
                messages.error(request, 'You already applied for this job')
                return render(request, 'applications/error.html')
            else:
                application.save()
                messages.success(request, 'Your application was successful')
                return redirect('/')
    else:
        form = ApplicationForm()
    context = {
        'form': form
    }
    return render(request, 'applications/application.html', context)


class JobDeleteView(UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/delete.html'
    success_url = reverse_lazy('main:jobs')

    def test_func(self):
        job = self.get_object()
        if self.request.user == job.employer:
            return True
        return False
