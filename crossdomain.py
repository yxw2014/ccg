# -*- coding: utf-8 -*-

import sys,os,time
import json
import uuid
import string
import datetime
import struct
import logging
from pprint import pprint

sys.path.append('./')
sys.path.append('./lib')
sys.path.append('./config')
sys.path.append('./service')
sys.path.append('./model')

import log
from config import config
from errors import err


from tornado.tcpserver import TCPServer  
from tornado.ioloop  import IOLoop  
from tornado import autoreload  
from tornado import process
from tornado.options import options, define

define('port', type=int, default=843, help="define the server port")
define('debug', type=bool, default=False, help="debug mode, True or False")
   
class ConnectionObj(object): 
    def __init__(self):   
        self.uuid = None       
        self.stream = None  
        self.time = None  

     
class Connection(object):  
    clients = {}  

    def __init__(self, stream, address):     
        self._stream = stream  
        self._address = address  
        self._message = []
        self._stream.set_close_callback(self.on_close)        
        
        self.read_message()  
        
        print "A new Crossdomain user has entered.", address, self.uuid  
      
    def read_message(self):  
        self._stream.read_until("<policy-file-request/>\0", self.send_message)     

    
    def send_message(self, data):  
        print data
        res= """<?xml version="1.0"?> 
<cross-domain-policy>
    <allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>\0"""
        print res
        self._stream.write(res)
        #self._stream.close()
        #self.read_message()
        
          
    def on_close(self):  
        print "Connection closed:", self._address 
        pass    

  
class GameServer(TCPServer):  
    def handle_stream(self, stream, address): 
        print "New Crossdomain connection :", address, stream 
        Connection(stream, address) 
  
if __name__ == '__main__':  
    options.parse_command_line()
    
    print "Crossdomain Server start ......"      
    server = GameServer()  
    server.bind(options.port) 
    server_id= str(options.port)
     
    #loop= IOLoop.instance()
    #autoreload.start(loop)

    server.start(1)
    IOLoop.instance().start()
            
            

    
    