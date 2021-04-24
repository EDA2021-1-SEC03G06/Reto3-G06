"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
import random
assert cf
def printMenu():
    print("Bienvenido")
    print("1-Inicializar catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Requerimiento 1: Caracterizar las reproducciones ")
    print("4- Requerimiento 2: Encontrar musica para festejar")
    print("5- Requerimiento 3: Encontrar musica para estudiar")
    print("6- Requerimiento 4: Estudiar los generos musicales")
    print("7- Requerimiento 5: Indicar el genero musical más escuchado en el tiempo")

def mostrar_categorias():
    print("1-Reggae")
    print("2-Down-Tempo")
    print("3-Chill-out")
    print("4-Hip-hop")
    print("5-Jazz and Funk")
    print("6-Pop")
    print("7-R&B")
    print("8-Rock")
    print("9-Metal")
    print("10-Ninguna opciòn adicional")

catalog = None

"""
Menu principal
"""
diccionario=None
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializar catalogo")
        diccionario=controller.initialize()
        
    elif int(inputs[0]) == 2:
        print("Cargando información en el catalogo.............")
        controller.loadData(diccionario)
        print("datos cargados correctamente")

        for i in range(1,6):
            video=lt.getElement(diccionario['audio-events'],i)
            print(i," : ",video)
        size=lt.size(diccionario['audio-events'])
        for i in range(size-5,size+1):
            video=lt.getElement(diccionario['audio-events'],i)
            print(i," :" ,video)
        print("Se han cargado un total de : ", controller.events_size(diccionario), " eventos de escucha")
        print(" Total de Autores : ", controller.artists_size(diccionario))
        print(" Total de canciones: ", controller.songs_size(diccionario))
    elif int(inputs[0])==3:
        caracteristica=input("indique la caracteristica de contenido")
        minm=(input("Indique el valor minimo"))
        maxm=(input("Indique el valor maximo"))
        lista=controller.requerimiento1(diccionario,caracteristica,minm,maxm)
        print("Cantidad total de eventos de escucha : " ,  lista[0])
        print("Cantidad total de artistas: " ,lista[1])
    elif int(inputs[0])==4:
        e1=float(input("Escriba el rango minimo para energía: "))
        e2=float(input("Escriba el rango maximo para energía: "))
        d1=float(input("Escriba el rango minimo para danceabilidad: "))
        d2=float(input("Escriba el rango maximo para danceabilidad: "))
        lista=controller.requerimiento2(diccionario,e1,e2,d1,d2)
        print(" La cantidad de canciones que cumnplene estas condiciones son : " ,lista[0])    

        for i in range(1,6):
            numero=random.randint(1,lt.size(lista[1]))
            evento=lt.getElement(lista[1],numero)
            print("Track",i," : ",evento['artist_id'], " with energy ", evento['energy']," and danceability : ", evento['danceability'] )

        
    elif int(inputs[0])==5:
       pass

            
    elif int(inputs[0])==6:
        lista=["reggae","down-tempo","chill-out","hip-hop","jazz and funk","pop","r&b","rock","metal"]
        salida=[]
        print("De cual de las siguientes categorias quiere conocer la cantidad reproducciones : ")
        bandera=True
        while bandera:
            mostrar_categorias()
            p=int(input())
            if p==10:
                bandera=False
            elif p<10:
                salida.append(lista[p-1])
        print("Cargando")
                
        variables=controller.requerimiento4(diccionario,salida)

        size=len(salida)

        for i in range(size):
            print(" Para la categoria  ", salida[i], " se obtuvieron: ", lt.getElement(variables[0],i+1), "reproducciones ")
            print(" Con ",lt.getElement(variables[1],i+1)," artistas")
            lista=lt.getElement(variables[2],i+1)
            tamaño_lista=lt.size(lista)
            for j in range(1,11):
                numero=random.randint(1,tamaño_lista)
                print("Artist",j," : ", lt.getElement(lista,numero)['artist_id'])
        
    else:
        sys.exit(0)
sys.exit(0)