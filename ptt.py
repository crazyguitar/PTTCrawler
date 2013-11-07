#!/usr/bin/env python
# coding=utf-8

import socket
import time
import sys
import re

class socketObj:

   def __init__(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
      self.sock.settimeout(5)

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
   
   def writeBoardToFile(self, fileName,msg):
      writeFile = open(fileName,'a')
      writeFile.write(msg)
      writeFile.close()


class pttParser:

   def __init__(self):
      self.sock = socketObj()
      self.sock.connect()

   def login(self,ID,password):
      
      # recv watting msg
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)
      time.sleep(1.5)

      # recv login view msg
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)

      # input account and password
      self.sock.sendMsg(ID+'\r'+password+'\r')
      time.sleep(1.5)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)
      
      # go to main menue
      self.sock.sendMsg('\r')
      time.sleep(1.5)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)

   def searchBoard(self,boardName):
      
      # send search command 's'
      self.sock.sendMsg('s')
      time.sleep(0.5)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)
      
      # send search board's name
      searchBoardStr = boardName + '\r'
      self.sock.sendMsg(searchBoardStr)
      time.sleep(1)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg.decode('big5').encode('utf-8'))

   def searchPopularPost(self):

      # search
      self.sock.sendMsg('Z')
      time.sleep(0.5)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)

      # post larger than 100
      self.sock.sendMsg('100\r')
      time.sleep(1)
      msg = self.sock.recvMsg()
      self.sock.printMsg(msg)

   def parseArticle(self,numberOfArticle):
      
      for i in range(numberOfArticle):
         self.sock.sendMsg('r')
         time.sleep(1)
         msg = self.sock.recvMsg()
         self.sock.printMsg(msg)
         if not msg:
            continue
         match = re.findall(' \d*/\d* ',msg)
         
         if match:
            currentPageList = match[-1].split('/')
            currentPage = int(currentPageList[0])
            totalPage = int(currentPageList[1])
            # print "(%d/%d)" % (currentPage, totalPage)
            while totalPage != currentPage:
               command = "%c" % 6
               self.sock.sendMsg(command)
               time.sleep(1)
               msg = self.sock.recvMsg()
               self.sock.printMsg(msg)
               currentPage += 1

         self.sock.sendMsg('qk')
         time.sleep(1)
         msg = self.sock.recvMsg()
         self.sock.printMsg(msg)

   def closeParserSocket(self):

      self.sock.closeSocket()


if __name__ == '__main__':
   
   boards = boardObj()
   boards.readBoardFromFile('boards.txt')
   pttParserObj = pttParser()
   pttParserObj.login(sys.argv[1],sys.argv[2])

   for item in boards.boardsList:

      pttParserObj.searchBoard(item) 
      pttParserObj.searchPopularPost()      
      pttParserObj.parseArticle(5)
      
      # write get result to file
      # boards.writeBoardToFile('PTT.txt',msg)

   
   pttParserObj.closeParserSocket
