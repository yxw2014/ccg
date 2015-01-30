# -*- coding: utf-8 -*-

import sys,os,time
import json

import config
sys.path.append('./')
sys.path.append('./lib')
sys.path.append('./config')
sys.path.append('./service')
sys.path.append('./model')

from model import *
from service import *
import log
from errors import err
from response import response

from tornado.tcpserver import TCPServer  
from tornado.ioloop  import IOLoop  
from tornado import autoreload  
from tornado import process 

reload(sys) 
sys.setdefaultencoding('utf-8') 


class ConnectionObj(object): 
        def __init__(self):         
            self.stream = None  
            self.time = None  

     
class Connection(object):  
    clients = {}  
    def __init__(self, stream, address):         
        self._stream = stream  
        self._address = address  
        self._stream.set_close_callback(self.on_close)  
        self.read_message()  
        print "A new user has entered.", address 
      
    def read_message(self):  
        self._stream.read_until('##', self.send_message)  
  
    def broadcast_messages(self, data):  
        #print "User said:", data, self._address
        for conn in Connection.clients:  
            conn.send_message(data)  
        self.read_message()  

        
    def parse_message(self, data): 
        print data               
        data= data.rstrip('##')   
        
        obj= ConnectionObj()
        obj.stream= self._stream
        obj.time= 123456789        
        Connection.clients[str(self._address[0])+ str(self._address[1])]=  obj
        return data  
      
        new_data = json.loads(data)   
        print "data:"+data      
        print new_data
        self.uid= new_data.get("uid")
        print self.uid
        service= new_data.get("service")
        method= new_data.get("method")
        params= new_data.get("params")
        
        """
        service= 'TestService'
        method= 'testMethod'
        params= {}
        """
        obj= ConnectionObj()
        obj.stream= self._stream
        obj.time= 123456789        
        Connection.clients[str(self.uid)+ self._address[1]]=  obj
        #print Connection.clients[self.uid].time     
        
        
        cls = getattr(TestService, service) 
        obj = cls()
        func = getattr(obj, method)
        
        data= func(params)
        req= response(data)
        #print req.dump()
        #return req.dump()
    
        return data
    
    def send_message(self, data):  
        #print "User said:", data[:-1], self._address
        res =self.parse_message(data)
        #self._stream.write(res)          
     
        #Connection.clients[self.uid].stream.write(data)
        for k, client in Connection.clients.items():
            client.stream.write((res+ "##").encode('utf8'))
        self.read_message()
        
          
    def on_close(self):          
        #Connection.clients[str(self._address[0])+ str(self._address[1])].stream.close()
        del(Connection.clients[str(self._address[0])+ str(self._address[1])])
        print "A user has left.", self._address
        #Connection.clients.remove(self)  
  
class GameServer(TCPServer):  
    def handle_stream(self, stream, address): 
        print "New connection :", address, stream 
        Connection(stream, address) 
        print "connection num is:", len(Connection.clients)
  
if __name__ == '__main__':  
    print "Server start ......"  
    server = GameServer()  
    server.listen(9527)  
    logger = log.get_logger(log.log_path, log.level)
    log.error = logger.error
    log.warn = logger.warning
    log.info = logger.info
    log.debug = logger.debug
    loop= IOLoop.instance()
    autoreload.start(loop)
    loop.start() 