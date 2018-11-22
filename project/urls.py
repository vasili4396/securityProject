from django.urls import path
from .views import *

urlpatterns = [
    path('api/second_task', second_task),
    path('api/fourth_task', fourth_task),
    path('api/fifth_task', fifth_task)
]
