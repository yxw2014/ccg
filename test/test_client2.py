# -*- coding: utf-8 -*-

import socket  
import time
import sys
import json 
import datetime
import struct

reload(sys) 
sys.setdefaultencoding('utf-8') 

encodedjson = '{"uid":3022, "version": "2013.11.12.10.31.00", "service": "TestService", "method": "testMethod", "params":{"fightid": 451377}}'

def clint():
     global encodedjson
     host = '50.23.111.162'
     #host = '127.0.0.1'
     port = 9528
     bufsize = 1024
     addr = (host,port)
     client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     client.connect(addr)
     i= 0
     while i< 20:          
          #print encodedjson   
          encodedjson= encodedjson+ '##'  
          encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson)  
          print len(encodedjson)        
          client.sendall((encodedjson))
          
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          client.sendall((encodedjson))
          
          #client.sendall(encodedjson2+ '\r\n')       
         
          while 1> 0:
               
              try:
                  revcdata = client.recv(512)                  
                  
                  #print '------------'
				  #i= i+ 1
                  le= len(revcdata)
                  #res_bin=  struct.pack(str(le)+'s', res)
                  print revcdata
                  #print len(revcdata)
                  #print (struct.unpack(str(le)+'s', revcdata))[0]
                  #print revcdata
                  #print '------------'
             
                  if not revcdata:
                      print 'not'
                      break 
                      
              except:
                      print 'except'
                      break
          print i, datetime.datetime.now()
          i= i+ 1
     while 1:
         pass
     client.close() 

if __name__ == '__main__':   
    clint()                 
