from django.urls import path
from .views import *

urlpatterns = [
    path('', JobSearchView.as_view(), name='query')
]