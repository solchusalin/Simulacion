import random
import math
import matplotlib.pyplot as plt
import numpy as np


def menu():
    for j in range(3):  #corridas del programa
        nros_uni = []
        nros_exp = []
        nros_ga = []
        nros_nor = []
        nros_pas = []
        nros_bi = []
        nros_hip = []
        nros_poi = []
        nros_emp = []
        for i in range(2000):
            x = uniforme(1, 20)
            nros_uni.append(x)

            x = exponencial(20)
            nros_exp.append(x)

            x = gamma(5, 1)
            nros_ga.append(x)

            x = normal(0.5, 0.05)
            nros_nor.append(x)

            x = pascal(3, 0.5)
            nros_pas.append(x)

            x = binomial(10, 0.6)
            nros_bi.append(x)

            x = hipergeo(40, 8, 0.25)
            nros_hip.append(x)

            x = poisson(5)
            nros_poi.append(x)

            x, pi = empirica()
            nros_emp.append(x)

        print('\nCorrida', j+1)
        plot_uni(nros_uni, 1, 20)
        plot_exp(nros_exp, 20)
        plot_gam(nros_ga, 5, 1)
        plot_nor(nros_nor, 0.5, 0.05)
        plot_bi(nros_bi, 10, 0.6)
        plot_hip(nros_hip, 40, 8, 0.25)
        plot_poi(nros_poi, 5)
        plot_emp(nros_emp, pi)


def plot_uni(nros, a, b):
    ex = (b + a)/2
    vx = (b - a)**2/12
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Uniforme')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_exp(nros, ex):
    vx = ex**2
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Exponencial')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_gam(nros, k, a):
    ex = k/a
    vx = k/(a**2)
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Gamma')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_nor(nros, ex, vx):
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Normal')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_bi(nros, n, p):
    q = 1 - p
    ex = n * p
    vx = n * p * q
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Binomial')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_hip(nros, N, n, p):
    q = 1 - p
    ex = n * p
    vx = n * p * q * ((N - n)/(N - 1))
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Hipergeométrica')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_poi(nros, p):
    ex = p  #p = lamda
    vx = p
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución de Poisson')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def plot_emp(nros, pi):
    ex = sum(pi[i]*(i+1) for i in range(len(pi))) #esperanza esperada
    vx = sum((((i+1) - ex)**2)*pi[i] for i in range(len(pi)))
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    print('\nDistribución Empírica')
    print('Esperanza esperada:', ex)
    print('Esperanza observada:', ex_obs)
    print('Diferencia entre las esperanzas:', abs(ex - ex_obs))
    print('Varianza esperada:', vx)
    print('Varianza observada:', vx_obs)
    print('Diferencia entre las varianzas:', abs(vx - vx_obs))


def uniforme(a, b):
    r = random.random()
    x = a + (b - a) * r
    return x


def exponencial(ex):
    r = random.random()
    x = -ex * math.log(r)
    return x


def gamma(k, a):
    tr = 1
    for i in range(k):
        r = random.random()
        tr *= r
    x = - math.log(tr)/a
    return x


def normal(ex, vx):
    stdx = math.sqrt(vx)
    sum = 0
    for i in range(12):
        r = random.random()
        sum += r
    x = stdx * (sum - 6) + ex
    return x


def pascal(k, p):
    q = 1 - p
    tr = 1
    qr = math.log(q)
    for i in range(k):
        r = random.random()
        tr = tr * r
    x = math.log(tr)/qr
    return x


def binomial(n, p):
    x = 0
    for i in range(n):
        r = random.random()
        if (r-p) < 0:
            x += 1
    return x


def hipergeo(N, n, p):
    x = 0
    for i in range(n):
        r = random.random()
        if (r-p) < 0:
            s = 1
            x += 1
        else:
            s = 0
        p = (N * p - s)/(N - 1)
        N = N - 1
    return x


def poisson(p):
    x = 0
    tr = 1
    b = math.exp(-p)
    r = random.random()
    tr *= r
    while (tr-b) >= 0:
        x += 1
        r = random.random()
        tr = tr * r
    return x


def empirica():
    pi = [0.25, 0.2, 0.15, 0.3, 0.1]
    pi_acum = []
    pi_acum.append(pi[0])
    for i in range(1, len(pi)):
        pi_acum.append(pi_acum[i-1]+pi[i])
    r = random.random()
    if r <= pi_acum[0]:
        x = 1
    else:
        for i in range(1, len(pi)):
            if(r > pi_acum[i-1] and r <= pi_acum[i]):
                x = i+1
    return x, pi



#main
menu()



