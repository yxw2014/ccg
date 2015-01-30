# -*- coding: utf-8 -*-

import socket  
import time
import sys
import json 
import datetime
import struct

encodedjson = '{"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "testMethod", "params":{"fightid": 451377}}'

def clint():
     #host = '50.23.111.162'
     host = '127.0.0.1'
     port = 9526
     bufsize = 1024
     addr = (host,port)
     client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     client.connect(addr)
     global encodedjson
     while True:
          print encodedjson   
          encodedjson= encodedjson+ '##'  
          encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson)  
          client.sendall(encodedjson)
        
          while 1:            
              try:
                  revcdata = client.recv(256)
                  print revcdata
                  print i, datetime.datetime.now()
             
                  if not revcdata:
                      print 'None'
                      #break 
                      
              except:
                      pass
                      #print 'except'
     
     #client.close() 

if __name__ == '__main__':   
    clint()                 
