import csv
import os

def crea_recorridos():
    #a partir del archivo escenarios.csv, genera recorridos.csv

    #0 -> 0 codigo parada
    #1 -> codigo area int
    #4 -> 1 dist
    #5 -> 2 codigo linea
    #8 -> 3 punto geogr x
        # 4 punto geogr y

    
    nombre_archivo = "E1.csv"
    out="E1_grafo.csv"
    
    with open(nombre_archivo, "r") as archivo, open(out, "w") as outFile:
        lector = csv.reader(archivo, delimiter=",")
        writer = csv.writer(outFile, delimiter=',')
        lista=list()
        #next(lector, None)
        for fila in lector:
            lista.append([fila[0],fila[1],fila[2],fila[3],fila[4]])

        long=len(lista)

        lista_paradas=[]

        #creamos recorridos en autobús
        for o in range(len(lista)):
            d=o+1
            dist=0
            linea=lista[o][2] #ej: D20I
            while linea == lista[d][2]:
                num_paradas=d-o
                #print(num_paradas)
                dist += float(lista[d][1])
                nuevo_rec=[lista[o][0], lista[d][0], dist_a_tiempo(dist,num_paradas), linea]
                writer.writerow(nuevo_rec)
                d += 1
                if d==long-1: break
            if d==long-1: break


        #creamos recorridos a pie (entre todas las paradas cuya distancia sea menor de 3000m)
        for o in range(len(lista)):
            for d in range(len(lista)):
                dist=coord_a_metros(lista[o][3],lista[o][4],lista[d][3],lista[d][4])
                if caminable(dist):
                    nuevo_rec=[lista[o][0], lista[d][0], dist/75, "APIE"]
                    writer.writerow(nuevo_rec)
##            

        #out: ORIGEN, DESTINO, TIEMPO, LINEA

        
    



def dist_a_tiempo(dist, num_paradas):
    #pasa un recorrido de distancia a tiempo
    
    #unidades de tiempo -> min
    #unidades de distancia -> metro

    t_cd_parada=0.5 #tiempo de carga y descarga de pasajeros por parada
    t_semaf=0.4 #tiempo de espera por semáforo
    t_ad=0.11 #tiempo perdido en acelerar y decelerar al parar (en semáforo o parada)
    prop_sem=0.4 #proporción de semáforos en los que para un autobús
    prop_par=0.95 #proporción de paradas en las que para un autobús
    dist_sem=150 #distancia entre semáforos
    t_seg=2 #tiempo de seguridad
    vel=450 #velocidad de crucero del autobús


    t_total_parada=prop_par*num_paradas*(t_ad+t_cd_parada)
    #tiempo total perdido en las paradas
    
    t_total_semaf=(dist/dist_sem)*prop_sem*(t_ad+t_semaf)
    #tiempo total perdido en los semáforos

    t=dist/vel+t_total_parada+t_total_semaf
    #tiempo total del recorrido

    return t



def coord_a_metros(x_o, y_o, x_d, y_d):
    #return (abs(float(x_d)-float(x_o))*83221.15+abs(float(y_d)-float(y_o))*111111)
    return (abs(float(x_d)-float(x_o))*111111+abs(float(y_d)-float(y_o))*111111)

def caminable(dist):
    if dist < 1500 and dist!=0: return True
    else: return False
        
    
    
    
    
    
