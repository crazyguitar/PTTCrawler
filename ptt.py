import socket
import time
import sys
# coding=utf-8

class socketObj:

   def __init__(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

   def connect(self):
      self.sock.connect(('ptt.cc',23))

   def recvMsg(self):
      return self.sock.recv(65535)
      

   def sendMsg(self,msg):
      self.sock.send(msg)

   def printMsg(self,msg):
      print msg

   def closeSocket(self):
      self.sock.close()

class boardObj:

   def __init__(self):
      self.boardsList = []
   
   def readBoardFromFile(self,fileName):
      readFile = open(fileName,'r')
      while True:
         line = readFile.readline()
         if not line:
            break;
         self.boardsList.append(line)
      
      print self.boardsList
      readFile.close()

if __name__ == '__main__':

   sock = socketObj()
   sock.connect()
   boards = boardObj()
   boards.readBoardFromFile('boards.txt')


   # recv watting msg
   msg = sock.recvMsg()
   sock.printMsg(msg)
   time.sleep(1.5)
   # recv login view msg
   msg = sock.recvMsg()
   sock.printMsg(msg)
   # input account and password
   sock.sendMsg(sys.argv[1]+'\r')
   time.sleep(1.5)
   msg = sock.sendMsg(sys.argv[2]+'\r')
   time.sleep(1.5)
   msg = sock.recvMsg()
   sock.printMsg(msg)
   time.sleep(1)
   # go to main menue
   sock.sendMsg('\r')
   time.sleep(1.5)
   msg = sock.recvMsg()
   sock.printMsg(msg)

   


   sock.closeSocket()
