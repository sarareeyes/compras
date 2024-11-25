import csv
from datetime import datetime,date
from typing import NamedTuple
from collections import Counter

Compra = NamedTuple('Compra',
                    [('dni', str),
                     ('supermercado', str),
                     ('provincia', str),
                     ('fecha_llegada', datetime),
                     ('fecha_salida', datetime),
                     ('total_compra', float)]
                    )

'''
dias_estrella: recibe una lista de tuplas de tipo Compra, un supermercado y una provincia, y devuelve una lista ordenada cronológicamente con las "fechas estrella" de ese supermercado en esa provincia. Se consideran "fechas estrella" aquellos días en los que el supermercado factura más que el día anterior y más que el día siguiente. (2 puntos)
Complete el código de las funciones de test del módulo compras_test.py para probar las funciones anteriores, teniendo en cuenta que la salida por consola de la ejecución de los test debe ser la siguiente. (1 punto)
'''

def lee_compras(fichero:str)->list[Compra]:
    '''recibe el nombre de un fichero y devuelve una lista de 
    tuplas de tipo Compra conteniendo todos los datos almacenados
    en el fichero. (1 punto) '''
    res=[]
    with open (fichero, encoding='Utf-8') as f:
        lector=csv.reader(f)
        next(lector)
        for dni,supermercado,provincia,fecha_llegada,fecha_salida,total_compra in lector:
            fecha_llegada=datetime.strptime(fecha_llegada,'%d,%m,%Y %H:%M')
            fecha_salida=datetime.strptime(fecha_salida,'%d,%m,%Y %H:%M')
            total_compra=float(total_compra)
            res.append(Compra(dni,supermercado,provincia,fecha_llegada,fecha_salida,total_compra))
    return res

def compra_maxima_minima_provincia(lista,provincia:str):
    '''recibe una lista de tuplas de tipo Compra y una provincia.
    Devuelve una tupla que contiene el importe máximo y el mínimo 
    de las compras que se han realizado en la provincia dada como 
    parámetro. Si la provincia toma el valor None, se devuelve una
    tupla con el importe máximo y el mínimo calculados a partir de
    todas las compras. (1 punto)'''
    importe=[elem.total_compra for elem in lista if provincia==None or provincia==elem.provincia]
    return (max(importe),min(importe))

def hora_menos_afluencia(lista):
    '''recibe una lista de tuplas de tipo Compra y devuelve una
    tupla con la hora en la que llegan menos clientes y el número 
    de clientes que llegan a dicha hora. (1,5 puntos)'''
    return Counter(elem.fecha_llegada.hour for elem in lista).most_common(24)[-1]

def supermercados_mas_facturacion(lista,n:3):
    '''recibe una lista de tuplas de tipo Compra y un número entero n,
con valor por defecto 3. Devuelve un ranking, es decir, una lista
de tuplas (posición_ranking, (supermercado, facturación)) con las 
n marcas de supermercados que más facturan, en orden decreciente 
de facturación. El ranking debe empezar por la posición 1. (1,5 puntos)'''
    supermercados_facturacion={}
    for compra in lista:
        [compra.supermercado] += compra.total_compra 
    ranking=sorted(supermercados_facturacion.items(),key=lambda tupla:tupla[1],reverse=True)[:n]
    return list(enumerate(ranking,1))

def clientes_itinerantes(lista,n):
    ''' recibe una lista de tuplas de tipo Compra y un entero n, 
y devuelve una lista de tuplas con el dni del cliente y la lista 
de provincias donde el cliente ha realizado sus compras, ordenadas
alfabéticamente. Solo se devolverán aquellos clientes que hayan 
comprado en un número de provincias mayor que el parámetro n. (2 puntos)
'''
    clientes={}
    clientes_provincias=provincias_por_cliente(lista)
    for dni,conjunto_provincias in clientes_provincias.items():
        if len(conjunto_provincias)>n:
            clientes[dni]=sorted(conjunto_provincias)
    return list(clientes.items())

def provincias_por_cliente(lista):
    clientes_provincias={}
    for compra in lista:
        if compra.dni not in clientes_provincias:
            provincias=set()
            provincias.add(compra.provincia)
            clientes_provincias[compra.dni]=provincias
        else:
            clientes_provincias[compra.dni].add(compra.provincia)
    return clientes_provincias
    

        

