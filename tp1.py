import random
import matplotlib.pyplot as plt
import statistics as stats
import math

#funciones graficas
def plot_prom(pe, proms):
    plt.title('Valor Promedio (VP)')
    plt.xlabel('N')
    plt.ylabel('VP')
    plt.plot(pe, label="VP esperado")
    for i in range(0, len(proms)):
        plt.plot(proms[i], label="VP corrida {}".format(i+1))
    plt.legend(prop = {'size': 7})

def plot_fr(fre, frs):
    plt.title('Frecuencia Relativa (Fr)')
    plt.xlabel('N')
    plt.ylabel('Fr')
    plt.plot(fre, label="Fr esperada")
    for i in range(0, len(frs)):
        plt.plot(frs[i], label="Fr corrida {}".format(i+1))
    plt.legend(prop = {'size': 7})

def plot_desv(de, des):
    plt.title('Desvio estandar (STD)')
    plt.xlabel('N')
    plt.ylabel('STD')
    plt.plot(de, label="STD esperado")
    for i in range(0, len(des)):
        plt.plot(des[i], label="STD corrida {}".format(i+1))
    plt.legend(prop = {'size': 7})

def plot_var(ve, vars):
    plt.title('Varianza (V)')
    plt.xlabel('N')
    plt.ylabel('V')
    plt.plot(ve, label="V esperada")
    for i in range(0, len(vars)):
        plt.plot(vars[i], label="V corrida {}".format(i+1))
    plt.legend(prop = {'size': 7})

def plot_todo(pe, proms, fre, frs, de, des, ve, vars):
    plt.figure(figsize=(12,6))
    plt.suptitle('Graficas')
    plt.subplot(2,2,1)
    plot_prom(pe, proms)
    plt.subplot(2,2,2)
    plot_fr(fre, frs)
    plt.subplot(2,2,3)
    plot_desv(de, des)
    plt.subplot(2,2,4)
    plot_var(ve, vars)
    plt.show()

#crear y mostrar ruleta
ruleta = list(range(37))
print('Ruleta:\n',ruleta)

#declaro variables
fr_esperada = 1/37
prom_esperado = stats.mean(ruleta)
varianza_esperada = stats.variance(ruleta)
desvio_esperado = stats.stdev(ruleta)
lista_proms = []
lista_frs = []
lista_ds = []
lista_vs = []

nro = int(input('Ingrese numero a apostar: '))
tiradas = int(input('Ingrese cantidad de tiradas: '))
corridas = int(input('Ingrese cantidad de corridas: '))


for j in range(0, corridas):
    lista = []
    promedios = []
    frec_relativas = []
    varianzas = []
    desvios = []
    cant = 0
    var=0
    acum_var=0
    n = 1

    for i in range(0, tiradas):
        lista.append(random.randint(0,36))
        acum = sum(lista)
        promedios.append(acum/len(lista))
    lista_proms.append(promedios)
    for l in range(0, len(lista)):
        if lista[l] == nro:
            cant += 1
        frec_relativas.append(cant/(l+1))
        acum_var = acum_var + (lista[l]-prom_esperado)**2
        if n != 1:
            var = acum_var/(n-1)
            varianzas.append(var)
            desvios.append(math.sqrt(var))
        n += 1
    lista_frs.append(frec_relativas)
    lista_ds.append(desvios)
    lista_vs.append(varianzas)

    print('Corrida {}: {}'.format(j+1, lista))
print('Lista de promedios:', lista_proms)
print('Lista de frecuencias relativas:', lista_frs)
print('Lista de desvios estandar:', lista_ds)
print('Lista de varianzas:', lista_vs)

lista_pe = [prom_esperado for i in range(0,len(lista))]
lista_fre = [fr_esperada for i in range(0,len(lista))]
lista_de = [desvio_esperado for i in range(0,len(lista))]
lista_ve = [varianza_esperada for i in range(0,len(lista))]

plot_todo(lista_pe, lista_proms, lista_fre, lista_frs, lista_de, lista_ds, lista_ve, lista_vs)



