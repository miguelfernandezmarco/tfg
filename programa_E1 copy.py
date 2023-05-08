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
    #crea el grafo a partir del csv con ORIGEN,DESTINO,TIEMPO,LINEA,ESPERA
    nombre_archivo = "E1_grafo.csv"
    frecuencias=frec_paso()
    grafo={}
    csv_a_lista=list()
    with open(nombre_archivo, "r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        for fila in lector:
            if fila[0] in grafo.keys():
                grafo[fila[0]].append((fila[1],float(fila[2])+frecuencias[fila[3]],fila[3],frecuencias[fila[3]]))
            else: grafo[fila[0]]=[(fila[1],float(fila[2])+frecuencias[fila[3]],fila[3],frecuencias[fila[3]])]
            #csv_a_lista.append([fila[0],fila[1],fila[2],fila[3]])
    return grafo

def todas_las_paradas():
    grafo=crea_grafo()
    lista_paradas=[]
    for p in grafo:
        lista_paradas.append(p)
    return lista_paradas

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
        for neighbor, weight,line,waiting in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecesors[neighbor] = (current_node,line,waiting)
                heapq.heappush(unvisited, (distance,neighbor))

    return distances, predecesors

    


def como_ir(o,d):
    dist,pred=dijkstra(o)
    referencia=d
    faltan_pasos=True
    lineas_usadas=[]
    tespera=[]
    tiempos=[]
    tiempos_acc=0
    print("Parada de origen: "+o+" >>")
    while faltan_pasos:
        tiempos.append(dist[referencia])
        lineas_usadas.append(pred[referencia][1])
        tespera.append(pred[referencia][2])
        referencia=pred[referencia][0]
        if referencia==o: faltan_pasos=False

    num_lineas=len(lineas_usadas)
    for i in range(num_lineas):
        print("Línea "+lineas_usadas[num_lineas-i-1][:-1]+" Esperar "+str(int(tespera[num_lineas-i-1]))+" min | Tiempo de recorido: "+str(int(tiempos[num_lineas-i-1]-tiempos_acc-tespera[num_lineas-i-1]))+" min >> ")
        tiempos_acc = tiempos[num_lineas-i-1]


def simulacion():
    N=10000
    datos=[]
    paradas=todas_las_paradas()
    out="simulacionE1.csv"
    with open(out, "w") as outFile:
        writer = csv.writer(outFile, delimiter=';')
        writer.writerow(["Parada origen","Parada destino","Total (min)","En autobús (min)","A pie (min)","Esperas (min)","Veh. usados","Uso de línea ortogonal?","Uso de V+H?","Espera por vehículo","Lineas"])
        for i in range(N):
            o=paradas[int(random.random()*len(paradas))]
            d=paradas[int(random.random()*len(paradas))]
            while d==o: d=paradas[int(random.random()*len(paradas))]
            dist,pred=dijkstra(o)
            tiempototal=dist[d]

            tiempopie=0
            tiempobus=0
            tesperas=0
            vehusados=0
            lineasusadas=[]
            lineaV=0
            lineaH=0
            lineaortog=0

            referencia=d
            faltan_pasos=True
            lineas_usadas=[]
            tespera=[]
            tiempos=[]
            tiempos_acc=0

            while faltan_pasos:
                tiempos.append(dist[referencia])
                lineas_usadas.append(pred[referencia][1])
                tespera.append(pred[referencia][2])
                referencia=pred[referencia][0]
                if referencia==o: faltan_pasos=False

            num_lineas=len(lineas_usadas)
            for i in range(num_lineas):
                if lineas_usadas[num_lineas-i-1] == "APIE":
                    tiempopie += float(tiempos[num_lineas-i-1]-tiempos_acc)

                else:
                    tiempobus += float(tiempos[num_lineas-i-1]-tiempos_acc-tespera[num_lineas-i-1])
                    vehusados += 1
                    tesperas += float(tespera[num_lineas-i-1])
                    lineasusadas.append(lineas_usadas[num_lineas-i-1][:-1])
                    if "V" in lineas_usadas[num_lineas-i-1][:-1]:
                        lineaV=1
                        lineaortog=1
                    if "H" in lineas_usadas[num_lineas-i-1][:-1]:
                        lineaH=1
                        lineaortog=1
                    if "D" in lineas_usadas[num_lineas-i-1][:-1]:
                        lineaortog=1
                    
                #texto="Línea "+lineas_usadas[num_lineas-i-1][:-1]+" Esperar "+str(int(tespera[num_lineas-i-1]))+" min | Tiempo de recorido: "+str(int(tiempos[num_lineas-i-1]-tiempos_acc-tespera[num_lineas-i-1]))+" min >> "
                tiempos_acc = tiempos[num_lineas-i-1]

            if vehusados>0: espera_por_vehiculo=tesperas/vehusados
            else: espera_por_vehiculo=0
        
            writer.writerow([o,d,str(tiempototal).replace(".",","),str(tiempobus).replace(".",","),str(tiempopie).replace(".",","),str(tesperas).replace(".",","),vehusados,lineaortog,lineaV*lineaH,str(espera_por_vehiculo).replace(".",","),lineasusadas])
        
              
        
        
    
    


        
