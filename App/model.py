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
        'user-events':None
    }
    diccionario["audio-events"]=lt.newList("ARRAY_LIST")
    diccionario["artists"]=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)
    diccionario["songs"]=om.newMap(omaptype='RBT',comparefunction=compareBySongId)
    diccionario['user-events']=lt.newList('ARRAY_LIST')
    return diccionario

# Funciones para agregar informacion al catalogo
def add_audio_event(diccionario,audio_event):
    lt.addLast(diccionario["audio-events"],audio_event)
    update_artist(diccionario,audio_event)
    update_song(diccionario,audio_event)
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
    
# Funciones de consulta
def events_size(diccionario):
    return lt.size(diccionario['audio-events'])
def artists_size(diccionario):
    return om.size(diccionario['artists'])
def songs_size(diccionario):
    return om.size(diccionario['songs']) 
# Funciones utilizadas para comparar elementos dentro de una lista
def compareBySongId(song1,song2):
    e1=song1.lower()
    e2=song2.lower()
    if e1==e2:
        return 0
    elif e1>e2:
        return 1
    else:
        return -1
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
    diccionario[feature]=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    iterador=li.newIterator(diccionario['audio-events'])
    
    while li.hasNext(iterador):
        event=li.next(iterador)
        id=float(event[feature])
        
        p=om.contains(diccionario[feature],id)
        if not p:
            lista=lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(lista,event)
        else:
            couple=om.get(diccionario[feature],id)
            lista=me.getValue(couple)
            lt.addLast(lista,event)
        om.put(diccionario[feature],id,lista)
    values=om.values(diccionario[feature],minm,maxm)

    total=0

    iterador2=li.newIterator(values)
    while li.hasNext(iterador2):
        lista=li.next(iterador2)
        size=lt.size(lista)
        total+=size

    return total

