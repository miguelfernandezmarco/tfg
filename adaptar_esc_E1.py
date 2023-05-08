import csv
import os

nombre_archivo="Escenario4grafo.csv"
out="E4.csv"

with open(nombre_archivo, "r") as archivo, open(out, "w") as outFile:
        lector = csv.reader(archivo, delimiter=";")
        writer = csv.writer(outFile, delimiter=',')
        #next(lector, None) #activar para esc1

        for fila in lector:
            dist = fila[1].replace(",",".")
            coord=fila[5][7:-1]
            pos_sp=coord.find(" ")
            xcoord=coord[:8]
            ycoord=coord[pos_sp+1:pos_sp+9]

            if fila[4]=="1": linia=fila[3]+"I"
            else: linia=fila[3]+"V"

            writer.writerow([fila[0],dist,linia,xcoord,ycoord])

            
            
            
            

        
