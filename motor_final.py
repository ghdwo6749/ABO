import blynklib
import blynktimer
import RPi.GPIO as GPIO
from time import sleep
BLYNK_AUTH = '39u9Non0p9uN_B8C3B7QnkyFwAfzWFnq'


# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"


# Register Virtual Pins
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
  print(WRITE_EVENT_PRINT_MSG.format(pin,value))

  if(value == ['1']):
    setMotor(CH1, 80, FORWARD)

  else:
    GPIO.output(21, 0)

@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
  print(WRITE_EVENT_PRINT_MSG.format(pin,value))

  if(value == ['1']):
    GPIO.output(20, 1)
  else:
    GPIO.output(20, 0)

# -*- coding: utf-8 -*-


STOP  = 0
FORWARD  = 1
BACKWORD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 26  #37 pin
ENB = 0   #27 pin

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

def setPinConfig(EN, INA, INB):        
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100) 
    pwm.start(0) 
    return pwm

def setMotorContorl(pwm, INA, INB, speed, stat):

    pwm.ChangeDutyCycle(speed)  
    
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
        
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

        
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        setMotorContorl(pwmB, IN3, IN4, speed, stat)
  

GPIO.setmode(GPIO.BCM)
      
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

    

setMotor(CH1, 80, FORWARD)
setMotor(CH2, 80, FORWARD)
sleep(5)

setMotor(CH1, 40, BACKWORD)
setMotor(CH2, 40, BACKWORD)
sleep(5)

setMotor(CH1, 100, BACKWORD)
setMotor(CH2, 100, BACKWORD)
sleep(5)

setMotor(CH1, 80, STOP)
setMotor(CH2, 80, STOP)

while True:
        blynk.run()

GPIO.cleanup()
