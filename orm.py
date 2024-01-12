import tkinter as tk
import random
import math
import json
import sqlite3

#Declaración de variables globales
personas = []

class Persona:
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio = valor(30,60)
        self.direccion = random.randint(0,360)
        self.color = colores()
        self.velocidad = valor(1,5)
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill="green")
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-16,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill="blue")
    def mueve(self):
        self.colisiona()
        desplazamientox = self.velocidad * math.cos(self.direccion)
        desplazamientoy = self.velocidad * math.sin(self.direccion)
        lienzo.move(
            self.entidad,
            desplazamientox,
            desplazamientoy)
        lienzo.move(
            self.entidadenergia,
            desplazamientox,
            desplazamientoy)
        lienzo.move(
            self.entidaddescanso,
            desplazamientox,
            desplazamientoy)
        self.posx += desplazamientox
        self.posy += desplazamientoy
        #self.direccion += random.uniform(-1, 1)
    def colisiona(self):
        if self.posx < 0 or self.posx >1024 or self.posy < 0 or self.posy >1024:
            self.direccion += math.atan2(self.posy,self.posx)

            
def colores():
    listacolores = ["red","blue","yellow","green","orange","purple","pink","black"]
    colorazar = listacolores[random.randint(0,len(listacolores)-1)]
    return colorazar

def valor(numero1,numero2):
    numero = random.randint(numero1,numero2)
    return numero

def guardarPersonas():
    print("guardo a los jugadores")
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE FROM jugadores
            ''')
    conexion.commit()
    for persona in personas:
        cursor.execute('''
            INSERT INTO jugadores
            VALUES (
                NULL,
                '''+str(persona.posx)+''',
                '''+str(persona.posy)+''',
                '''+str(persona.radio)+''',
                '''+str(persona.direccion)+''',
                "'''+str(persona.color)+'''",
                '''+str(persona.velocidad)+''',
                "'''+str(persona.entidad)+'''"
            )
            ''')
    conexion.commit()
    conexion.close()

#Creo una ventana
raiz = tk.Tk()

#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz,width=1024,height=1024)
lienzo.pack()

#Botón de guardar
boton = tk.Button(raiz,text="Guarda",command=guardarPersonas)
boton.pack()

#Cargar personas desde SQL
try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''
            SELECT *
            FROM jugadores
            ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        print(fila)
        persona = Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.velocidad = fila[6]
        persona.entidad = fila[7]
        personas.append(persona)
    conexion.close()
except:
    print("error al leer base de datos")

#En la colección introduzco instancias de personas en el caso de que no existan
print(len(personas))
if len(personas) == 0:
    numeropersonas = 10
    for i in range(0,numeropersonas):
        personas.append(Persona())
    
#Dibujar cada persona de la colección
for persona in personas:
    persona.dibuja()
    
#Creo un buble repetitivo
def bucle():
    #Muevo a cada persona de la colección
    for persona in personas:
        persona.mueve()
    raiz.after(10,bucle)
    
#Ejecuto el bucle
bucle()

raiz.mainloop()

