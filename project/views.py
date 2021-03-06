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
    ans = []
    l = []
    for item in form['l']:
        l.append(Mod(item, form['n']))
    # l = [Mod(form['l'][0], form['n']), Mod(form['l'][0], form['n']), Mod(form['l'][0], form['n'])]
    k = form['n'] - 1
    count = 0
    while k % 2 == 0:
        k = k // 2
        count += 1
    lis = {'between': []}
    for i in l:
        lis['between'].append(['{}^{} = {} != 1'.format(i, k, i ** k)])
        if i ** k == 1:
            ans.append(['{}^{} = 1, значит простое'.format(i, k)])
            continue
        for j in range(count):
            lis['between'].append(['{}^({}*2^{}) = {} != -1'.format(i, k, j, i ** (k * (2 ** j)))])
            if i ** (k * (2 ** j)) == -1:
                ans.append(['{}^({}*2^{}) = -1, значит простое'.format(i, k, j)])
                break
    lis['ans'] = ans

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


@api_method(SixthTaskForm)
def sixth_task(request, form):
    p, q = [i for i in prime_factors(form['n'])]
    f = (p-1)*(q-1)
    d = 1//Mod(form['e'], f)
    s = Mod(form['m']**int(d), form['n'])
    ans = [form['m'], s]
    d = {'ans': 'ans = (m, s) = ({}, {})'.format(form['m'], s), 'between':['n = p*q = {}*{}'.format(p, q),\
                                'f = (p-1)*(q-1) = %s' % f,\
                                'd = e^-1 mod f = %s' % d,\
                                's = c^d mod n = %s' % s,\
                                'ans = (m, s) = ({}, {})'.format(form['m'], s)]}

    return JsonResponse.success(d)


def cypher(request, form):
    g = Mod(form['g'], form ['p'])
    y = g**form['x']
    a = g**form['k']
    b = (y**form['k'])*form['M']
    d = {'ans': '({}, {})'.format(a, b), 'between':['y = g^x = %s' % y,\
                                'a = g^k = %s' % a,\
                                'b = M*y^k = %s' %b,\
                                'ans = ({}, {})'.format(a, b)]}
    return JsonResponse.success(d)


def sign(request, form):
    g = Mod(form['g'], form['p'])
    r = g**form['k']
    r = Mod(int(r), form['p']-1)
    s = (form['M'] - form['x']*r)*(1//Mod(form['k'], form['p']-1))
    d = {'ans': '({}, {})'.format(r, s), 'between':['r = g^k mod p-1 = %s' % r,\
                                's = (M - x*r)*(k)^-1 mod p-1 = %s' % s,\
                                'ans = ({}, {})'.format(r, s)]}

    return JsonResponse.success(d)


@api_method(SeventhTaskForm)
def seventh_task(request, form):
    if form['task_id'] == 1:
        return cypher(request, form)
    elif form['task_id'] == 2:
        return sign(request, form)
    else:
        return JsonResponse.internal_error()


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
