from django.urls import path
from .views import *

urlpatterns = [
    path('api/second_task', second_task),
]
