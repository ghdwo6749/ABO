import socket
import RPi.GPIO as GPIO
from time import sleep

# -*- coding: utf-8 -*-


STOP  = 0
FORWARD  = 1
BACKWARD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 1   #28 pin
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
        
    elif stat == BACKWARD:
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

#파이 컨트롤 함수
def do_some_stuffs_with_input(input_string):
    #라즈베리파이를 컨트롤할 명령어 설정
    if input_string == "left":
        #input_string = "좌회전 합니다."
        setMotor(CH1 , 40 , FORWARD)
        setMotor(CH2 , 40 , BACKWARD)
    elif input_string == "right":
        input_string = "우회전 합니다."
        setMotor(CH1 , 40 , BACKWARD)
        setMotor(CH2 , 40 , FORWARD)
    elif input_string == "up":
        input_string = "위로 갑니다."
        setMotor(CH1 , 40 , FORWARD)
        setMotor(CH2 , 40 , FORWARD)
    elif input_string == "down":
        input_string = "아래로 갑니다."
        setMotor(CH1 , 40 , BACKWARD)
        setMotor(CH2 , 40 , BACKWARD)
    elif input_string == "stop" :
        setMotor(CH1 , 0 , FORWARD)
        setMotor(CH2 , 0 , BACKWARD)
    else :input_string ="null"
    return input_string


HOST = ""
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
s.bind((HOST, PORT))
print ('Socket bind complete')
s.listen(1)
print ('Socket now listening')


#접속 승인
conn, addr = s.accept()
print("Connected by ", addr)
while True:

        
	#데이터 수신
        data = conn.recv(1024)
        data = data.decode("utf8").strip()
        if not data: break
        print("Received: " + data)

	#수신한 데이터로 파이를 컨트롤
        res = do_some_stuffs_with_input(data)
        print("파이 동작 :" + res)

	#클라이언트에게 답을 보냄
        conn.sendall(res.encode("utf-8"))

        if data == "END" :
                break;
	
	

#연결 닫기
conn.close()	
s.close()


