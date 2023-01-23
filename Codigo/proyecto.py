#Librerías
import RPi.GPIO as GPIO
import adafruit_dht
import time

#Definición de sensor
dht= adafruit_dht.DHT11(12)
GPIO.setmode(GPIO.BCM)

#Terminales GPIO para el Proyecto
GPIO_TRIGGER = 18 # Trigger sensor ultrasónico
GPIO_ECHO = 24 # Echo sensor ultrasónico
GPIO_INTRUSOS = 17 # Detección de intrusos
GPIO_NO_INTRUSOS = 27 # Sin detección de intrusos

#Dirección de terminales (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) # Trig salida
GPIO.setup(GPIO_ECHO, GPIO.IN) # Echo entrada
GPIO.setup(GPIO_INTRUSOS,GPIO.OUT) # Led salida (rojo)
GPIO.setup(GPIO_NO_INTRUSOS,GPIO.OUT) # Led salida (entrada)

def distance():
  # set Trigger to HIGH
  GPIO.output(GPIO_TRIGGER, True)
  # set Trigger after 0.01ms to LOW
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  StartTime = time.time()
  StopTime = time.time()
  # tiempo de inicio
  while GPIO.input(GPIO_ECHO) == 0:
    StartTime = time.time()
  # tiempo de llegada
  while GPIO.input(GPIO_ECHO) == 1:
    StopTime = time.time()
  # tiempo de diferencia entre que inicia y regresa la señal
  TimeElapsed = StopTime - StartTime
  # multiplicamos por la velocidad del sonido (34300 cm/s)
  # y dividimos entre 2, por ser ida y vuelta
  distance = (TimeElapsed * 34300) / 2
return distance
if __name__ == '__main__':
  try:
    while True:
      dist = distance()
      print ("Measured Distance = %.1f cm" % dist)
      # Si distancia es menor a 5 cm encendemos led de intrusos
      # y apagamos led de no intrusos
      if dist <= 5.0:
        GPIO.output(GPIO_INTRUSOS,True)
        GPIO.output(GPIO_NO_INTRUSOS,False)
      # Si distancia es mayor a 5 cm encendemos led de no intrusos
      # y apagamos led de intrusos
      else:
        GPIO.output(GPIO_INTRUSOS,False)
        GPIO.output(GPIO_NO_INTRUSOS,True)
        time.sleep(1)
  # Ctrl+C detiene proceso
  except KeyboardInterrupt:
    print("Medición detenida por usuario")
    GPIO.cleanup()
