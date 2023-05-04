#modo
   ##sensores: y
   ##control rc: z
#laser: soltar l
   ##x izquierda j
   ##x derecha k
   ##y arriba    h
   ##y abajo     i
#disparos: acorde al numumero

#direccion: soltar: g
##avanzar c
# retroceder f
# derecha e
# izquierda d
# stop g

import utime
from machine import Pin,UART,ADC

#Parte de comunicacion
uart = UART(1,9600)
#CONFIGURACION DEL PUENTE H
M1A = Pin(28, Pin.OUT)
M1B = Pin(27, Pin.OUT)
M2A = Pin(15, Pin.OUT)
M2B = Pin(14, Pin.OUT)

#Modo
modo='c'#Control RC
#modo='a'#Autonomo
#Movimientos para la raspberry
def move(m1a, m1b, m2a, m2b):
    M1A.value(m1a)
    M1B.value(m1b)
    M2A.value(m2a)
    M2B.value(m2b)

#Creación servo
s1 = Servo(2) 

# Función Map para conversión de valores 
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Función que controla el angulo
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value


while True:
    #lectura del hc 
   if uart.any():
     command = uart.readline()
     print("Esto llega del celular", command)
     print("Modo actual ",modo)
     #Adecuamos el modo de acuerdo a la entrada desde la interfaz    
     if command == b'z':
         modo = 'c' #Cambiando a modo rc
     elif command == b'y':
         modo = 's'#Cambiando a modo sensores
     
     if modo == 'c':
        # Mover hacia adelante
          if command == b'c':
              print("moviendome hacia adelante")
              move(1, 0, 1, 0)
              utime.sleep(1)

        # Mover hacia atrás
          elif command == b'f':
              print("moviendome hacia atras")
              move(0, 1, 0, 1)
              utime.sleep(1)
            
        # Mover hacia derecha
          elif command == b'e':
              print("moviendome hacia la derecha")
              move(1, 0, 0, 1)
              utime.sleep(1)
            
        # Mover hacia izquierda
          elif command == b'd':
              print("moviendome hacia la izquierda")
              move(0, 1, 1, 0)
              utime.sleep(1)
        # Detenerse
          elif command == b'g':
              print("deteniendome")
              move(0, 0, 0, 0)
              utime.sleep(1)
    
     elif modo == 's':
        
         #Seguidor de linea
           print("Modo actual ",modo)
    
    #pwm
   pot = ADC(26)
   valor = pot.read_u16()
   #print("potenciometro: ", valor)
    
    
    # Leer los datos del módulo Bluetooth

    # Interpretar los datos recibidos
    

    # Pequeña pausa
   utime.sleep(0.1)
  
    
