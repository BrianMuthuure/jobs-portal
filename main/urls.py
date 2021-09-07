from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('jobs/', JobListView.as_view(), name='jobs'),
    path('add-employer/', add_employer, name='add-employer'),

    path('add-client/', add_client, name='add-client'),
    path('create-job/', create_job, name='create-job'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/update', JobUpdateView.as_view(), name='update-job'),
    path('jobs/<int:pk>/delete', JobDeleteView.as_view(), name='delete-job'),
    path('jobs/<int:pk>/add-qualification', add_qualification, name='add-qualification'),
    path('jobs/<int:pk>/apply', apply, name='apply'),
]
