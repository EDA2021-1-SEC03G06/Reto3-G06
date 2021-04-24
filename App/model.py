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
        'danceability':None,
        'tempo':None
    }
    diccionario["audio-events"]=lt.newList("ARRAY_LIST")
    diccionario["artists"]=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)
    diccionario["songs"]=om.newMap(omaptype='RBT',comparefunction=compareBySongId)
    diccionario['user-events']=lt.newList('ARRAY_LIST')
    diccionario['energy']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario['danceability']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario['tempo']=mp.newMap(numelements=10,maptype='CHAINING',loadfactor=1.0)
    
    create_tempo(diccionario)
    return diccionario

# Funciones para agregar informacion al catalogo
def add_audio_event(diccionario,audio_event):
    lt.addLast(diccionario["audio-events"],audio_event)
    update_artist(diccionario,audio_event)
    update_song(diccionario,audio_event)
    update_danceability(diccionario,audio_event)
    update_tempo(diccionario,audio_event)
    
    
def add_user_event(diccionario,audio_event):
    lt.addLast(diccionario['user-events'],audio_event)
# Funciones para creacion de datos
def create_tempo(diccionario):
    
    mp.put(diccionario['tempo'],'reggae',create_category(60,90))
    mp.put(diccionario['tempo'],'down-tempo',create_category(70,100))
    mp.put(diccionario['tempo'],'chill-out',create_category(90,120))
    mp.put(diccionario['tempo'],'hip-hop',create_category(85,115))
    mp.put(diccionario['tempo'],'jazz and funk',create_category(120,125))
    mp.put(diccionario['tempo'],'pop',create_category(100,130))
    mp.put(diccionario['tempo'],'r&b',create_category(60,80))
    mp.put(diccionario['tempo'],'rock',create_category(110,140))
    mp.put(diccionario['tempo'],'metal',create_category(100,160))
   
    
def create_category(min,max):
    diccionario=mp.newMap(2,maptype='CHAINING',loadfactor=1.0)
    lista=lt.newList(datastructure='ARRAY_LIST')
    listrango=lt.newList(datastructure='ARRAY_LIST')

    lt.addFirst(listrango,min)
    lt.addLast(listrango,max)

    mp.put(diccionario,'events',lista)
    mp.put(diccionario,'range',listrango)

    return diccionario



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
def update_danceability(diccionario,audio_event):
    id=audio_event['danceability']
    p=om.contains(diccionario['danceability'],id)
    if not p:
        create_danceability(diccionario,audio_event)
    else:
        insert_danceability(diccionario,audio_event)
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

def create_danceability(diccionario,audio_event):
    lista=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(lista,audio_event)
    om.put(diccionario['danceability'],audio_event['danceability'],lista)

def insert_danceability(diccionario,audio_event):
    couple=om.get(diccionario['danceability'],audio_event['danceability'])
    lista=me.getValue(couple)
    lt.addLast(lista,audio_event)
    om.put(diccionario['danceability'],audio_event['danceability'],lista)
def update_tempo(diccionario,audio_event):
    lista=mp.keySet(diccionario['tempo'])

    for feature in lt.iterator(lista):
        couple=mp.get(diccionario['tempo'],feature)
        p=me.getValue(couple)

        couple2=mp.get(p,'range')
        values=me.getValue(couple2)

        couple3=mp.get(p,'events')
        lista=me.getValue(couple3)

        minimo=lt.firstElement(values)
        maximo=lt.lastElement(values)
        if minimo<=float(audio_event['tempo'])<=maximo:
            lt.addLast(lista,audio_event)
        
        mp.put(p,'events',lista)
        mp.put(diccionario['tempo'],feature,p)
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
    return artist1['artist_id'].lower()>artist2['artist_id'].lower()
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
    artistas=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)#creación rbt artistas

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


    for lista in lt.iterator(values):                   
        total+=lt.size(lista)                    #se cuenta el tamaño de la lista de cada nodo
        for events in lt.iterator(lista):
            artist_id=events["artist_id"]
            r=om.contains(artistas,artist_id)
            if not r:
                lista2=lt.newList(datastructure='ARRAY_LIST')
                lt.addLast(lista2,events)
            else:
                couple2=om.get(artistas,artist_id)
                lista2=me.getValue(couple2)
                lt.addLast(lista2,events)

            om.put(artistas,artist_id,lista2)

    size=om.size(artistas)

    return total,size


def requerimiento2(diccionario,mine,maxe,mind,maxd):
    mine=float(mine)
    maxe=float(maxe)
    mind=float(mind)
    maxd=float(maxd)
    values=om.values(diccionario['danceability'],mind,maxd)
    
    lista_total=lt.newList(datastructure='ARRAY_LIST')



    suma=0
    for lista in lt.iterator(values):
        suma+=lt.size(lista)
        for evento in lt.iterator(lista):
            if mine<=float(evento['energy'])<=maxe :
                lt.addLast(lista_total,evento)
    #print(suma)
    #print(lt.size(lista_total))
    
    ordenada=ms.sort(lista_total,compareSongIdBinary)#se ordena segun el id de la canción, de tal manera que las
                                                     # mismas canciones queden consecutivas

    
    lista_final=lt.newList(datastructure='ARRAY_LIST')
    
    lt.addLast(lista_final,lt.firstElement(lista_total))
    iterador3=li.newIterator(ordenada)

    while li.hasNext(iterador3):
        event=li.next(iterador3)
        comparador=lt.lastElement(lista_final)
        if event['track_id'] != comparador['track_id']:
            lt.addLast(lista_final,event)

    size=lt.size(lista_final)
    return size, lista_final


def requerimiento4(diccionario,lista):
    total=lt.newList(datastructure='ARRAY_LIST')
    numeroartistas=lt.newList(datastructure='ARRAY_LIST')
    lista_artistas=lt.newList(datastructure='ARRAY_LIST')
    artistas=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)
    for categorias in lista:
        couple=mp.get(diccionario['tempo'], categorias)         #Se obtiene la tabla de hash cuyo 
        categoria=me.getValue(couple)
        
        couple2=mp.get(categoria,'events')
        eventos=me.getValue(couple2)
        size=lt.size(eventos)
        lt.addLast(total,size)

        for evento in lt.iterator(eventos):
            id=evento['artist_id']
            p=om.contains(artistas,id)

            if not p:
                lista2=lt.newList(datastructure='ARRAY_LIST')
                lt.addLast(lista2,evento)
            else:
                couple2=om.get(artistas,id)
                lista2=me.getValue(couple2)
                lt.addLast(lista2,evento)
            om.put(artistas,id,lista2)
            
        size_artists=om.size(artistas)
        ids_list=om.keySet(artistas)
        lt.addLast(numeroartistas,size_artists)
        lt.addLast(lista_artistas,ids_list)

    return total,numeroartistas,lista_artistas
    