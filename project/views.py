from .utils import JsonResponse, api_method
from .forms import *
from mod import Mod
import json


def parse_mod (module):
    return '{}'.format(module)


@api_method('GET', SecondTaskForm)
def second_task(request, form):

    l = form['l']
    p = form['p']

    l = [Mod(i, p) for i in l]
    a = (1 // (l[1] - l[0])) * (l[2] - l[1])
    b = l[1] - a * l[0]
    l.append(a * l[2] + b)
    l.append(a * l[3] + b)
    lis = ['a = {}, '.format(a), 'b = {}'.format(b)]
    d = {'ans': 'x4={}, x5={}'.format(l[3], l[4]), 'between': lis}

    return JsonResponse.success(d)


@api_method('GET', FourthTaskForm)
def fourth_task (request, form):
    l = form['l']
    n = form['n']
    ans = []
    l = [Mod(i, n) for i in l]
    k = n - 1
    count = 0
    while k % 2 == 0:
        k = k // 2
        count += 1
    lis = {'between':[]}
    for i in l:
        lis['between'].append([parse_mod(i), 1, parse_mod(i**k)])
        if i**k == 1:
            ans.append([parse_mod(i), 1])
            continue
        for j in range(count):
            lis['between'].append([parse_mod(i), 2, j, parse_mod(i**(k*(2**j)))])
            if i**(k*(2**j)) == -1:
                ans.append([parse_mod(i), 2, j])
                break

    lis['ans'] = ans
    lis['between'] = lis['between']

    return JsonResponse.success(lis)
