"""
Universidad Nacional del Nordeste

Método de tabulacion - Quine-McCluskey

"""

import pandas as pd
import numpy as np
from tkinter import *
# "(A+B+C+D)*(A+B+C+D')*(A+B+C'+D)*(A+B+C'+D')*(A+B'+C+D)*(A'+B+C+D)*(A'+B+C+D')"
# A*B*D+A'*C'*D'+A'*B+A'*C*D'+A*B'*D' ejercicio 9.a guia 2
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

# Funcion principal que calcula el metodo de tabulacion, tiene como input el la funcion
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
    
    for i in range(cantidad):
        save.append(0)
        save_val.append(0)
    
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
            
        Tabla.append(row)
    
    df_Tabla = pd.DataFrame(Tabla, columns=(variables))
    
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
    for termino in s:
        base = []
        for i in termino:
            if i in variables:
                base.append(variables.index(i)+1)
            elif i == "'":
                base[-1] = base[-1]*-1
                  
        fund.append(base)
    for i in fund:
        g = []
        
        for w in range(cantidad):
            if w+1 in i:
                g.append(1)
            elif -w-1 in i:
                g.append(0)
            else:
                g.append("-")
                
        bases.append(g)
    
    miniTerminos = []
    miniTerminos_index = []
    
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
    for i in miniTerminos:
        tabulacion[i.count(1)].append(i)
        tabulacion_index[i.count(1)].append(miniTerminos_index[miniTerminos.index(i)]) #No necesario
        
    #print(tabulacion)
    #print(tabulacion_index)
    
    df_tabulacion = pd.DataFrame(tabulacion)
    print(df_tabulacion)
    
    tabulacion_ordenado = tabulacion[:]
    iterar = 1
    while iterar < 2:
        tabulacion_old = tabulacion_ordenado[:]
        tabulacion_iterado=[]
        tabulacion_ordenado=[]
        for grupo in tabulacion_old: #iteramos por cada agrupacion por cantidad de unos
            
            for termino in grupo: #iteramos por cada termino en el grupo        
                
                if tabulacion_old.index(grupo)+1 <= len(tabulacion_old)-1: # esta linea evita el error de index out of range, no importa
                    
                    for i in tabulacion_old[tabulacion_old.index(grupo)+1]:#y por ultimo iteramos por cada valor en el grupo siguiente
                        suma = []
                        for elemento in termino:#comparo los dos terminos
                            
                            if elemento == i[termino.index(elemento)] and elemento != "-":
                                suma.append(elemento)
                            elif elemento == "-" or i[termino.index(elemento)] == "-":
                                suma.append("-")
                            else:
                                suma.append("-")
                        
                        if suma.count("-") == iterar:
                            tabulacion_iterado.append(suma)                                
                                
        
        for i in range(cantidad-iterar+1): #se crean la matriz vacias de las dimensiones requeridas
            tabulacion_ordenado.append([])
        for i in tabulacion_iterado:
            tabulacion_ordenado[i.count(1)].append(i)
        #print(pd.DataFrame(tabulacion_iterado))
        #print(pd.DataFrame(tabulacion_ordenado))
        iterar = iterar + 1
        print(iterar)
        #print(tabulacion_ordenado)
        print(pd.DataFrame(tabulacion_ordenado))
    return df_tabulacion,df_Tabla
    #print(Tabla.index([0,1,0,0]))
       
    #print(np.add(tabulacion[2][1],tabulacion[3][1]))
    #print(np.add(Tabla[8],Tabla[12]))


metodoDeTabulacion(Entrada)

# UI

#""" Se activa comentando esta linea

def boton():
    tab,tablita = metodoDeTabulacion(Entrada.get())
    
    #Agregar display de tablas     
    lb = Label(window, text= tab.to_string()+tablita.to_string(), font=("Arial Bold",12))
    lb.grid(column= 0, row= 50)
    
    
window = Tk()
window.title("Método de Tabulacion - Circuitos Lógicos")
window.geometry('600x600')

lb = Label(window, text= "Funcion de entrada", font=("Arial Bold",12))
lb.grid(column= 0, row= 0)

Entrada = Entry(window, width= 50)
Entrada.grid(column= 0, row= 15)

btn = Button(window, text= "Calcular", command=boton)
btn.grid(column= 0, row = 35)
    
window.mainloop()

#y esta linea""" 