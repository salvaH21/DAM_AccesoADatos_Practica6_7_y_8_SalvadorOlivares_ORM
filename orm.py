import tkinter as tk
import random
import math
import json
import sqlite3

#Declaración de variables globales
personas = []
seleccioncolor = 'SELECT * FROM jugadores WHERE color="pink"'
seleccionciudad = 'SELECT * FROM jugadores WHERE ciudad="jaen"'
seleccionpelo = 'SELECT * FROM jugadores WHERE colorpelo="pelirrojo"'
seleccionprofesion = 'SELECT * FROM jugadores WHERE profesion="docencia"'

class Recogible():
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.color = colores()
    def serializar(self):
        recogible_serializado = {
            "posx":self.posx,
            "posy":self.posy,
            "color":self.color,
            }
        return recogible_serializado

class Persona():
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio = 30
        self.direccion = random.randint(0,360)
        self.color = colores()
        self.velocidad = valor(1,5)
        self.edad = valor(1,100)
        self.ciudad = ciudad()
        self.colorpelo = colorpelo()
        self.profesion = profesion()
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.inventario = []
        for i in range(0,10):
            self.inventario.append(Recogible())
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
        if self.energia > 0:
            self.energia -= 0.1
        if self.descanso > 0:
            self.descanso -= 0.1
        self.colisiona()
        desplazamientox = self.velocidad * math.cos(self.direccion)
        desplazamientoy = self.velocidad * math.sin(self.direccion)
        lienzo.move(
            self.entidad,
            desplazamientox,
            desplazamientoy)
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(
            self.entidadenergia,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 10,
            self.posx - self.radio/2 + anchuraenergia,
            self.posy - self.radio/2 - 8)
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(
            self.entidaddescanso,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 16,
            self.posx - self.radio/2 + anchuradescanso,
            self.posy - self.radio/2 - 14)
        self.posx += desplazamientox
        self.posy += desplazamientoy
        #self.direccion += random.uniform(-1, 1)
    def colisiona(self):
        if self.posx < 0 or self.posx >1024 or self.posy < 0 or self.posy >1024:
            self.direccion += math.atan2(self.posy,self.posx)
    def serializar(self):
        persona_serializada = {
            "posx":self.posx,
            "posy":self.posy,
            "radio":self.radio,
            "direccion":self.direccion,
            "color":self.color,
            "velocidad":self.velocidad,
            "edad":self.edad,
            "ciudad":self.ciudad,
            "colorpelo":self.colorpelo,
            "profesion":self.profesion,
            "energia":self.energia,
            "descanso":self.descanso,
            "inventario":[item.serializar() for item in self.inventario]
            }
        return persona_serializada

            
def colores():
    listacolores = ["red","blue","yellow","green","orange","purple","pink","black"]
    colorazar = listacolores[random.randint(0,len(listacolores)-1)]
    return colorazar

def colorpelo():
    listacolores = ["moreno","rubio","pelirrojo","canoso","sin pelo"]
    colorazar = listacolores[random.randint(0,len(listacolores)-1)]
    return colorazar

def profesion():
    listaprofesiones = ["docencia","hosteleria","informatica","arquitectura","derecho","policia","medicina","enfermeria"]
    profesionazar = listaprofesiones[random.randint(0,len(listaprofesiones)-1)]
    return profesionazar

def ciudad():
    listaciudades = ["jaen","valencia","madrid","barcelona","bilbao","granada","almeria","santander"]
    ciudadazar = listaciudades[random.randint(0,len(listaciudades)-1)]
    return ciudadazar

def valor(numero1,numero2):
    numero = random.randint(numero1,numero2)
    return numero

def guardarPersonas():
    print("guardo a los jugadores")
    #Tambien guardo en json de momento
    personas_serializadas = [persona.serializar() for persona in personas]
##    cadena = json.dumps(personas_serializadas)
##    archivo = open("jugadores.json",'w')
##    archivo.write(cadena)
    with open("jugadores.json","w") as archivo:
        json.dump(personas_serializadas,archivo,indent=4)
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE FROM jugadores
            ''')
    cursor.execute('''
            DELETE FROM recogibles
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
                '''+str(persona.edad)+''',
                "'''+str(persona.ciudad)+'''",
                "'''+str(persona.colorpelo)+'''",
                "'''+str(persona.profesion)+'''",
                "'''+str(persona.entidad)+'''",
                '''+str(persona.energia)+''',
                '''+str(persona.descanso)+''',
                "'''+str(persona.entidadenergia)+'''",
                "'''+str(persona.entidaddescanso)+'''",
                "'''+str(persona.inventario)+'''"
            )
            ''')
        for recogible in persona.inventario:
            peticion = '''
            INSERT INTO recogibles
            VALUES (
                NULL,
                '''+str(persona.entidad)+''',
                "'''+str(recogible.posx)+'''",
                "'''+str(recogible.posy)+'''",
                "'''+str(recogible.color)+'''"
            )
            '''
            cursor.execute(peticion)
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
##try:
##    conexion = sqlite3.connect("jugadores.sqlite3")
##    cursor = conexion.cursor()
##
##    cursor.execute(seleccioncolor)
##    while True:
##        fila = cursor.fetchone()
##        if fila is None:
##            break
##        #print(fila)
##        persona = Persona()
##        persona.posx = fila[1]
##        persona.posy = fila[2]
##        persona.radio = fila[3]
##        persona.direccion = fila[4]
##        persona.color = fila[5]
##        persona.velocidad = fila[6]
##        persona.edad = fila[7]
##        persona.ciudad = fila[8]
##        persona.colorpelo = fila[9]
##        persona.profesion = fila[10]
##        persona.entidad = fila[11]
##        persona.energia = fila[12]
##        persona.descanso = fila[13]
##        persona.entidadenergia = fila[14]
##        persona.entidaddescanso = fila[15]
##        personas.append(persona)
##        
##        cursor2 = conexion.cursor()
##        cursor2.execute('''
##            SELECT *
##            FROM recogibles
##            WHERE persona='''+persona.entidad+'''
##            ''')
##        while True:
##            fila2 = cursor2.fetchone()
##            if fila2 is None:
##                break
##            nuevorecogible = Recogible()
##            nuevorecogible.posx = fila2[2]
##            nuevorecogible.posy = fila2[3]
##            nuevorecogible.color = fila2[4]
##            persona.inventario.append(nuevorecogible)
##    conexion.close()
##except Exception as e:
##    print("error al leer base de datos", str(e))

#En la colección introduzco instancias de personas en el caso de que no existan
print("Personas encontradas: " + str(len(personas)))
if not personas:
    numeropersonas = 1
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

