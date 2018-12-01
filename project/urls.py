from django.urls import path
from .views import *

urlpatterns = [
    path('api/first_task', first),
    path('api/second_task', second_task),
    path('api/fourth_task', fourth_task),
    path('api/fifth_task', fifth_task),
    path('api/eliptic', solve_eliptic),
]
