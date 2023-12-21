import tkinter as tk
import random
import math
import json

personas = []

class Persona:
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio = valor(30,60)
        self.direccion = random.randint(0,360)
        self.color = colores()
        self.velocidad = valor(1,10)
        self.entidad = ""
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
    def mueve(self):
        self.colisiona()
        desplazamientox = self.velocidad * math.cos(self.direccion)
        desplazamientoy = self.velocidad * math.sin(self.direccion)
        lienzo.move(
            self.entidad,
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
    cadena = json.dumps([vars(persona) for persona in personas])
    print(cadena)
    archivo = open("jugadores.json",'w')
    archivo.write(cadena)
   

#Creo una ventana
raiz = tk.Tk()

#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz,width=1024,height=1024)
lienzo.pack()

#Botón de guardar
boton = tk.Button(raiz,text="Guarda",command=guardarPersonas)
boton.pack()

#Cargar personas desde el disco duro
try:
    carga = open("jugadores.json",'r')
    cargado = carga.read()
    cargadolista = json.loads(cargado)
    for elemento in cargadolista:
        persona = Persona()
        persona.__dict__.update(elemento)
        personas.append(persona)
except:
    print(math.pi)

#En la colección introduzco instancias de personas en el caso de que no existan
print(len(personas))
if len(personas) == 0:
    numeropersonas = 8
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

