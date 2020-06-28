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
    Q_LIMIT = 10000000
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
        sys.exit(1)
    thetime = min_time_next_event


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



# main()
mean_interarrival = 1    #lambda  
mean_service = 2         #mu
total_cus = 10000           #total de demoras de clientes. condicion de finalizacion
util_corridas, avgdel_corridas, avgniq_corridas, time_corridas = [], [], [], []     #guardo los rdos de cada corrida para sacar los proms

print("Parametros: ====")
print("Tiempo medio entre arrivos: %.3f minutos" % (1/mean_interarrival))
print("Tiempo medio de servicio: %.3f minutos" % (1/mean_service))
print("Numero maximo de demoras de clientes: %d" % total_cus)

for i in range(5):
    init()
    while num_custs_delayed < total_cus:
        timing()
        # update_time_avg_stats()
        time_since_last_event = thetime - time_last_event
        time_last_event = thetime
        area_num_in_q = area_num_in_q + (num_in_q * time_since_last_event)
        area_server_status = area_server_status + (server_status * time_since_last_event)

        if next_event_type == 1:
            arrive()
        elif next_event_type == 2:
            depart()
        else:
            sys.exit(4)

    # report()
    util_corridas.append(area_server_status / thetime)
    avgdel_corridas.append(total_of_delays / num_custs_delayed)
    avgniq_corridas.append(area_num_in_q / thetime) 
    time_corridas.append(thetime)
    print("\nReporte %d: ====" % (i+1))
    print("Cantidad de clientes que completaron demora %d" % num_custs_delayed)
    print("Demora promedio del cliente en cola %.3f minutos" % (total_of_delays / num_custs_delayed))
    print("Numero promedio del cliente en cola %.3f" % (area_num_in_q / thetime))
    print("Utilizacion del servidor %.3f " % (area_server_status / thetime))
    print("Tiempo en que finaliza la simulacion %.3f" % thetime)

print("\nPromedios de las corridas: ====")
print("Promedios de utilidad del servidor: ", np.mean(util_corridas))
print("Promedios de demoras prom del cliente en cola:", np.mean(avgdel_corridas))
print("Promedios de numeros promedio del cliente en cola:", np.mean(avgniq_corridas))
print("Promedios de tiempos en que finaliza la simulacion:", np.mean(time_corridas))

graficar(util_corridas, 0.5)
graficar(avgdel_corridas, 0.5)
graficar(avgniq_corridas, 0.5)

