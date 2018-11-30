from .utils import JsonResponse, api_method
from .forms import *
from .maths_modules.modular_arithmetic import Mod
from .maths_modules.eliptic import Coord, EC


def parse_mod(module):
    return '{}'.format(module)


@api_method(SecondTaskForm)
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


@api_method(FourthTaskForm)
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
            lis['between'].append([parse_mod(i), -1, j, parse_mod(i**(k*(2**j)))])
            if i**(k*(2**j)) == -1:
                ans.append([parse_mod(i), -1, j])
                break

    lis['ans'] = ans
    lis['between'] = lis['between']

    return JsonResponse.success(lis)


@api_method(FifthTaskForm)
def fifth_task(request, form):
    n = form['n']
    e = form['e']
    c = form['c']
    p = form['p']
    q = form['q']

    f = (p-1)*(q-1)
    d = 1//Mod(e, f)
    ans = Mod(c**int(d), n)
    d = {'ans': parse_mod(ans), 'between': [(parse_mod(d), f)]}
    return JsonResponse.success(d)


@api_method(ElipticForm)
def solve_eliptic(request, form):
    task_id = form['task_id']
    a = form['a']
    b = form['b']
    q = form['q']
    x = form['x']
    y = form['y']
    n = form.get('n', None)

    ec = EC(a, b, q)

    def solver_1(__x, __y, __n):
        p = Coord(__x, __y)
        return ec.mul(p, __n)

    def solver_2():
        return ec.generate()

    def solver_3(__x, __y):
        return ec.generate_from_point(Coord(__x, __y))

    return JsonResponse.success({'status': 'ok'})
