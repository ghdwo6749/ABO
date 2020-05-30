import cv2
from datetime import datetime
import time
import os
import shutil
import ftplib

now = datetime.now()
timeValue = now.strftime("%Y-%m-%d_%H%M%S")
fileName =timeValue+'.mp4'

def name_return(fileName):
    return fileName

print(fileName)
print(type(fileName))


cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

# 컬러 영상 저장시
writer = cv2.VideoWriter(fileName, fourcc, 30.0, (width, height))
# 그레이스케일 영상 저장시
# writer = cv2.VideoWriter('output.avi', fourcc, 30.0, (width, height), 0)

while True:
    ret,img_color = cap.read()

    if ret == False:
        break

    cv2.imshow("Color", img_color)

    writer.write(img_color)
    print(name_return(fileName))

    if cv2.waitKey(1)&0xFF == 27:

        break

cap.release()
writer.release()
cv2.destroyAllWindows()


ftp=ftplib.FTP()
ftp.connect("223.194.33.57",21)
ftp.login("FTP_server","7482")
ftp.cwd("ABO/")
os.chdir('C:\\Users\\PSPICE\\Desktop\\')
myfile = open(fileName,'rb')
ftp.storbinary('STOR ' +fileName, myfile )
ftp.close
