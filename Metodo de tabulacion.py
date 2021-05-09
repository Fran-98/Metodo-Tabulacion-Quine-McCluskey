"""
Universidad Nacional del Nordeste

Método de tabulacion - Quine-McCluskey

"""

import pandas as pd
import numpy as np
from tkinter import *
# "(A+B+C+D)*(A+B+C+D')*(A+B+C'+D)*(A+B+C'+D')*(A+B'+C+D)*(A'+B+C+D)*(A'+B+C+D')"
# A*B*D+A'*C'*D'+A'*B+A'*C*D'+A*B'*D' ejercicio 9.a guia 2
# 
Entrada = "A*B*D+A'*C'*D'+A'*B+A'*C*D'+A*B'*D'"

# Funcion que detecta el tipo de funcion segun el primer signo que encuentre
# Aca todavia falta analizar el caso en el que se tenga una sola variable en el primer termino
def tipoDeFuncion(f):
    
    parentesis = 0
    for c in f:
        if c == "(":
            parentesis = 1
        elif c == ")":
            parentesis = 0
        elif c == "+" and parentesis == 0:
            return "productos"
        elif c == "*" and parentesis == 0:
            return "sumas"

# Funcion principal que calcula el metodo de tabulacion, tiene como input la funcion
def metodoDeTabulacion(Funcion):
           
    b=[]
    variables=[]
        
    #Iteramos por cada elemento en el string Funcion y separamos las variables, colocamos las variables sin repetir en "variables"
    for i in Funcion:
        if i != "'" and i != "+" and i != "*" and i != "(" and i != ")":
                
            b.append(i)
                
            if i not in variables:
                variables.append(i)
                
    variables.sort()
    
    cantidad = len(variables) 
    
    # Obtener miniterminos y tabla
        
    Tabla = []
    save = []
    save_val = []
    
    #Reservamos los lugares en la matrices para guardar las variables guardadas
    for i in range(cantidad):
        save.append(0)
        save_val.append(0)
    #iteramos en cada fila cada columna y mediante la relacion de potencias de 2
    #obtenemos la tabla canonica de la cantidad de variables
    for fila in range(pow(2,cantidad)):
        row = []
        for col in range(cantidad):
            
            if save[col] < pow(2,cantidad - col - 1):
                save[col] = save[col] + 1
                
            else:
                save[col] = 1
                if save_val[col] == 0:
                    save_val[col] = 1
                else:
                    save_val[col] = 0
            
            row.append(save_val[col])
        #la tabla va guardando cada columna 
        Tabla.append(row)
    
    df_Tabla = pd.DataFrame(Tabla, columns=(variables)) #realizamos un dataframe para tener mejor control sobre la misma
    
    #print(df_Tabla)
    
    # Separamos la funcion en términos
    tipo = tipoDeFuncion(Funcion)
    
    if tipo == "sumas":
        s = Funcion.split("+")
    else:
        s = Funcion.split("*")
        
    #En cada termino detectar que minitermino tenemos
    
    fund = [] #fundamentales?
    bases = [] #bases?
    #por cada termino se busca las "fundamentales", siendo estas las que se presentan
    #en cada minitermino que este termino representa
    for termino in s:
        base = []
        for i in termino:
            if i in variables:
                base.append(variables.index(i)+1)
            elif i == "'":
                base[-1] = base[-1]*-1
                  
        fund.append(base) #las fundamentales se guardan aqui (el nombre base quedó sin sentido despues de programarlo)
    #por cada elemento en las fundamentales se observa.
    
    #las fundamentales contienen el numero de cada variables de la base y 
    #si la variable se encuentra primada este numero es negativo.
    
    #print(fund)
    
    #Luego se pasan estos numeros a 0 y 1
    for i in fund:
        g = []
        
        for w in range(cantidad):
            if w+1 in i:
                g.append(1)
            elif -w-1 in i:
                g.append(0)
            else:
                g.append("-")
    #y se los coloca ahora si a la matriz bases
        bases.append(g)
    
    miniTerminos = []
    miniTerminos_index = []
    
    #Comparando las bases con los miniterminos se pueden encontrar cuales describen a la funcion canonica
    for n in bases:
        
        for t in Tabla:
            incidencia = 0
            for i in range(len(n)):
                if n[i] == t[i]:
                    incidencia = incidencia + 1
            
            if incidencia == n.count(0)+n.count(1):
                
                if t not in miniTerminos:
                    miniTerminos.append(t)
                    miniTerminos_index.append(Tabla.index(t))
                    
    miniTerminos.sort()
    miniTerminos_index.sort()
    
    df_miniTerminos = pd.DataFrame(miniTerminos, columns = (variables), index = (miniTerminos_index))
    #print(miniTerminos)
    #print(miniTerminos_index)
    
    #print(df_miniTerminos)
    
    tabulacion = []
    tabulacion_index = []
    for i in range(cantidad+1): #se crean las matrices vacias de las dimensiones requeridas
        tabulacion.append([])
        tabulacion_index.append([])
    #Se ordena por cantidad de 1
    for i in miniTerminos:
        tabulacion[i.count(1)].append(i)
        tabulacion_index[i.count(1)].append(miniTerminos_index[miniTerminos.index(i)]) #No necesario
        
    #print(tabulacion)
    #print(tabulacion_index)
    
    df_tabulacion = pd.DataFrame(tabulacion)
    print(df_tabulacion)
    
    tabulacion_ordenado = tabulacion[:]
    iterar = 1
    while iterar < 3:
        tabulacion_old = tabulacion_ordenado[:]
        tabulacion_iterado=[]
        tabulacion_ordenado=[]
        for grupo in tabulacion_old: #iteramos por cada agrupacion por cantidad de unos
            
            for termino in grupo: #iteramos por cada termino en el grupo        
                usado = 0
                if tabulacion_old.index(grupo)+1 <= len(tabulacion_old)-1: # esta linea evita el error de index out of range, no importa
                    
                    for i in tabulacion_old[tabulacion_old.index(grupo)+1]:#y por ultimo iteramos por cada valor en el grupo siguiente
                        suma = [] # formando el valor final para añadir a la matriz
                        index = 0 #indice para el elemento a comparar
                        for elemento in termino:#comparo los dos terminos
                            dash_coinc = 1
                            if elemento == i[index] and elemento != "-":
                                suma.append(elemento)
                            elif elemento != i[index] and i[index] == "-":
                                dash_coinc = 0
                            elif elemento == "-" and i[index] != "-":
                                dash_coinc = 0
                            else:
                                suma.append("-")
                            index = index+1
                        if suma.count("-") == iterar and suma not in tabulacion_iterado and dash_coinc == 1 and len(suma)==len(variables):
                            tabulacion_iterado.append(suma)
                                         
        for i in range(cantidad-iterar+1): #se crea la matriz vacias de las dimensiones requeridas
            tabulacion_ordenado.append([])
        for i in tabulacion_iterado:
            tabulacion_ordenado[i.count(1)].append(i)
        #print(pd.DataFrame(tabulacion_iterado))
        #print(pd.DataFrame(tabulacion_ordenado))
        iterar = iterar + 1
        #print(tabulacion_ordenado)
        print(pd.DataFrame(tabulacion_ordenado))
        
        #Fin while
    
    funcion_simp = ""
    cant_de_terminos = 0
    cant_de_terminos_puestos = 0
    
    #calculo la cantidad de terminos que tendremos
    for grupo in tabulacion_ordenado:
        cant_de_terminos = cant_de_terminos + len(grupo)
        
    #armar la funcion simplificada
    #Se itera sobre cada termino obtenido para armar la funcion simplificada
    for grupo in tabulacion_ordenado:
        
        for termino in grupo:
            index = 0
            for i in termino:
                if i == 1:
                    funcion_simp = funcion_simp + variables[index]
                elif i == 0:
                    funcion_simp = funcion_simp + variables[index] + "'"
                if i != "-" and index+1 < len(termino):
                    if tipo == "sumas":
                        funcion_simp = funcion_simp + "*"
                    else:
                        funcion_simp = funcion_simp + "+"
                        
                if i == "-" and index == len(termino)-1:
                    funcion_simp = funcion_simp[:-1]
                    
                index = index + 1
                
            cant_de_terminos_puestos = cant_de_terminos_puestos + 1
            
            if funcion_simp[-1] != "*" and funcion_simp[-1] != "+" and cant_de_terminos_puestos<cant_de_terminos:
                
                if tipo == "sumas":
                    funcion_simp = funcion_simp + "+"
                else:
                    funcion_simp = funcion_simp + "*"
            
    print(funcion_simp)
    return df_tabulacion,df_Tabla
    
#Fin metodoDeTabulacion

metodoDeTabulacion(Entrada)
