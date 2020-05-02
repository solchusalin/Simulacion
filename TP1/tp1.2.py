import random
import matplotlib.pyplot as plt

def menu():
    print('Bienvenidos al juego de la ruleta!')
    juega = True
    while juega:
        estrategia = int(input('\nEstrategias: \n1. Martingala \n2. Sistema Zeta \n0. Salir\nEstrategia elegida: '))
        if estrategia == 1:
            martingala()
        elif estrategia == 2:
            zeta()
        elif estrategia == 0:
            print('\nGracias por jugar! Vuelva pronto')
            break


def plot_martingala(capitales, opc, ci, mi, cap_ini):
    plt.figure(figsize=(12,6))
    plt.title('Martingala - Capital {}'.format(opc))
    plt.xlabel('N')
    plt.ylabel('cc')
    if opc == 1:
        opc = 'acotado'
        plt.plot(ci, label="Capital inicial ${}".format(cap_ini))
        for i in range(0, len(capitales)):
            plt.plot(capitales[i], label="Apuesta inicial ${}".format(mi[i]))
    else:
        opc = 'infinito'
        plt.plot(ci, label="Capital inicial")
        for i in range(0, len(capitales)):
            plt.plot(capitales[i], label="Apuesta inicial ${}".format(mi[i]))
    plt.title('Martingala - Capital {}'.format(opc))
    plt.legend(prop = {'size': 7})
    plt.show()


def plot_zeta(capitales, opc, ci, mi, cap_ini):
    plt.figure(figsize=(12,6))
    plt.xlabel('N')
    plt.ylabel('cc')
    if opc == 1:
        opc = 'acotado'
        plt.plot(ci, label="Capital inicial ${}".format(cap_ini))
        for i in range(0, len(capitales)):
            plt.plot(capitales[i], label="Apuesta inicial ${}".format(mi[i]))
    else:
        opc = 'infinito'
        plt.plot(ci, label="Capital inicial")
        for i in range(0, len(capitales)):
            plt.plot(capitales[i], label="Apuesta inicial ${}".format(mi[i]))
    plt.title('Sistema Zeta - Capital {}'.format(opc))
    plt.legend(prop = {'size': 7})
    plt.show()


def martingala():
    print('\nElegiste Martingala')
    rojos = [1,3,5,7,9,12,14,18,16,19,21,23,25,27,30,32,34,36]
    negros = [2,4,6,8,10,11,13,15,17,20,24,22,26,29,28,31,33,35]
    apuesta = int(input('Apuestas:\n1. Par \n2. Impar\n3. Rojo\n4. Negro\nApuesta elegida: '))
    opc = int(input('Capital 1. Acotado o 2. Infinito?: '))
    corridas = int(input('Ingrese cantidad de corridas: '))
    if opc == 1:
        lista_caps = []
        mi = []
        for x in range(0, corridas):
            caps = []
            nros = []
            print('\nCorrida ',x+1)
            capital = int(input('Ingrese capital: '))
            capital_inicial = capital
            dinero_apuesta = int(input('Ingrese monto a apostar: '))
            monto_inicial = dinero_apuesta
            monto_maximo = monto_inicial*10
            mi.append(monto_inicial)
            caps.append(capital)
            while capital >= dinero_apuesta:
                nro_ruleta = random.randint(0,36)
                nros.append(nro_ruleta)
                if (nro_ruleta % 2 == 0 and apuesta == 2) or (nro_ruleta % 2 != 0 and apuesta == 1) or (nro_ruleta in rojos and apuesta == 4) or (nro_ruleta in negros and apuesta == 3) or nro_ruleta == 0:
                    capital -= dinero_apuesta
                    caps.append(capital)
                    dinero_apuesta = dinero_apuesta*2
                    if dinero_apuesta > monto_maximo:
                        dinero_apuesta = monto_inicial
                elif (nro_ruleta % 2 == 0 and apuesta == 1) or (nro_ruleta % 2 != 0 and apuesta ==2) or (nro_ruleta in rojos and apuesta == 3) or (nro_ruleta in negros and apuesta == 4):
                    capital += dinero_apuesta
                    caps.append(capital)
                    dinero_apuesta = monto_inicial
            print('\nSalieron los numeros:',nros)
            print('\nFlujo de caja:',caps)
            lista_caps.append(caps)
        lens = [len(cap) for cap in lista_caps]
        ci = [capital_inicial for c in range(0,max(lens))]
        plot_martingala(lista_caps, opc, ci, mi, capital_inicial)

    elif opc == 2:
        lista_caps = []
        mi = []
        for x in range(0, corridas):
            caps = []
            nros = []
            capital = 0
            print('\nCorrida ',x+1)
            dinero_apuesta = int(input('Ingrese monto a apostar: '))
            monto_inicial = dinero_apuesta
            monto_maximo = monto_inicial*10
            mi.append(monto_inicial)
            caps.append(capital)
            for i in range(5000):
                nro_ruleta = random.randint(0,36)
                nros.append(nro_ruleta)
                if (nro_ruleta % 2 == 0 and apuesta == 2) or (nro_ruleta % 2 != 0 and apuesta == 1) or (nro_ruleta in rojos and apuesta == 4) or (nro_ruleta in negros and apuesta == 3) or nro_ruleta == 0:
                    capital -= dinero_apuesta
                    caps.append(capital)
                    dinero_apuesta = (dinero_apuesta*2)
                    if dinero_apuesta > monto_maximo:
                        dinero_apuesta = monto_inicial
                elif (nro_ruleta % 2 == 0 and apuesta == 1) or (nro_ruleta % 2 != 0 and apuesta == 2) or (nro_ruleta in rojos and apuesta == 3) or (nro_ruleta in negros and apuesta == 4):
                    capital += dinero_apuesta
                    caps.append(capital)
                    dinero_apuesta = monto_inicial
            print('\nSalieron los numeros ',nros)
            print('\nFlujo de caja:',caps)
            lista_caps.append(caps)
        lens = [len(cap) for cap in lista_caps]
        ci = [0 for c in range(0,max(lens))]
        plot_martingala(lista_caps, opc, ci, mi, 0)

def zeta():
    print('\nElegiste el Sistema Zeta')
    columna1 = [1,4,7,10,13,16,19,22,25,28,31,34]
    columna2 = [2,5,8,11,14,17,20,23,26,29,32,35]
    columna3 = [3,6,9,12,15,18,21,24,27,30,33,36]
    fichas = [1,2,3,4,6]
    apuesta = int(input('Apuestas:\n1. 1ra columna\n2. 2da columna\n3. 3ra columna\nApuesta elegida: '))
    opc = int(input('Capital 1. Acotado o 2. Infinito?: '))
    corridas = int(input('Ingrese cantidad de corridas: '))
    if opc == 1:
        lista_caps = []
        mi = []
        for x in range(0, corridas):
            caps = []
            nros = []
            print('\nCorrida ',x+1)
            capital = int(input('Ingrese capital: '))
            capital_inicial = capital
            dinero_apuesta = int(input('Ingrese monto a apostar: '))
            monto_inicial = dinero_apuesta
            mi.append(monto_inicial)
            caps.append(capital)
            gano = False
            i = 0
            while capital >= dinero_apuesta:
                nro_ruleta = random.randint(0,36)
                nros.append(nro_ruleta)
                if (nro_ruleta in columna1 and apuesta != 1) or (nro_ruleta in columna2 and apuesta != 2) or (nro_ruleta in columna3 and apuesta != 3) or nro_ruleta == 0:
                    capital -= dinero_apuesta
                    caps.append(capital)
                    if i == 5:
                        i = 0
                    if gano:
                        i = 1
                    else:
                        dinero_apuesta = monto_inicial*fichas[i]
                        i += 1
                    gano = False

                elif (nro_ruleta in columna1 and apuesta == 1) or (nro_ruleta in columna2 and apuesta == 2) or (nro_ruleta in columna3 and apuesta == 3):
                    capital += (dinero_apuesta*2)
                    caps.append(capital)
                    dinero_apuesta = monto_inicial
                    gano = True
            print('\nSalieron los numeros:',nros)
            print('\nFlujo de caja:',caps)
            lista_caps.append(caps)
        lens = [len(cap) for cap in lista_caps]
        ci = [capital_inicial for c in range(0,max(lens))]
        plot_zeta(lista_caps, opc, ci, mi, capital_inicial)

    elif opc == 2:
        lista_caps = []
        mi = []
        for x in range(0, corridas):
            caps = []
            nros = []
            capital = 0
            print('\nCorrida ',x+1)
            dinero_apuesta = int(input('Ingrese monto a apostar: '))
            monto_inicial = dinero_apuesta
            mi.append(monto_inicial)
            caps.append(capital)
            gano = False
            i = 0
            j = 1
            while j < 5000:
                nro_ruleta = random.randint(0,36)
                nros.append(nro_ruleta)
                if (nro_ruleta in columna1 and apuesta != 1) or (nro_ruleta in columna2 and apuesta != 2) or (nro_ruleta in columna3 and apuesta != 3) or nro_ruleta == 0:
                    capital -= dinero_apuesta
                    caps.append(capital)
                    if i == 5:
                        i = 0
                    if gano:
                        i = 1
                    else:
                        dinero_apuesta = monto_inicial*fichas[i]
                        i += 1
                    gano = False

                elif (nro_ruleta in columna1 and apuesta == 1) or (nro_ruleta in columna2 and apuesta == 2) or (nro_ruleta in columna3 and apuesta == 3):
                    capital += (dinero_apuesta*2)
                    caps.append(capital)
                    dinero_apuesta = monto_inicial
                    gano = True
                j += 1
            print('\nSalieron los numeros:',nros)
            print('\nFlujo de caja:',caps)
            lista_caps.append(caps)
        lens = [len(cap) for cap in lista_caps]
        ci = [0 for c in range(0,max(lens))]
        plot_zeta(lista_caps, opc, ci, mi, 0)


#main
menu()
