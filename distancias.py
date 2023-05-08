import csv
import os

nombre_archivo = "Escenario4grafo.csv"
out="distanciasok.csv"
with open(nombre_archivo, "r") as archivo, open(out, "w") as outFile:
    lector = csv.reader(archivo, delimiter=";")
    writer = csv.writer(outFile, delimiter=';')
    linia_ant="XH1"
    sentit_ant="1"
    dist=0
    # Omitir el encabezado
    next(lector, None)
    for fila in lector:
        if fila[3]==linia_ant and fila[4]==sentit_ant:
            dist += float(fila[1].replace(",","."))
        else:
            writer.writerow([str(dist).replace(".",",")])
            dist=0
        linia_ant=fila[3]
        sentit_ant=fila[4]
        if fila[3][0]!="X": break

            
            
