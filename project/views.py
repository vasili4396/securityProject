from .utils import JsonResponse, api_method
from .forms import *
from .maths_modules.modular_arithmetic import Mod
from .maths_modules.eliptic import Coord, EC
from .maths_modules.other import *
import numpy as np


def parse_mod(module):
    return '{}'.format(module)


@api_method(FirstTaskForm)
def first (request, form):
    #set_trace()
    def ent(l):
        ans = 0
        for i in l:
            ans += -i*np.log2(i)
        return ans
    def ent_c(X, Y):
        ans = 0
        for x in X:
            for y in Y:
                ans += -x*y*np.log2(x*y)
        return ans
    def mutXY (X, Z, Y):
        x1, x2 = X
        z1, z2 = Z
        y1, y2 = Y
        return ent(X) - (-x1*z1*np.log2(x1*z1/y1)\
                         -x1*z2*np.log2(x1*z2/y2)\
                         -x2*z2*np.log2(x2*z2/y1)\
                         -x2*z1*np.log2(x2*z1/y2))
    def aps (X, Z, Y):
        x1, x2 = X
        z1, z2 = Z
        y1, y2 = Y
        ans = [x1*z1/y1, x2*z2/y1, x1*z2/y2, x2*z1/y2]
        ans.append((ans [0] == x1)&(ans [1] == x2)&(ans [2] == x1)&(ans [3] == x2))
        return ans
    x1, x2, z1, z2, ans, between= form['x1'], form['x2'], form['z1'], form['z2'], [], []
    #1
    y1, y2 = x1*z1+x2*z2, x1*z2+x2*z1
    ans.append((round(-np.log2(x1), 2), round(-np.log2(x2), 2)))
    between.extend(['I(x1) = -log2(p(x1)) = {}'.format(ans[0][0]), 'I(x2) = -log2(p(x2)) = {}'.format(ans[0][1])])
    #2
    ans.append((round(ent([x1, x2]), 2), round(ent([z1, z2]), 2), round(ent([y1, y2]), 2)))
    between.extend(['H(x1, x2) = -p(x1)log2(p(x1))-p(x2)log2(p(x2)) = {}'.format(ans[1][0]),\
                    'H(z1, z2) = {}'.format(ans[1][1]),\
                    'H(y1, y2) = {}'.format(ans[1][2])])
    #3
    ans.append(0)
    between.extend(['I = 0, тк. они независимы'])
    #4
    ans.append(mutXY([x1, x2], [z1, z2], [y1, y2]))
    between.extend(['I(X, Y) = S(-p(x, y)log2(p(x|y))) = {}'.format(ans[3])])
    #5
    ans.append(mutXY([z1, z2], [x1, x2], [y1, y2]))
    between.extend(['I(Z, Y) = S(-p(z, y)log2(p(z|y))) = {}'.format(ans[4])])
    #6
    ans.append(aps([z1, z2], [x1, x2], [y1, y2]))
    between.extend(['P(x1,y1) = p(x1)p(y1|x1)/p(y1) = {}'.format(ans[5][0]),\
                    'P(x2, y1) = {}'.format(ans[5][1]),\
                    'P(x2, y1) = {}'.format(ans[5][2]),\
                    'P(x1, y2) = {}'.format(ans[5][3]),\
                    'P(x, y) != P(x) => {}, сделайте равновероятными'.format(ans[5][4])])
    d = {'ans': ans, 'between': between}

    return JsonResponse.success(d)


@api_method(SecondTaskForm)
def second_task(request, form):
    l0 = form['l'][0]
    l1 = form['l'][1]
    l2 = form['l'][2]
    l0, l1, l2 = Mod(l0, form['p']), Mod(l1, form['p']), Mod(l2, form['p'])
    a = (1 // (l1 - l0)) * (l2 - l1)
    b = l1 - a * l0
    l3 = a * l2 + b
    l4 = a * l3 + b
    lis = ['a = (x1-x2)*(x2-x3)^-1 = {}'.format(a), \
           'b = (x2-b)*x1^-1 = {}'.format(b), \
           'x4 = a*x3 + b= {}'.format(l3), \
           'x5 = a*x4 + b= {}'.format(l4)]

    d = {'ans': parse_mod((l3, l4)), 'between': lis}
    return JsonResponse.success(d)


@api_method(ThirdTaskForm)
def third_task(request, form):
    par = form['par']
    p = len(par)//2
    A = [par[i:p+i]+[1] for i in range(p+1)]
    y = par[p:]
    B = modMatInv(A,2)
    ans = np.array(B).dot(np.array(y))%2
    pol = ''
    for i in range(len(ans)):
        if ans[i]:
            pol+='x^{}+'.format(p-i)
    lis = ['A*x = y => x = A^-1*y', 'A = {}'.format(A), 'A^-1 = {}'.format(B), 'solv of lin sys = {}'.format(ans), pol[:-1]]
    d = {'ans': pol[:-1],  'between': lis}

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
    p, q = [i for i in prime_factors(form['n'])]
    f = (p-1)*(q-1)
    d = 1//Mod(form['e'], f)
    ans = Mod(form['c']**int(d), form['n'])
    d = {'ans': 'ans = c^d mod n = %s' % ans, 'between':['n = p*q = {}*{}'.format(p, q),\
                                'f = (p-1)*(q-1) = %s' % f,\
                                'd = e^-1 mod f = %s' % d,\
                                'ans = c^d mod n = %s' % ans]}

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
        return ec.mul(p, __n).__str__()

    def solver_2():
        res = ec.generate()
        return [item.__str__() for item in res]

    def solver_3(__x, __y):
        res = ec.generate_from_point(Coord(__x, __y))
        return [item.__str__() for item in res]

    if task_id == 1:
        res = solver_1(x, y, n)
    elif task_id == 2:
        res = solver_2()
    else:
        res = solver_3(x, y)

    return JsonResponse.success(res)
