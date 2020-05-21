import socket

#파이 컨트롤 함수
def do_some_stuffs_with_input(input_string):
	#라즈베리파이를 컨트롤할 명령어 설정
	if input_string == "left":
		input_string = "좌회전 합니다."
		#파이 동작 명령 추가할것
	elif input_string == "right":
		input_string = "우회전 합니다."
	elif input_string == "up":
		input_string = "위로 갑니다."
	elif input_string == "down":
		input_string = "아래로 갑니다."
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


