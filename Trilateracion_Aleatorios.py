from tkinter import *
from tkinter import messagebox
import numpy as np
from time import time
import math

#Metodo que busca el menor elemento de un vector y devuelve su indice
#Utiliza el metodo burbuja, ya que son vectores pequeños
def buscar_menor(vector):
    menor=vector[0]
    indice=0;
    for i in range(len(vector)):
        if vector[i]<menor:
            menor=vector[i]
            indice=i
    return indice

#Metodo que busca el mayor elemento de un vector y devuelve su indice
#Utiliza el metodo burbuja, ya que son vectores pequeños
def buscar_mayor(vector):
    mayor=vector[0]
    indice=0;
    for i in range(len(vector)):
        if vector[i]>mayor:
            mayor=vector[i]
            indice=i
    return indice

#Metodo que imprime en consola la Z,X,Y de cada iteración
def imprime(x,y,z):
    for i in range(len(x)):
        print("X= "+str(x[i])+"   Y= "+str(y[i])+"   Z= "+str(z[i]))

#Método que hace 1000 iteraciones (población) y genera X,Y aleatorias, entre un rango de X2-X2
#Y2-Y1 y hace las evaluaciones de la funcion C(X,Y)
#Para esta función las restricciones se tomaron como >=0 
def iterar_aleatorio(x,y,r,X1,X2,Y1,Y2):
    tabla= np.zeros((1000,7))
    for i in range (1000):
        tabla[i][0]= np.random.uniform(low=X2,high=X1)
        tabla[i][1]= np.random.uniform(low=Y2,high=Y1)
        ev=np.zeros(4)
        #Hace las evaluaciones de C(X,Y)
        ev[0]=math.pow((math.pow((tabla[i][0]-x[0]),2)+math.pow((tabla[i][1]-y[0]),2)-math.pow(r[0],2)),2)
        ev[1]=math.pow((math.pow((tabla[i][0]-x[1]),2)+math.pow((tabla[i][1]-y[1]),2)-math.pow(r[1],2)),2)
        ev[2]=math.pow((math.pow((tabla[i][0]-x[2]),2)+math.pow((tabla[i][1]-y[2]),2)-math.pow(r[2],2)),2)
        ev[3]=math.pow((math.pow((tabla[i][0]-x[3]),2)+math.pow((tabla[i][1]-y[3]),2)-math.pow(r[3],2)),2)
        #Hace la sumatoria
        z= np.sum(ev)
        tabla[i][6]=z
    #Busca la Z mínima en el conjunto de 1000
    #Retorna la X,Y,Z de la Z mínima
    minimo=tabla[0][6]
    indice=0
    for i in range(1000):
        if tabla[i][6]<minimo:
            minimo=tabla[i][6]
            indice=i
    return [tabla[indice][0],tabla[indice][1],tabla[indice][6]]

#Método que limpia la interfaz, limpia las entradas de datos y las salidas
def limpiar():
    x1.delete(0,"end")
    x2.delete(0,"end")
    x3.delete(0,"end")
    x4.delete(0,"end")
    y1.delete(0,"end")
    y2.delete(0,"end")
    y3.delete(0,"end")
    y4.delete(0,"end")
    r1.delete(0,"end")
    r2.delete(0,"end")
    r3.delete(0,"end")
    r4.delete(0,"end")
    tiempo.delete(0,"end")
    rx.delete(0,"end")
    ry.delete(0,"end")
    
#Método que muestra los resultados en la interfaz    
def muestra(x,y,s):
    tiempo.insert(0,str(s))
    rx.insert(0,str(x))
    ry.insert(0,str(y))
    
#Método que se ejecuta al dar clic en calcular
#Primero valida que todas las entradas esten rellenadas, si no muestra un error
def clicked():
    resp=[]
    vx=[]
    vy=[]
    vr=[]
    resp.append(x1.get())
    resp.append(x2.get())
    resp.append(x3.get())
    resp.append(x4.get())
    resp.append(y1.get())
    resp.append(y2.get())
    resp.append(y3.get())
    resp.append(y4.get())
    resp.append(r1.get())
    resp.append(r2.get())
    resp.append(r3.get())
    resp.append(r4.get())
    if "" in resp:
        messagebox.showwarning('ERROR', 'Porfavor rellena todos los parámetros')
    else:
        for i in range(12):
            if i<4:
                vx.append(float(resp[i]))
            if i>=4 and i<8:
                vy.append(float(resp[i]))
            if i>=8 and i<12:
                vr.append(float(resp[i]))
        #Crea 3 vectores de 100 donde se guardaran las X,Y,Z mas optimizadas
        X= np.zeros(100)
        Y= np.zeros(100)
        Z= np.zeros(100)
        vectorX= np.asarray(vx)
        vectorY= np.asarray(vy)
        vectorR= np.asarray(vr)
        tiempo_inicial = time()
        #Busca las X,Y mayores y menores y les suma a las mayores su radio
        #A las menores se los resta, para crear el rango para generar los 
        #números aleatorios
        x_men=buscar_menor(vectorX)
        x_may=buscar_mayor(vectorX)
        xmenor=vectorX[x_men]-abs(vectorR[x_men])
        xmayor=vectorX[x_may]+abs(vectorR[x_may])
        y_men=buscar_menor(vectorY)
        y_may=buscar_mayor(vectorY)
        ymenor=vectorX[y_men]-abs(vectorR[y_men])
        ymayor=vectorX[y_may]+abs(vectorR[y_may])
        cont=100
        #Hace un ciclo de 100 iteraciones, y en cada iteración, genera una poblacion
        #Mediante el método iterar, se genera una poblacion de 1000 y se obtiene
        #la Z minima de la poblacion y sus coordenadas, esto se hace 100 veces
        #Si en las iteraciones el temporizador alcanza los 60 seg. se rompe el
        #ciclo, y el contador de iteraciones ya no seria 100, sino el numero en que
        #se paro el proceso
        #Se Promedian las X y Y de los arreglos de 100 y se obtiene el resultado.
        for i in range(100):
            X[i],Y[i],Z[i] = iterar_aleatorio(vectorX,vectorY,vectorR,xmayor,xmenor,ymayor,ymenor)
            tiempo=time()
            if (tiempo-tiempo_inicial)>=60:
                cont=i+1
                break;
        x_final= np.sum(X)/cont
        y_final= np.sum(Y)/cont
        tiempo_final = time() 
        tiempo_ejecucion = tiempo_final - tiempo_inicial
        muestra(x_final,y_final,tiempo_ejecucion)
        print(str(cont))
        imprime(X,Y,Z)

#ESTOS SON LOS ELEMENTOS DE LA INTERFAZ
window = Tk()
window.title("Trilateración")
window.geometry('350x200')

#Textos de las referencias
marcoizq=Label(window,text="RE.1")
marcoizq.place(x=20,y=30)
marcoizq2=Label(window,text="RE.2")
marcoizq2.place(x=20,y=50)
marcoizq3=Label(window,text="RE.3")
marcoizq3.place(x=20,y=70)
marcoizq4=Label(window,text="RE.4")
marcoizq4.place(x=20,y=90)

# Textos y salidas de resultados
result= Label(window,text="Resultado:")
result.place(x=20,y=130)
resx=Label(window,text="X",fg="red")
resx.place(x=122,y=115)
resy=Label(window,text="Y",fg="blue")
resy.place(x=182,y=115)
rest=Label(window,text="Tiempo",fg="green")
rest.place(x=222,y=115)
rx = Entry(window,width=7,bg="#FA8072")
rx.place(x=100, y=130)
ry = Entry(window,width=7,bg="#00FFFF")
ry.place(x=160, y=130)
tiempo= Entry(window,width=7,bg="#01f138")
tiempo.place(x=220,y=130)

#Textos para orientar al usuario
txt1 = Label(window, text="X",fg="red")
txt1.place(x=90, y=10)
txt2 = Label(window, text="Y",fg="blue")
txt2.place(x=175, y=10)
txt3 = Label(window, text="R",fg="green")
txt3.place(x=260, y=10)

#Entradas X
x1 = Entry(window,width=10)
x1.place(x=60, y=30)
x2 = Entry(window,width=10)
x2.place(x=60, y=50)
x3 = Entry(window,width=10)
x3.place(x=60, y=70)
x4 = Entry(window,width=10)
x4.place(x=60, y=90)

# Entradas Y
y1 = Entry(window,width=10)
y1.place(x=145, y=30)
y2 = Entry(window,width=10)
y2.place(x=145, y=50)
y3 = Entry(window,width=10)
y3.place(x=145, y=70)
y4 = Entry(window,width=10)
y4.place(x=145, y=90)

#Entradas de distancia
r1 = Entry(window,width=10)
r1.place(x=230, y=30)
r2 = Entry(window,width=10)
r2.place(x=230, y=50)
r3 = Entry(window,width=10)
r3.place(x=230, y=70)
r4 = Entry(window,width=10)
r4.place(x=230, y=90)

#Botones Calcular y limpiar
btn = Button(window, text="Calcular", command=clicked, bg="#00FF00")
btn.place(x=90, y=160)
limpia = Button(window, text="Limpiar", command=limpiar, bg="#CD5C5C")
limpia.place(x=190, y=160)
window.mainloop()