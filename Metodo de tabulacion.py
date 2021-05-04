# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:24:10 2021

@author: Fran
"""

import pandas as pd
import numpy as np

Funcion = "A'+B*C+C*D"

# Funcion que detecta el tipo de funcion
def tipoDeFuncion(f):
    
    parentesis = 0
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
variables=[]
    
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

df = pd.DataFrame(Tabla, columns=(variables))

print(df)

# Separamos la funcion en términos
tipo = tipoDeFuncion(Funcion)

if tipo == "sumas":
    s = Funcion.split("+")
else:
    s = Funcion.split("*")

    
#En cada termino detectar que mini tenemos (funcion)?

fund = []
bases = []
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
print(bases)
 
for i in bases:
    for w in Tabla:
        
#print(Tabla.index([0,1,0,0]))
   
#print(np.add(Tabla[8],Tabla[12]))



