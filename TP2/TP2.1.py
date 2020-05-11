import random
import math
import matplotlib.pyplot as plt
from scipy.stats import chi2
from matplotlib.pylab import hist, show
import statistics as stats
import collections

def menu():
    opc = 5
    while opc != 0:
        opc = int(input('\nMenu: \n1. Middle Square \n2. Generador Congruencial Lineal \n3. Generador de Python\n0. Salir \nIngrese una opción: '))
        if opc == 1:
            mid_square()
        elif opc == 2:
            gcl()
        elif opc == 3:
            random_py()

def pruebas(nums):
    rta = 5
    while rta != 0:
        rta = int(input('\nPruebas: \n1. Chi-cuadrado \n2. de Series \n3. Kolmogorov Smirnov \n0. Volver al menu principal \nIngrese una opción: '))
        if rta == 1:
            test_chi2(nums)
        elif rta == 2:
            test_series(nums)
        elif rta == 3:
            test_ks(nums)

def mid_square():
    dus = []
    seeds = []
    nums = []
    seed = int(input("Ingrese una semilla de 4 numeros: "))
    n = int(input("Ingrese cantidad de numeros a generar: "))
    for i in range(n):
        x = seed ** 2
        nums.append(x)
        if len(str(x)) < 8:
            x = str(x).zfill(8) 	#valor de 8 digitos para generar la nueva semilla
        xlist = list(str(x)) 		#convierto a lista para extraer despues las posiciones q necesito
        new_seed = xlist[2:-2]	#guardo los 4 digitos centrales
        seed = int(''.join(new_seed)) #paso lista a numero
        dus.append(seed/10000)
        seeds.append(seed)
    print('\nNúmeros generados: {}\nSemillas: {}\nDistribucion: {}'.format(nums,seeds,dus))

def gcl():
    dus = []
    nums = []
    print('\nGenerador Congruencial: Xi = (a * Xi-1 + c) mod m')
    seed = int(input('Ingrese valor de la semilla: '))
    a = int(input('Ingrese el valor de a: '))
    c = int(input('Ingrese el valor de c: '))
    m = int(input('Ingrese el valor de m: '))
    nums.append(seed)
    x = ((a * seed) + c) % m
    while x != seed:
        dus.append(x/m)
        nums.append(x)
        x = ((a * x) + c) % m
    print('\nNúmeros generados: {}\nDistribucion: {}'.format(nums,dus))
    maximo = max(nums)
    for i in range(0,len(nums)):
        nums[i] = (nums[i]/maximo)
    if (len(nums) == m):
        print('El periodo es completo')
    else:
        print('El periodo es incompleto')

    pruebas(nums)

def random_py():
    nums = []
    print('\nGenerador de Python')
    seed = int(input('Ingrese valor de la semilla: '))
    random.seed(seed)
    for i in range(100):
        num = random.random()
        nums.append(num)
    print(nums)
    '''hist(nums)
    plt.ylabel('frequencia')
    plt.xlabel('valores')
    plt.title('Histograma Uniforme')
    show()'''

    pruebas(nums)

def test_chi2(nums):
    print('\nPrueba Chi-Cuadrado: χ2 = k/n * Σ(fj - n/k)^2')
    k = 10
    freqs = [0 for i in range(k)]
    for i in range(1,k+1):
        max = i/k
        min = max - (1/k)
        for n in nums:
            if n < max and n >= min:
                #Si el numero esta en el rango, sumamos 1 a la frecuencia de ese rango
                freqs[i-1] += 1
    #χ2 = k/n * Σ(fj - n/k)^2
    n = len(nums)
    chi2exp = (k/n) * sum([(i-(n/k))**2 for i in freqs])
    print('χ2 experimento:', chi2exp)

    #alfa=0.05, 95%, grados de libertad=k-1
    chi_tabla = chi2.isf(0.05, k-1)
    print('χ2 critico:', chi_tabla)
    if (chi2exp < chi_tabla):
        print('\nLa hipótesis nula es aceptada. La distribución es uniforme según prueba de Chi-Cuadrado')
    else:
        print('\nLa hipótesis nula no es aceptada. La distribución no es uniforme según prueba de Chi-Cuadrado')


menu()
