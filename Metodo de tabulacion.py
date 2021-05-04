# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:24:10 2021

@author: Fran
"""

import math
import pandas as pd
import numpy as np

Funcion = "A'+B*C+C*D"

def tipoDeFuncion(f):
    
    parentesis = 0
    tipo = "nada"
    for c in f:
        if c == "(":
            parentesis = 1
        elif c == ")":
            parentesis = 0
        elif c == "+" and parentesis == 0:
            return "sumas"
        elif c == "*" and parentesis == 0:
            return "productos"
        

b=[]
c=[]
    
for i in Funcion:
    if i != "'" and i != "+" and i != "*" and i != "(" and i != ")":
            
        b.append(i)
            
        if i not in c:
            c.append(i)
            
c.sort()

cantidad = len(c) 


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

df = pd.DataFrame(Tabla, columns=(c))

print(df)

# Separamos la funcion en términos

if tipoDeFuncion(Funcion) == "sumas":
    s = Funcion.split("+")
else:
    s = Funcion.split("*")
    
print(np.add(Tabla[8],Tabla[12]))



