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
    diccionario["audio-events"]=mp.newMap(maptype='PROBING',numelements=60000,loadfactor=0.5)
    diccionario["artists"]=mp.newMap(maptype='PROBING',numelements=11000,loadfactor=0.5)
    diccionario["songs"]=mp.newMap(maptype='CHAINING',numelements=31000,loadfactor=2.0)
    diccionario['user-events']=lt.newList('ARRAY_LIST')
    diccionario['energy']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario['danceability']=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario["tempo"]=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    diccionario["tempo-artists"]=om.newMap(omaptype='RBT',comparefunction=compareByFeature)
    

    
    
    #create_tempo(diccionario)
    return diccionario

# Funciones para agregar informacion al catalogo
def add_audio_event(diccionario,audio_event):
    key=audio_event["user_id"]+audio_event["track_id"]+audio_event["created_at"]
    mp.put(diccionario["audio-events"],key,audio_event)
    update_artist(diccionario,audio_event)
    update_song(diccionario,audio_event)
    update_danceability(diccionario,audio_event)
    update_tempo(diccionario,audio_event)
    
    
def add_user_event(diccionario,audio_event):
    lt.addLast(diccionario['user-events'],audio_event)
# Funciones para creacion de datos
    




def update_artist(diccionario,audio_event):
    id=audio_event["artist_id"]
    mp.put(diccionario["artists"],id,audio_event)
  


def update_song(diccionario,audio_event):
    id=audio_event['track_id']
    mp.put(diccionario["songs"],id,audio_event)
def update_danceability(diccionario,audio_event):
    id=audio_event['danceability']
    p=om.contains(diccionario['danceability'],id)
    if not p:
        create_danceability(diccionario,audio_event)
    else:
        insert_danceability(diccionario,audio_event)
def create_artist(diccionario,audio_event):
    om.put(diccionario['artists'],audio_event['artist_id'],audio_event)
"""
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
def update_tempo(diccionario,audio_event):
    
    
    id=float(audio_event["tempo"])
    unique_id=audio_event["user_id"]+audio_event["track_id"]+audio_event["created_at"]
    artist_id=audio_event["artist_id"]



    contains=om.contains(diccionario["tempo"],id)
    if not contains:
        values=mp.newMap(maptype="PROBING",numelements=50,loadfactor=0.5)
        values_artists=mp.newMap(maptype='PROBING',numelements=20,loadfactor=0.5)
       
        
    else:
        couple=om.get(diccionario["tempo"],id)
        values=me.getValue(couple)

        couple2=om.get(diccionario["tempo-artists"],id)
        values_artists=me.getValue(couple2)


    mp.put(values_artists,artist_id,audio_event)
    mp.put(values,unique_id,audio_event)

    om.put(diccionario["tempo"],id,values)
    om.put(diccionario["tempo-artists"],id,values_artists)
    

   


# Funciones de consulta
def events_size(diccionario):
    return mp.size(diccionario['audio-events'])
def artists_size(diccionario):
    return mp.size(diccionario['artists'])
def songs_size(diccionario):
    return mp.size(diccionario['songs']) 
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
    iterador=mp.valueSet(diccionario['audio-events'])
    lista=lt.newList("ARRAY_LIST")
    artists=mp.newMap(maptype='PROBING',loadfactor=0.5,numelements=4000)
    
    
    for event in lt.iterator(iterador):
        if minm<=float(event[feature])<=maxm:
            lt.addLast(lista,event)
            mp.put(artists,event["artist_id"],event)
    size=lt.size(lista)
    artists_size=mp.size(artists)
            
            
    """
    diccionario[feature]=om.newMap(omaptype='RBT',comparefunction=compareByFeature) #creación RBT
    artistas=om.newMap(omaptype='RBT',comparefunction=compareByArtistid)#creación rbt artistas

                   #Forma alternativa con RBT
    print(1)
    
    for event in lt.iterator(iterador):
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
        
        if minm<=float(event[feature])<=maxm:
            artist_id=event["artist_id"]
            r=om.contains(artistas,artist_id)
            if not r:
                lista2=lt.newList(datastructure='ARRAY_LIST')
                lt.addLast(lista2,event)
            else:
                couple2=om.get(artistas,artist_id)
                lista2=me.getValue(couple2)
                lt.addLast(lista2,event)

            om.put(artistas,artist_id,lista2)
    
        
    values=om.values(diccionario[feature],minm,maxm)
    total=0

    for lista in lt.iterator(values):                   
        total+=lt.size(lista)                    #se cuenta el tamaño de la lista de cada nodo
        

    size=om.size(artistas)
    """
    return size,artists_size


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

def crear_generos():

    generos=mp.newMap(maptype='PROBING',numelements=9,loadfactor=0.5)
    lista=lt.newList()
    lt.addLast(lista,60)
    lt.addLast(lista,90)
    mp.put(generos,"reggae",lista)
    lista=lt.newList()
    lt.addLast(lista,70)
    lt.addLast(lista,100)
    mp.put(generos,"down-tempo",lista)
    lista=lt.newList()
    lt.addLast(lista,90)
    lt.addLast(lista,120)
    mp.put(generos,"chill-out",lista)
    lista=lt.newList()
    lt.addLast(lista,85)
    lt.addLast(lista,115)
    mp.put(generos,"hip-hop",lista)
    lista=lt.newList()
    lt.addLast(lista,120)
    lt.addLast(lista,125)
    mp.put(generos,"jazz and funk",lista)
    lista=lt.newList()
    lt.addLast(lista,100)
    lt.addLast(lista,130)
    mp.put(generos,"pop",lista)
    lista=lt.newList()
    lt.addLast(lista,60)
    lt.addLast(lista,80)
    mp.put(generos,"r&b",lista)
    lista=lt.newList()
    lt.addLast(lista,110)
    lt.addLast(lista,140)
    mp.put(generos,"rock",lista)
    lista=lt.newList()
    lt.addLast(lista,100)
    lt.addLast(lista,160)
    mp.put(generos,"metal",lista)
  
    return generos
def requerimiento4(diccionario,lista,nuevo):
    
    
    generos=crear_generos()

    total=lt.newList(datastructure='ARRAY_LIST')
    numeroartistas=lt.newList(datastructure='ARRAY_LIST')
    lista_artistas=lt.newList(datastructure='ARRAY_LIST')



    if lt.firstElement(nuevo)==True:
        rango=lt.newList()
        lt.addLast(rango,lt.getElement(nuevo,2))
        lt.addLast(rango,lt.getElement(nuevo,3))
        mp.put(generos,lt.lastElement(lista),rango)
    for categorias in lt.iterator(lista):
        
        values=diccionario["tempo"]
        
        
        couple=mp.get(generos,categorias)
        lista=me.getValue(couple)
        minm=lt.firstElement(lista)
        maxm=lt.lastElement(lista)

        range_events=om.values(values,minm,maxm)
        range_artists=om.values(diccionario["tempo-artists"],minm,maxm)

        size=0
        size_artists=0
        
        artists_map=mp.newMap(maptype="PROBING",numelements=100,loadfactor=0.5)
        for events in lt.iterator(range_events):
            size+=mp.size(events)

        for artists in lt.iterator(range_artists):
            lista=mp.keySet(artists)
            for artist in lt.iterator(lista):
                mp.put(artists_map,artist,artist)

        size_artists=mp.size(artists_map)

        
        lt.addLast(total,size)
        lt.addLast(numeroartistas,size_artists)
        lt.addLast(lista_artistas,mp.keySet(artists_map))

    return total,numeroartistas,lista_artistas


def requerimiento5():
    pass