"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import listiterator as li
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initialize():
    diccionario={
        'audio-events': None,
        'artists':None,
        'songs':None,
        'user-events':None,
        'energy':None,
        'danceability':None
    }
    diccionario["audio-events"]=lt.newList("ARRAY_LIST")
    diccionario["artists"]=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)
    diccionario["songs"]=om.newMap(omaptype='RBT',comparefunction=compareBySongId)
    diccionario['user-events']=lt.newList('ARRAY_LIST')
    diccionario['energy']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario['danceability']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    return diccionario

# Funciones para agregar informacion al catalogo
def add_audio_event(diccionario,audio_event):
    lt.addLast(diccionario["audio-events"],audio_event)
    update_artist(diccionario,audio_event)
    update_song(diccionario,audio_event)
    update_energy(diccionario,audio_event)
    
def add_user_event(diccionario,audio_event):
    lt.addLast(diccionario['user-events'],audio_event)
# Funciones para creacion de datos

def update_artist(diccionario,audio_event):
    id=audio_event['artist_id']
    p=om.contains(diccionario['artists'],id)
    if not p:
        create_artist(diccionario,audio_event) 
    else:
        insert_event(diccionario,audio_event)

def update_song(diccionario,audio_event):
    id=audio_event['track_id']
    p=om.contains(diccionario['songs'],id)
    if not p:
        create_song(diccionario,audio_event)
    else:
        insert_song(diccionario,audio_event)
def update_energy(diccionario,audio_event):
    id=audio_event['energy']
    p=om.contains(diccionario['energy'],id)
    if not p:
        create_energy(diccionario,audio_event)
    else:
        insert_energy(diccionario,audio_event)
def create_artist(diccionario,audio_event):
    lista=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(lista,audio_event)
    om.put(diccionario['artists'],audio_event['artist_id'],lista)

def insert_event(diccionario,audio_event):
    couple=om.get(diccionario['artists'],audio_event['artist_id'])
    lista=me.getValue(couple)
    lt.addLast(lista,audio_event)
    om.put(diccionario['artists'],audio_event['artist_id'],lista)

def create_song(diccionario,audio_event):
    lista=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(lista,audio_event)
    om.put(diccionario['songs'],audio_event['track_id'],lista)

def insert_song(diccionario,audio_event):
    couple=om.get(diccionario['songs'],audio_event['track_id'])
    lista=me.getValue(couple)
    lt.addLast(lista,audio_event)
    om.put(diccionario['songs'],audio_event['track_id'],lista)

def create_energy(diccionario,audio_event):
    lista=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(lista,audio_event)
    om.put(diccionario['energy'],audio_event['energy'],lista)

def insert_energy(diccionario,audio_event):
    couple=om.get(diccionario['energy'],audio_event['energy'])
    lista=me.getValue(couple)
    lt.addLast(lista,audio_event)
    om.put(diccionario['energy'],audio_event['energy'],lista)
"""
def create_danceability(diccionario,audio_event):
    lista=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(lista,audio_event)
    om.put(diccionario['danceability'],audio_event['danceability'],lista)

def insert_danceability(diccionario,audio_event):
    couple=om.get(diccionario['danceability'],audio_event['danceability'])
    lista=me.getValue(couple)
    lt.addLast(lista,audio_event)
    om.put(diccionario['danceability'],audio_event['danceability'],lista)
"""
# Funciones de consulta
def events_size(diccionario):
    return lt.size(diccionario['audio-events'])
def artists_size(diccionario):
    return om.size(diccionario['artists'])
def songs_size(diccionario):
    return om.size(diccionario['songs']) 
# Funciones utilizadas para comparar elementos dentro de una lista
def compareSongIdBinary(song1,song2):
    return song1['track_id']>song2['track_id']
def compareBySongId(song1,song2):
    e1=song1.lower()
    e2=song2.lower()
    if e1==e2:
        return 0
    elif e1>e2:
        return 1
    else:
        return -1
def compareByArtistidBinary(artist1,artist2):
    return artist1.lower()>artist2.lower()
def compareByArtistid(artist1,artist2):
    e1=artist1.lower()
    e2=artist2.lower()
    if e1==e2:
        return 0
    elif e1>e2:
        return 1
    else:
        return -1
def compareByFeature(e1,e2):
    e1=float(e1)
    e2=float(e2)
    if e1==e2:
        return 0
    elif e1>e2:
        return 1
    else:
        return -1
# Funciones de ordenamiento


def requerimiento1(diccionario,feature,minm,maxm):
    minm=float(minm)
    maxm=float(maxm)
    feature=feature.lower()
    diccionario[feature]=om.newMap(omaptype='RBT',comparefunction=compareByFeature) #creación RBT
    iterador=li.newIterator(diccionario['audio-events'])
    while li.hasNext(iterador):
        event=li.next(iterador)
        id=float(event[feature])
        
        p=om.contains(diccionario[feature],id)          #se verifica si el rbt contiene el valor de la caracteristica correspondiente
        if not p:                                           #si no lo tiene, se crea un nodo con llave el valor de esa caracteristica
            lista=lt.newList(datastructure='ARRAY_LIST')    # y su valor una lista con el evento correspondiente
            lt.addLast(lista,event)
        else:
            couple=om.get(diccionario[feature],id)              # si ya lo contiene, se agrega a la lista, el evento correspondiente
            lista=me.getValue(couple)
            lt.addLast(lista,event)
        om.put(diccionario[feature],id,lista)

    values=om.values(diccionario[feature],minm,maxm)
    total=0

    artistas=lt.newList(datastructure='ARRAY_LISTS')
    for lista in lt.iterator(values):                   
        total+=lt.size(lista)                       #se cuenta el tamaño de la lista de cada nodo
        for evento in lt.iterator(lista):
            lt.addLast(artistas,evento['artist_id'])        #se añade a una lista los artistas de cada uno de los eventos
    
    artistas_ordenados=ms.sort(artistas,compareByArtistidBinary)        #estos artistas son ordenados, de tal manera que los mismos artistas queden consecutivos
    
    artistas_final=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(artistas_final,lt.firstElement(artistas_ordenados))

    for evento in lt.iterator(artistas_ordenados):      #el bucle sirve para añadir a una nueva lista cada uno de los artistas a lo sumo una vez
        if evento!=lt.lastElement(artistas_final):
            lt.addLast(artistas_final,evento)
    size=lt.size(artistas_final)

    return total,size


def requerimiento2(diccionario,mine,maxe,mind,maxd):
    mine=float(mine)
    maxe=float(maxe)
    mind=float(mind)
    maxd=float(maxd)
    values=om.values(diccionario['energy'],mine,maxe)
    
    lista_total=lt.newList(datastructure='ARRAY_LIST')



    suma=0
    for lista in lt.iterator(values):
        suma+=lt.size(lista)
        for evento in lt.iterator(lista):
            if mind<=float(evento['danceability'])<=maxd :
                lt.addLast(lista_total,evento)
    #print(suma)
    #print(lt.size(lista_total))
    
    ordenada=ms.sort(lista_total,compareSongIdBinary)#se ordena segun el id de la canción, de tal manera que las
                                                     # mismas canciones queden consecutivas

    
    lista_final=lt.newList(datastructure='ARRAY_LIST')
    
    lt.addLast(lista_final,lt.lastElement(lista_total))
    iterador3=li.newIterator(ordenada)

    while li.hasNext(iterador3):
        event=li.next(iterador3)
        comparador=lt.lastElement(lista_final)
        if event['track_id'] != comparador['track_id']:
            lt.addLast(lista_final,event)

    size=lt.size(lista_final)
    return size, lista_final


def requerimiento4():