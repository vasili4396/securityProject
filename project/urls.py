from django.urls import path
from .views import *

urlpatterns = [
    path('api/first_task', first_task),
]
