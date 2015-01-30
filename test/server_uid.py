# -*- coding: utf-8 -*-

import sys,os,time
import json
import uuid
import string
import datetime
import struct

reload(sys) 
sys.setdefaultencoding('utf-8') 

sys.path.append('./')
sys.path.append('./lib')
sys.path.append('./config')
sys.path.append('./service')
sys.path.append('./model')

from model import *
from service import *
import log
from config import config
from errors import err
from request import request
from response import response

from tornado.tcpserver import TCPServer  
from tornado.ioloop  import IOLoop  
from tornado import autoreload  
from tornado import process 


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
        
        self.uuid= str(uuid.uuid1())
        
        obj= ConnectionObj()
        obj.stream= self._stream
        obj.time= int(time.time())
        obj.uuid= self.uuid    
        
        Connection.clients[self.uuid]=  obj
        
        
        version= '2013.11.13.00.00.00'
        all_uuids= []
        for id, client in Connection.clients.items(): 
             all_uuids.append({"uuid":id})
         
        #stream.write((res+ config['GAME']['msgSuffix']).encode('utf8')) 
        #stream.write(res.encode('utf8'))        
        #res_bin=  struct.pack(str(len(res))+'s', res)   
           
        for id, client in Connection.clients.items(): 
                if id== self.uuid:  
                    encoded_data = {"uuid":self.uuid, "service": "main", "method": "signUpSucceeded", "params":{"all_user": all_uuids}}                     
                else:
                    encoded_data = {"uuid":self.uuid, "service": "main", "method": "joinNewPlayer", "params":{"user": {'uuid':self.uuid}}}
                #print encoded_data
                reqt= request(encoded_data)
                res= reqt.dump()                
                client.stream.write_to_fd(res) 
                    
        
        self.read_message()  
        
        print "A new user has entered.", address, self.uuid  
      
    def read_message(self):  
        self._stream.read_until('##', self.send_message)  
  
    def broadcast_messages(self, data):  
        for conn in Connection.clients:  
            conn.send_message(data)  
        self.read_message()  

        
    def parse_message(self, data): 
        print 'origin data:'+ data               
        data= data.rstrip('##')            
        new_data = json.loads(data)
        print new_data
        
        uid= new_data.get("uid")
        print self.uid        
        service= new_data.get("service")
        method= new_data.get("method")
        params= new_data.get("params")
        
        """
        service= 'TestService'
        method= 'testMethod'
        params= {}
        """
    
        cls = getattr(TestService, service) 
        obj = cls()
        func = getattr(obj, method)
        
        data= func(params)
        req= response(data)
        #print req.dump()
        return req.dump()
    
        return data
    
    def send_message(self, data):  
        #print "User send:", len(data), type(data), data, self._address, len(Connection.clients), datetime.datetime.now()
        #self._stream.write(data) 
        #self.read_message()
     
        #res= self.parse_message(data)
        #self._stream.write(res)   
        
        #self._message.append(data)
        #if(len(self._message)>= 1):  
        if(True):                
            for id, client in Connection.clients.items():  
                #res= ''.join(self._message)
                #res= data.decode('utf8').encode('utf8')
                
                res= data
                
                #res= struct.pack(str(len(res))+'s', res)
                #print res[2::]
                #print "%3s" % res[0].encode('hex'),"%3s" % res[1].encode('hex')
                
                #res_bin= struct.pack(str(len(res))+'s', res[2::])          
                res_bin= struct.pack(str(len(res))+'s', res) 
                #print len(res_bin) , type(res_bin)
                client.stream.write(res_bin) 
                
            self._message= []        
     
        #Connection.clients[self.uid].stream.write(data)
        #for uuid, client in Connection.clients.items():
            #client.stream.write(res.encode('utf8'))
        self.read_message()
        
          
    def on_close(self):          
        #Connection.clients[str(self._address[0])+ str(self._address[1])].stream.close()
        del(Connection.clients[self.uuid])
        for id, client in Connection.clients.items():    
            encoded_data = {"uuid":id, "service": "main", "method": "leavePlayer", "params":{"user": {'uuid':self.uuid}}}
            reqt= request(encoded_data)
            res= reqt.dump()
            #client.stream.write((''.join(res)).encode('utf8')) 
            client.stream.write(res)     
        print "A user has left.", self.uuid, self._address
        #Connection.clients.remove(self)  
  
class GameServer(TCPServer):  
    def handle_stream(self, stream, address): 
        print "New connection :", address, stream 
        Connection(stream, address) 
  
if __name__ == '__main__':  
    print "Server start ......"  
    server = GameServer()  
    server.listen(9528) 
     
    logger = log.get_logger(log.log_path, log.level)
    log.error = logger.error
    log.warn = logger.warning
    log.info = logger.info
    log.debug = logger.debug
    
    loop= IOLoop.instance()
    autoreload.start(loop)
    loop.start()
    
    