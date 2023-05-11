"""
modo
   sensores: y
   control rc: z
laser: soltar l
   x izquierda j
   x derecha k
   y arriba    h
   y abajo     i
disparos: acorde al numumero

direccion: soltar: g
avanzar c
retroceder f
derecha e
izquierda d
stop g
"""


import utime
from machine import Pin, UART, PWM
from servo import Servo

#Comunicacion Serial  UART_PORT_1  GP4_TX  GP5_TX
uart = UART(1,9600)

#Entradas digitales sensores
sensor1 = Pin(0, Pin.IN, Pin.PULL_DOWN) #izquierda
sensor2 = Pin(2, Pin.IN, Pin.PULL_DOWN) #derecha

#Servomotores
s1 = Servo(16)
s2 = Servo(17)
s3 = Servo(15)

#Salidas pines puente H
M1A = Pin(18)   #motorDerechaGiroAdelnate
M1B = Pin(19)   #motorDerechaGiroAtras
M2A = Pin(20)   #motorIzquierdaGiroAdelante
M2B = Pin(21)   #motorIzquierdaGiroAtras

pwmDerechadelante       = PWM(M1A)  #PWM_motorDerechaGiroAdelnate
pwmDerechatras          = PWM(M1B)  #PWM_motorDerechaGiroAtras
pwmIzquierdaAdelante    = PWM(M2A)  #PWM_motorIzquierdaGiroAdelante
pwmIzquierdAtras        = PWM(M2B)  #PWM_motorIzquierdaGiroAtras

inMin = 0           #minimoVelocidad 0 %
inMax = 100         #maximoVelocidad 100 %
outMin = 0          #minimoVelocidad 0 PWM
outMax = 65535      #maximoVelocidad 65535 PWM

#modo de contro
modo=True #Control RC

#control servo
dirServo = 'l'
posSerX = 90
posSerY = 90
posSerZ = 90
angulos = 1

#Funcion map para conversion Porcentaje a PWM
def Map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

#Conversion angulo a pwm 20ms
def servo_Angle(angle, idServo):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
        
    if idServo == 'x':
        s1.goto(round(Map(angle,0,180,0,1024)))
    if idServo == 'y':
        s2.goto(round(Map(angle,0,180,0,1024)))
    if idServo == 'z':
        s3.goto(round(Map(angle,0,180,0,1024)))
    
#Funcion que controla los puente H
def move(m1a, m1b, m2a, m2b):
    pwmDerechadelante.duty_u16(m1a)
    pwmDerechatras.duty_u16(m1b)
    pwmIzquierdaAdelante.duty_u16(m2a)
    pwmIzquierdAtras.duty_u16(m2b)

#Funciones para el contro de giro y navegacion
def adelante(vel):
    move(vel , 0, vel , 0)
    
def atras(vel):
    move(0, vel , 0, vel )
    
def derecha(vel):
    move(0, vel , vel , 0)
    
def izquierda(vel):
    move(vel , 0, 0, vel )
    
def giroderecha(vel):
    move(0 , 0, 0, vel )
    
def giroizquierda(vel):
    move(vel , 0, 0, 0 )

def detenerme(vel):
    move(0, 0, 0, 0)


def autonomo():
    print("autonomo")
    s1_estado = sensor1.value() #izquierda
    s2_estado = sensor2.value() #derecha  
    #Validaciones modo autonomo
    if modo == False and s1_estado==1 and s2_estado==0:
        print("S1")
        velocidad = Map(45, inMin, inMax, outMin, outMax)
        derecha(velocidad)
        utime.sleep(0.05)
                        
    if modo == False and s1_estado==0 and s2_estado==1:
        print("S2")
        velocidad = Map(45, inMin, inMax, outMin, outMax)
        izquierda(velocidad)
        utime.sleep(0.05)
                        
    if modo == False and s1_estado==1 and s2_estado==1:
        print("S4")
        velocidad = Map(13, inMin, inMax, outMin, outMax)
        adelante(velocidad)
        utime.sleep(0.01)

    if modo == False and s1_estado==0 and s2_estado==0:
        print("S4")
        velocidad = Map(13, inMin, inMax, outMin, outMax)
        adelante(velocidad)
        utime.sleep(0.01)


#Antes de iniciar pocisiona los servos XY en el origen
servo_Angle(posSerX, 'x')
utime.sleep(0.5)
servo_Angle(posSerY, 'y')
utime.sleep(0.5)
servo_Angle(posSerZ, 'z')
utime.sleep(0.5)
#Bucle infinito
while True:
    
    #lectura del señal Bluetooth 
    if uart.any():
        command = uart.readline()
        print("Esto llega del celular", command)
        print("pos Y", posSerY)
        print("pos X", posSerX)
        
        #Adecuamos el modo de acuerdo a la entrada desde la interfaz    
        if command == b'z':
            modo = True #Cambiando a modo rc
            print("Modo actual ",modo)
            velocidad = Map(0, inMin, inMax, outMin, outMax)
            detenerme(velocidad)
            utime.sleep(0.01)
            
        elif command == b'y':
            modo = False#Cambiando a modo sensores
            print("Modo actual ",modo)
            velocidad = Map(0, inMin, inMax, outMin, outMax)
            detenerme(velocidad)
            utime.sleep(0.01)
     
        #Validaciones de control remoto
        if modo == True and command == b'c':
            print("adelante")
            velocidad = Map(50, inMin, inMax, outMin, outMax)
            adelante(velocidad)
            utime.sleep(0.1)

        if modo == True and command == b'f':
            print("atras")
            velocidad = Map(50, inMin, inMax, outMin, outMax)
            atras(velocidad)
            utime.sleep(0.1)

            
        if modo == True and command == b'e':
            print("derecha")
            velocidad = Map(40, inMin, inMax, outMin, outMax)
            izquierda(velocidad)
            utime.sleep(0.1)

        if modo == True and command == b'd':
            print("izquierda")
            velocidad = Map(40, inMin, inMax, outMin, outMax)
            derecha(velocidad)
            utime.sleep(0.1)

            
        if modo == True and command == b'g':
            print("parar")
            velocidad = Map(0, inMin, inMax, outMin, outMax)
            detenerme(velocidad)
            utime.sleep(0.1)
            
        #Servomotor Y arriba
        if modo == True and command == b'h':
            dirServo = 'h'
        #Servomotor Y abajo
        if modo == True and command == b'i':
            dirServo = 'i'
        #Servomotor X izquierda 
        if modo == True and command == b'j':
            dirServo = 'j'
        #Servomotor X derecha
        if modo == True and command == b'k':
            dirServo = 'k'
        #Pausa el movimiento de los servos
        if modo == True and command == b'l':
            dirServo = 'l'
        #MOVIMIENTO DEL LASER
        #Arriba
        if modo == True and command == b'p':
            dirServo = 'p'
        #Abajo
        if modo == True and command == b'q':
            dirServo = 'q'
        #Pone los servomotores en el origen
        if modo == True and command == b'o':
            dirServo = 'l'
            servo_Angle(90, 'x')
            utime.sleep(0.2)
            servo_Angle(90, 'y')
            utime.sleep(0.2)
            servo_Angle(90, 'z')
            utime.sleep(0.2)
            
    if dirServo == 'h':
        if posSerY > 171:
            posSerY = 171
        else:
            posSerY = posSerY + angulos
        servo_Angle(posSerY, 'y')
        utime.sleep(0.001)
         
    if dirServo == 'i':
        if posSerY < 30:
            posSerY = 30
        else:
            posSerY = posSerY - angulos
        servo_Angle(posSerY, 'y')
        utime.sleep(0.001)
         
    if dirServo == 'j':
        if posSerX < 0:
            posSerX = 0
        elif posSerX > 180:
            posSerX =180
        else:
            posSerX = posSerX + angulos
        servo_Angle(posSerX, 'x')
        utime.sleep(0.001)

    if dirServo == 'k':
        if posSerX < 0:
            posSerX = 0
        elif posSerX > 180:
            posSerX =180
        else:
            posSerX = posSerX - angulos
        servo_Angle(posSerX, 'x')
        utime.sleep(0.001)
        
    if dirServo == 'p':
        if posSerZ < 0:
            posSerZ = 0
        elif posSerZ > 180:
            posSerZ =180
        else:
            posSerZ = posSerZ + angulos
        servo_Angle(posSerZ, 'z')
        utime.sleep(0.001)
        
    if dirServo == 'q':
        if posSerZ < 0:
            posSerZ = 0
        elif posSerZ > 180:
            posSerZ =180
        else:
            posSerZ = posSerZ - angulos
        servo_Angle(posSerZ, 'z')
        utime.sleep(0.001)

         
    if modo == False:
        autonomo()
        utime.sleep(0.05)
    
    utime.sleep(0.01)
    
