import csv
import os
import random
import heapq

def frec_paso():
    nombre_archivo = "ESC1.csv"
    dicc={}
    with open(nombre_archivo, "r") as archivo:
        lector = csv.reader(archivo, delimiter=";")
        next(lector, None)
        for fila in lector:
            if fila[4]=="SUMA": break
            if fila[2]=="1": sentido="I"
            else: sentido="V"
            dicc[fila[1]+sentido]=random.random()*float(fila[4])+1
    dicc["APIE"]=0
    return dicc


def crea_grafo():
    #crea el grafo a partir del csv con ORIGEN,DESTINO,TIEMPO,LINEA
    nombre_archivo = "E1_grafo.csv"
    frecuencias=frec_paso()
    grafo={}
    csv_a_lista=list()
    with open(nombre_archivo, "r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        for fila in lector:
            if fila[0] in grafo.keys():
                grafo[fila[0]].append((fila[1],float(fila[2])+frecuencias[fila[3]],fila[3],))
            else: grafo[fila[0]]=[(fila[1],float(fila[2])+frecuencias[fila[3]],fila[3])]
            #csv_a_lista.append([fila[0],fila[1],fila[2],fila[3]])
    return grafo

def dijkstra(start):
    graph=crea_grafo()
    linee=""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    predecesors = {}
    unvisited = [(0, start)]

    while unvisited:
        # Obtener el nodo no visitado con la distancia más corta del heap de prioridad.
        current_distance, current_node = heapq.heappop(unvisited)


        # Si el nodo actual ya ha sido visitado, saltar a la siguiente iteración.
        if current_distance > distances[current_node]:
            continue

        # Para cada vecino del nodo actual, calcular la distancia desde el nodo de inicio y actualizar si es menor.
        for neighbor, weight,line in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecesors[neighbor] = (current_node,line)
                heapq.heappush(unvisited, (distance,neighbor))

    return distances, predecesors

    


def como_ir(o,d):
    dist,pred=dijkstra(o)
    referencia=d
    faltan_pasos=True
    lineas_usadas=[]
    tiempos=[]
    tiempos_acc=0
    while faltan_pasos:
        tiempos.append(dist[referencia])
        lineas_usadas.append(pred[referencia][1])
        referencia=pred[referencia][0]
        if referencia==o: faltan_pasos=False

    num_lineas=len(lineas_usadas)
    for i in range(num_lineas):
        print(lineas_usadas[num_lineas-i-1][:-1]+" ("+str(int(tiempos[num_lineas-i-1]-tiempos_acc))+" min) >> ", end="")
        tiempos_acc = tiempos[num_lineas-i-1]
              
        
        
    
    


        
