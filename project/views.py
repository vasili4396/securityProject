from .utils import JsonResponse, api_method
from .forms import SecondTaskForm
from mod import Mod
import json


@api_method('GET', SecondTaskForm)
def second_task(request, form):
    l = form['l']
    p = form['p']

    l = [Mod(i, p) for i in l]

    a = (l[2] - l[1]) * (l[1] - l[0]) ** (-1)
    b = l[1] - a * l[0]
    l.append(a * l[2] + b)
    l.append(a * l[3] + b)
    lis = ['a = {}'.format(a), 'b = {}'.format(b), 'x4 = {}'.format(l[3]), 'x5 = {}'.format(l[4])]
    d = {'ans': 'x4={}, x5={}'.format(l[3], l[4]), 'between': lis}

    return JsonResponse.success(d)
