import random
import math
import sys
import numpy as np
import matplotlib.pyplot as plt


def expon(rmean):
    u = random.random()
    x = -rmean * math.log(u)
    return x


def init():
    global Q_LIMIT, BUSY, IDLE, thetime, next_event_type, server_status, num_in_q, num_events, num_custs_delayed, area_num_in_q, area_server_status, time_arrival, time_last_event, time_next_event, total_of_delays
    Q_LIMIT = 10
    BUSY = 1    #ocupado
    IDLE = 0    #desocupado
    thetime = 0     #reloj del simulacion
    next_event_type = 0    #tipo de evento siguiente 
    server_status = IDLE    #estado del servidor
    num_in_q = 0    #num de clientes actualmente en cola
    num_events = 2      #num de tipos de eventos
    num_custs_delayed = 0     #num de clientes que completaron demora
    area_num_in_q = 0.0         #area debajo de Q(t) 
    area_server_status = 0.0    #area debajo de B(t)
    time_last_event = 0.0   #tiempo del ultimo evento
    time_next_event = [ 0, thetime + expon(1/mean_interarrival), 1e30]  #tiempo del siguiente evento de tipo 1 o 2
    time_arrival = []    #tiempo de arrivo de clientes a la cola
    total_of_delays = 0   #total de demoras completadas


def timing():
    global next_event_type, time_next_event, thetime, min_time_next_event, num_events 
    min_time_next_event = 1e29  #tiempo minimo del siguiente evento
    next_event_type = 0    #0 si no hay otro evento
    for i in range(1, num_events+1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
    if next_event_type == 0:
        print("Lista vacia en tiempo %f" % thetime)
        return 1
    else:
        thetime = min_time_next_event
        return 0


def arrive():
    global time_next_event, thetime, mean_interarrival, server_status, num_in_q, num_custs_delayed, mean_service, total_of_delays
    time_next_event[1] = thetime + expon(1/mean_interarrival)
    if server_status == BUSY:
        num_in_q += 1
        time_arrival.append(thetime)
    else:
        # delay = 0
        # total_of_delays += delay
        num_custs_delayed += 1
        server_status = BUSY
        time_next_event[2] = thetime + expon(1/mean_service)


def depart():
    global num_in_q, server_status, time_next_event, total_of_delays, time_arrival, num_custs_delayed, mean_service
    if num_in_q == 0:
        server_status = IDLE
        time_next_event[2] = 1e30
    else:
        delay = thetime - time_arrival.pop(0)
        total_of_delays += delay
        num_in_q -= 1
        num_custs_delayed += 1
        time_next_event[2] = thetime + expon(1/mean_service)


def grafico_pn(probs, p):  
    plt.title("Probabilidades de clientes en cola")
    plt.xlabel('n')
    plt.ylabel("Pn")
    plt.bar([x for x in range(len(probs))], [(p**i)*(1-p) for i in range(len(probs))], label = "Pn Esperada", color = "pink", width = 0.25)
    plt.bar([x+0.25 for x in range(len(probs))], probs, label = "Pn Observada", color = "c", width = 0.25)
    plt.xticks([x+0.15 for x in range(len(probs))], [x for x in range(len(probs))])
    plt.legend(loc='upper right', prop={'size': 7})
    plt.show()


def grafico_barras(proms, prom_esp, tit, ylbl):
    plt.title(tit)
    plt.xlabel('Corrida')
    plt.ylabel(ylbl)
    plt.bar([x for x in range(len(proms))], [prom_esp for i in range(len(proms))], label = "{} Esperada".format(ylbl), color = "r", width = 0.25)
    plt.bar([x+0.25 for x in range(len(proms))], proms, label = "{} Observada".format(ylbl), color = "b", width = 0.25)
    plt.xticks([x+0.15 for x in range(len(proms))], [x for x in range(len(proms))])
    plt.legend(loc='lower right', prop={'size': 7})
    plt.show()


def grafico_b_q(server_acum, time_acum, niq_acum):
    plt.subplot(211)    
    plt.step(time_acum, server_acum, color = "g")
    plt.fill_between(time_acum, server_acum, step="pre", alpha=0.5, color = "g")
    plt.title("Estado del servidor")
    plt.xlabel("t")
    plt.ylabel("B(t)")

    plt.subplot(212)
    plt.step(time_acum, niq_acum, color="m")
    plt.fill_between(time_acum, niq_acum, step="pre", alpha=0.5, color="m")
    plt.title("Longitud de la cola")
    plt.xlabel("t")
    plt.ylabel("Q(t)")
    plt.show()


def prob_deneg(probs):
    n0 = probs[0]
    print("Probabilidad de denegación de servicio con n = {0}: {1} %".format(0, (1-n0)*100))
    n2 = probs[0] + probs[1] + probs[2]
    print("Probabilidad de denegación de servicio con n = {0}: {1} %".format(2, (1-n2)*100))
    n5 = probs[0] + probs[1] + probs[2] + probs[3] + probs[4] + probs[5]
    print("Probabilidad de denegación de servicio con n = {0}: {1} %".format(5, (1-n5)*100))

# main()
mean_interarrival = 0.5    #lambda  
mean_service = 2         #mu
total_cus = 500           #total de demoras de clientes. condicion de finalizacion
util_esp = mean_interarrival/mean_service
lq_esp = util_esp**2/(1-util_esp)
wq_esp = lq_esp/mean_interarrival
ws_esp = wq_esp + 1/mean_service
ls_esp = mean_interarrival*ws_esp
den_serv = []
util_corridas, wq_corridas, lq_corridas, time_corridas, ws_corridas, ls_corridas, pn_corridas, niq_prob, niq_cont = [], [], [], [], [], [], [], [], [0]*50    #guardo los rdos de cada corrida para sacar los proms

print("Parametros: ====")
print("Tiempo medio entre arrivos: %.3f minutos" % (1/mean_interarrival))
print("Tiempo medio de servicio: %.3f minutos" % (1/mean_service))
print("Numero maximo de demoras de clientes: %d" % total_cus)

for i in range(10):
    init()
    time_acum, server_acum, niq_acum = [], [], []
    while num_custs_delayed < total_cus:
        t = timing()
        if t == 0:
        # update_time_avg_stats()
            time_since_last_event = thetime - time_last_event
            time_last_event = thetime
            time_acum.append(thetime)
            server_acum.append(server_status)
            niq_acum.append(num_in_q)
            area_num_in_q = area_num_in_q + (num_in_q * time_since_last_event)
            area_server_status = area_server_status + (server_status * time_since_last_event)

            if next_event_type == 1:
                arrive()
            elif next_event_type == 2:
                niq_cont[num_in_q] += 1
                depart()

        elif t == 1:
            break

    # report()
    grafico_b_q(server_acum, time_acum, niq_acum)
    ls_corridas.append(mean_interarrival * ((total_of_delays / num_custs_delayed) + (1/mean_service)))
    ws_corridas.append((total_of_delays / num_custs_delayed) + (1/mean_service))
    util_corridas.append(area_server_status / thetime)
    wq_corridas.append(total_of_delays / num_custs_delayed)
    lq_corridas.append(area_num_in_q / thetime) 
    time_corridas.append(thetime)
    print("\nReporte %d: ====" % (i+1))
    print("Cantidad de clientes que completaron demora %d" % num_custs_delayed)
    print("Tiempo promedio en el sistema %.3f" % ws_corridas[i]) #Ws
    print("Tiempo promedio en cola %.3f minutos" % wq_corridas[i])   #Wq
    print("Numero promedio de clientes en el sistema %.3f" % ls_corridas[i]) #Ls
    print("Numero promedio de clientes en cola %.3f" % lq_corridas[i])   #Lq
    print("Utilizacion del servidor %.3f " % util_corridas[i])    #p


for j in range(len(niq_cont)):
    if niq_cont[j] > 0:
        niq_prob.append(niq_cont[j]/sum(niq_cont))

print("\nPromedios de las corridas: ====")
print("Promedios de utilidad del servidor: ", np.mean(util_corridas))
print("Promedios de tiempos promedio en cola:", np.mean(wq_corridas))
print("Promedios de numeros promedio de clientes en cola:", np.mean(lq_corridas))
print("Promedios de tiempos en el sistema:", np.mean(ws_corridas))
print("Promedios de numeros promedio de clientes en el sistema:", np.mean(ls_corridas))
for j in range(len(niq_prob)):
    print('Probabilidad de que haya {0} clientes en cola: {1} %'.format(j, niq_prob[j]*100))  #Pn
print("Prob acumulada: ", sum(niq_prob))

print("\nValores esperados: ====")
print("Utilidad del servidor: ",util_esp)
print("Tiempo promedio en cola:", wq_esp)
print("Numero promedio de clientes en cola:",lq_esp)
print("Tiempo en el sistema:", ws_esp)
print("Numero promedio de clientes en el sistema:", ls_esp)

#prob_deneg(niq_prob)
grafico_pn(niq_prob, util_esp)
grafico_barras(util_corridas, util_esp, 'Utilización del servidor', 'B(t)')  #p
grafico_barras(wq_corridas, wq_esp, 'Tiempo promedio en cola', 'Dq(n)')    #Wq
grafico_barras(lq_corridas, lq_esp, 'Longitud promedio de la cola', 'Q(t)')    #Lq
grafico_barras(ws_corridas, ws_esp, 'Tiempo promedio en el sistema', 'Ds(n)')    #Ws
grafico_barras(ls_corridas, ls_esp, 'Longitud promedio en el sistema', 'S(t)')   #Ls