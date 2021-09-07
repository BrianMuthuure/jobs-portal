from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from main.models import Job


class JobSearchView(ListView):
    context_object_name = 'jobs'
    template_name = 'search/job_search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(JobSearchView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Job.objects.search(query)
        return Job.objects.all()