import random
import math
import matplotlib.pyplot as plt
import numpy as np


def menu():
    for j in range(5):  #corridas del programa
        nros_uni, eos_uni, vos_uni = [], [], []
        nros_exp, eos_exp, vos_exp = [], [], []
        nros_ga, eos_gam, vos_gam = [], [], []
        nros_nor, eos_nor, vos_nor = [], [], []
        nros_bi, eos_bi, vos_bi = [], [], []
        nros_hip, eos_hip, vos_hip = [], [], []
        nros_poi, eos_poi, vos_poi = [], [], []
        nros_emp, eos_emp, vos_emp = [], [], []
        for i in range(2000):
            x = uniforme(1, 20)
            nros_uni.append(x)
            x = exponencial(20)
            nros_exp.append(x)
            x = gamma(5, 1)
            nros_ga.append(x)
            x = normal(0.5, 0.05)
            nros_nor.append(x)
            x = binomial(10, 0.6)
            nros_bi.append(x)
            x = hipergeo(40, 8, 0.25)
            nros_hip.append(x)
            x = poisson(5)
            nros_poi.append(x)
            x, pi = empirica()
            nros_emp.append(x)
        print('\nCorrida', j+1)
        ee_uni, ve_uni, eo, vo = ev_uni(nros_uni, 1, 20)
        eos_uni.append(eo)
        vos_uni.append(vo)
        ee_exp, ve_exp, eo, vo = ev_exp(nros_exp, 20)
        eos_exp.append(eo)
        vos_exp.append(vo)
        ee_gam, ve_gam, eo, vo = ev_gam(nros_ga, 5, 1)
        eos_gam.append(eo)
        vos_gam.append(vo)
        ee_nor, ve_nor, eo, vo = ev_nor(nros_nor, 0.5, 0.05)
        eos_nor.append(eo)
        vos_nor.append(vo)
        ee_bi, ve_bi, eo, vo = ev_bi(nros_bi, 10, 0.6)
        eos_bi.append(eo)
        vos_bi.append(vo)
        ee_hip, ve_hip, eo, vo = ev_hip(nros_hip, 40, 8, 0.25)
        eos_hip.append(eo)
        vos_hip.append(vo)
        ee_poi, ve_poi, eo, vo = ev_poi(nros_poi, 5)
        eos_poi.append(eo)
        vos_poi.append(vo)
        ee_emp, ve_emp, eo, vo = ev_emp(nros_emp, pi)
        eos_emp.append(eo)
        vos_emp.append(vo)
    graficar('Uniforme', ee_uni, ve_uni, eos_uni, vos_uni)
    graficar('Exponencial', ee_exp, ve_exp, eos_exp, vos_exp)
    graficar('Gamma', ee_gam, ve_gam, eos_gam, vos_gam)
    graficar('Normal', ee_nor, ve_nor, eos_nor, vos_nor)
    graficar('Binomial', ee_bi, ve_bi, eos_bi, vos_bi)
    graficar('Hipergeométrica', ee_hip, ve_hip, eos_hip, vos_hip)
    graficar('de Poisson', ee_poi, ve_poi, eos_poi, vos_poi)
    graficar('Empírica', ee_emp, ve_emp, eos_emp, vos_emp)


def graficar(nombre, ee, ve, eo, vo):
    esperanzas = [[ee, ee, ee, ee], eo]
    X = np.arange(4)
    plt.title("Gráfico de Esperanzas - Distribución " + nombre)   # Establece el título del gráfico
    plt.xlabel("Corridas")   # Establece el título del eje x
    plt.ylabel("EX")   # Establece el título del eje y
    plt.bar(X + 0.00, esperanzas[0], color = "g", width = 0.25)
    plt.bar(X + 0.25, esperanzas[1], color = "b", width = 0.25)
    plt.xticks(X + 0.15, ["1","2","3","4"])
    plt.show()

    varianzas = [[ve, ve, ve, ve], vo]
    X = np.arange(4)
    plt.title("Gráfico de Varianzas - Distribución " + nombre)   # Establece el título del gráfico
    plt.xlabel("Corridas")   # Establece el título del eje x
    plt.ylabel("VX")   # Establece el título del eje y
    plt.bar(X + 0.00, varianzas[0], color = "r", width = 0.25)
    plt.bar(X + 0.25, varianzas[1], color = "b", width = 0.25)
    plt.xticks(X + 0.15, ["1","2","3","4"])
    plt.show()


def test(nombre, ee, ve, eo, vo):
    print('\nDistribución', nombre)
    print('Esperanza esperada:', ee)
    print('Esperanza observada:', eo)
    print('Diferencia entre las esperanzas:', abs(ee - eo))
    print('Varianza esperada:', ve)
    print('Varianza observada:', vo)
    print('Diferencia entre las varianzas:', abs(ve - vo))


def ev_uni(nros, a, b):
    ex = (b + a)/2
    vx = (b - a)**2/12
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Uniforme', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_exp(nros, ex):
    vx = ex**2
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Exponencial', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_gam(nros, k, a):
    ex = k/a
    vx = k/(a**2)
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Gamma', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_nor(nros, ex, vx):
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Normal', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_bi(nros, n, p):
    q = 1 - p
    ex = n * p
    vx = n * p * q
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Binomial', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_hip(nros, N, n, p):
    q = 1 - p
    ex = n * p
    vx = n * p * q * ((N - n)/(N - 1))
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Hipergeometrica', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_poi(nros, p):
    ex = p  #p = lamda
    vx = p
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('de Poisson', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


def ev_emp(nros, pi):
    ex = sum(pi[i]*(i+1) for i in range(len(pi))) #esperanza esperada
    vx = sum((((i+1) - ex)**2)*pi[i] for i in range(len(pi)))
    ex_obs = np.mean(nros)
    vx_obs = np.var(nros)
    test('Empirica', ex, vx, ex_obs, vx_obs)
    return ex, vx, ex_obs, vx_obs


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



