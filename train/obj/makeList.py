#-*- coding:utf-8 -*-
import os
import sys

CURRENT_DIR = os.getcwd()

def progressBar(value, endvalue, bar_length=20):
  percent = float(value) / endvalue
  arrow = '-' * int(round(percent * bar_length)-1) + '>'
  spaces = ' ' * (bar_length - len(arrow))

  sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
  sys.stdout.flush()

def returnFileList(dirname, extract):
  fileList = []
  filenames = os.listdir(dirname)
  for filename in filenames:
    ext = os.path.splitext(filename)[-1]
    if ext == extract: 
      fileList.append(filename)
  return fileList

with open("./list.txt","w") as fileList:
  fileNames = returnFileList(CURRENT_DIR, ".jpg")
  
  for i, fileName in enumerate(fileNames):
    fileList.write(CURRENT_DIR+"\\"+fileName+"\n")
    progressBar(i, len(fileNames), bar_length=100)
