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

def pruebas(uis):
    rta = 5
    while rta != 0:
        rta = int(input('\nPruebas: \n1. Chi-cuadrado \n2. de Series \n3. Kolmogorov Smirnov \n4. de Huecos\n0. Volver al menu principal \nIngrese una opción: '))
        if rta == 1:
            test_chi2(uis)
        elif rta == 2:
            test_series(uis)
        elif rta == 3:
            test_ks(uis)
        elif rta == 4:
            test_huecos(uis)

def mid_square():
    print('\nGenerador Cuadrado de los Medios')
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
    uis = []
    nums = []
    print('\nGenerador Congruencial Lineal')
    a = int(input('Ingrese el valor de a: '))
    seed = int(input('Ingrese valor de la semilla: '))
    c = int(input('Ingrese el valor de c: '))
    m = int(input('Ingrese el valor de m: '))
    nums.append(seed)
    uis.append(seed/m)
    x = ((a * seed) + c) % m
    while x != seed:
        uis.append(x/m)
        nums.append(x)
        x = ((a * x) + c) % m
    print('\nNúmeros generados: {}\nDistribucion: {}'.format(nums,uis))
    if (len(nums) == m):
        print('El periodo es completo')
    else:
        print('El periodo es incompleto')

    pruebas(uis)

def random_py():
    nums = []
    print('\nGenerador de Python')
    seed = int(input('Ingrese valor de la semilla: '))
    n = int(input('Ingrese cantidad de numeros a generar: '))
    random.seed(seed)
    for i in range(n):
        num = random.random()
        nums.append(num)
    print(nums)

    pruebas(nums)

def test_chi2(uis):
    print('\nPrueba Chi-Cuadrado')
    k = 10
    freqs = [0 for i in range(k)]
    for i in range(1,k+1):
        max = i/k
        min = max - (1/k)
        for u in uis:
            if u < max and u >= min:
                #Si el numero esta en el rango, sumamos 1 a la frecuencia de ese rango
                freqs[i-1] += 1
    #χ2 = k/n * Σ(fj - n/k)^2
    n = len(uis)
    chi2exp = (k/n) * sum([(i-(n/k))**2 for i in freqs])
    print('χ2 experimento:', chi2exp)

    #alfa=0.05, 95%, grados de libertad=k-1
    chi_tabla = chi2.isf(0.05, k-1)
    print('χ2 crítico:', chi_tabla)
    print('Frecuencias:', freqs)

    if (chi2exp < chi_tabla):
        print('\nLa hipótesis nula es aceptada. La distribución es uniforme según prueba de Chi-Cuadrado')
    else:
        print('\nLa hipótesis nula es rechazada. La distribución no es uniforme según prueba de Chi-Cuadrado')

def test_series(uis):
    print('\nPrueba de Series')
    k = int(math.sqrt(len(uis)))

    #Calculamos frecuencias absolutas. Crear el array bidimensional de las celdas con sus frecuencias
    freqs = [[0 for i in range(k)] for j in range(k)]
    fr_int = []

    #Para cada par de rangos (i,j)
    for i in range(1,k+1):
        maxI = i/k
        minI = maxI - (1/k)
        for j in range(1,k+1):
            maxJ = j/k
            minJ = maxJ - (1/k)
            for u in range(0, len(uis)-1):
                if uis[u] < maxI and uis[u] >= minI and uis[u+1] < maxJ and uis[u+1] >= minJ:
                #Si el primer elemento esta en el rango i, y el segundo en el j,
                #sumamos 1 a la frecuencia de esos rangos
                    freqs[i-1][j-1]+=1
    for j in range(0,k):
        cont = 0
        for i in range(0,k):
            cont += freqs[i][j]
        fr_int.append(cont)

    #χ2 = k/n * Σ(fj - n/k)^2
    n = len(uis)
    fe = (n-1)/k
    chi2exp = (1/fe) * sum([(i-fe)**2 for i in fr_int])

    print('χ2 experimento:', chi2exp)

    chi_tabla = chi2.isf(0.05, k-1)
    print('χ2 crítico:', chi_tabla)
    print('Frecuencias en cada celda:', freqs)
    print("Frecuencia observada en cada intervalo: ",fr_int)
    if (chi2exp < chi_tabla):
        print('\nLa hipótesis nula es aceptada. Los números son independientes según la prueba de Series')
    else:
        print('\nLa hipótesis nula es rechazada. Los números no son independientes según la prueba de Series')

def test_ks(uis):
    print("\nPrueba Kolmogorov-Smirnov")
    nums = sorted(uis)
    print(nums)
    n = len(nums)
    dmas = []
    dmenos = []
    for i in range(1,n+1):
        d1 = (i/n) - nums[i-1]
        d2 = nums[i-1] - ((i-1)/n)
        dmas.append(math.fabs(d1))
        dmenos.append(math.fabs(d2))
    dmas_max = max(dmas)
    dmenos_max = max(dmenos)
    d = max(dmas_max,dmenos_max)
    k = math.sqrt(n) + 0.12 + (0.11/math.sqrt(n))
    d_ks = 1.358/k  #grado de confianza de 95%-- valor sacado de la tabla
    print('D = {}\nD tabla = {}'.format(d,d_ks))
    if d > d_ks:
        print("\nLos números no siguen una distribución uniforme según la prueba Kolmogorov Smirnov")
    else:
        print("\nLos números siguen una distribución uniforme según la prueba Kolmogorov Smirnov")

def test_huecos(uis):
    print('\nPrueba de Huecos')
    posiciones = []
    for u in uis:
        if u >= 0 and u < 0.5:
            posiciones.append(1)
        else:
            posiciones.append(0)
    print('Arreglo de posiciones:', posiciones)
    huecos = []
    cont = 0
    for i in range(len(posiciones)-1):
        if posiciones[i] == 1:
            for j in range(i+1, len(posiciones)):
                if posiciones[j] == 1:
                    huecos.append(cont)
                    cont = 0
                else:
                    cont += 1
            break
    if len(huecos) == 0:
        print('\nNo se puede realizar la prueba. No hay números que pertenezcan al intervalo [0, 0.5)')
    else:
        print('Longitudes de los huecos:', huecos)
        hueco_max = max(huecos)
        if hueco_max > 10:
            hueco_max = 10
        print('Hueco máximo:', hueco_max)
        freq_obs = []
        for i in range(hueco_max+1):
            cont = 0
            for h in huecos:
                if h == i:
                    cont += 1
            freq_obs.append(cont)
        print('Frecuencias observadas:', freq_obs)
        freq_esp = []
        for i in range(hueco_max):
            freq_esp.append((1 - 0.5)**i * 0.5 * sum(freq_obs))
        freq_esp.append((1 - 0.5)**hueco_max * sum(freq_obs))
        print('Frecuencias esperadas:', freq_esp)
        if len(freq_obs)==1 and len(freq_esp) and int(freq_esp[0]) == freq_obs[0]:
            print('\nLa hipótesis nula es aceptada. Los números son independientes según prueba de Huecos')
        else:
            chi2exp = sum([(freq_esp[i] - freq_obs[i])**2 / freq_esp[i] for i in range(hueco_max+1)])
            print('χ2 experimento:', chi2exp)
            chi_tabla = chi2.isf(0.05, hueco_max-1)
            print('χ2 crítico:', chi_tabla)
            if (chi2exp < chi_tabla):
                print('\nLa hipótesis nula es aceptada. Los números son independientes según prueba de Huecos')
            else:
                print('\nLa hipótesis nula es rechazada. Los números no son independientes según prueba de Huecos')


menu()
