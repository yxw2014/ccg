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

from model import *
from service import *
#from model import BaseModel
#from service import BaseService
#from service import FightService
import log
from config import config
from errors import err
from request import request
from response import response
from lib.mongo import Mongo
import redis
#from data import data

from tornado.tcpserver import TCPServer  
from tornado.ioloop  import IOLoop  
from tornado import autoreload  
from tornado import process
from tornado.options import options, define

define('port', type=int, default=8801, help="define the server port")
define('debug', type=bool, default=True, help="debug mode, True or False")
   
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
        
        self.uuid= str(uuid.uuid4())
        #self.uuid= str(451377)
        
        obj= ConnectionObj()
        obj.stream= self._stream
        obj.time= int(time.time())
        obj.uuid= self.uuid    
        
        Connection.clients[self.uuid]=  obj
        redis.zadd('hs:user:session'+ ":"+ server_id, self.uuid, int(time.time()))        
        
        '''
        all_uuids= []
        for id, client in Connection.clients.items(): 
             all_uuids.append({"uuid":id})
         
         
        for id, client in Connection.clients.items(): 
                if id== self.uuid:  
                    encoded_data = {"uuid":self.uuid, "service": "main", "method": "signUpSucceeded", "params":{"all_user": all_uuids}}                     
                else:
                    continue
                    encoded_data = {"uuid":self.uuid, "service": "main", "method": "joinNewPlayer", "params":{"user": {'uuid':self.uuid}}}
                print encoded_data
                reqt= request(encoded_data)
                res= reqt.dump()
                
                client.stream.write_to_fd(res) 
         '''
            
        encoded_data = {"uuid":self.uuid, "service": "main", "method": "signUpSucceeded", "params":{}}
        reqt= request(encoded_data)
        res= reqt.dump()
        self._stream.write_to_fd(res)            
        
        self.read_message()  
        
        print "A new user has entered.", address, self.uuid  
      
    def read_message(self):  
        self._stream.read_until(config['GAME']['msgsuffix'], self.send_message)
          
    """
    def broadcast_messages(self, data):  
        for conn in Connection.clients:  
            conn.send_message(data)  
        self.read_message()  
    """
        
    def parse_message(self, data): 
        #print 'origin data:', data               
        data= data.rstrip(config['GAME']['msgsuffix'])            
        new_data = json.loads(data)
        #print 'new data:', new_data
        
        if(isinstance(new_data, dict)== False):  
            encoded_data = {"error":{"code": 4, "msg": err[4]}, "service":"main", "method":"error", "data":{}}
            reqt= response(encoded_data, self.uuid)
            res= reqt.dump()
            return res
        
        uid= new_data.get("uid")      
        service= new_data.get("service")
        method= new_data.get("method")
        params= new_data.get("params")
        print '---------------parse_message', service, method, params        
       
        cls = getattr(FightService, service, None) 

        if cls== None:
            encoded_data = {"error":{"code": 2, "msg": err[2]}, "service":"main", "method":"error", "data":{}}
            reqt= response(encoded_data, self.uuid)
            res= reqt.dump()
            return res
            
        obj = cls()  
        
        func = getattr(obj, method, None)
        if cls== None:
            encoded_data = {"error":{"code": 3, "msg": err[3]}, "service":"main", "method":"error", "data":{}}
            reqt= response(encoded_data, self.uuid)
            res= reqt.dump()
            return res
       
        data, push_data= func(params)
        #print 'data------', data, push_data
        
        #push         
        if(isinstance(push_data, dict)!= False):         
            if push_data.get('uuid')!= None:
                push_uuid= push_data.get('uuid')         
                friend= Connection.clients.get(push_uuid)
                if(friend== None):
                    encoded_data = {"uuid":self.uuid, "service": "main", "method": "leavePlayer", "params":{"user": {'uuid':push_uuid}}}
                    reqt= request(encoded_data)
                    res= reqt.dump()
                    print "server send lost:", len(res), res, self._address, len(Connection.clients), datetime.datetime.now()
                    self._stream.write(res)
                    return None
                else:
                    reqt= request(push_data)
                    res= reqt.dump()
                    #client.stream.write((''.join(res)).encode('utf8')) 
                    print "---------------server send friend:", len(res), res, self._address, type(Connection.clients), len(Connection.clients), datetime.datetime.now()
                    friend.stream.write(res) 
                
        if data== False or data== None:
            return None
        req= response(data, self.uuid)    
        return req.dump()
    
    def send_message(self, data):  
        #print "User send:", len(data), data, self._address, len(Connection.clients), datetime.datetime.now()
        
        res= self.parse_message(data)  
        if res!= None:
             self._stream.write(res) 
        print "---------------server send:", type(res), res, self._address, len(Connection.clients), datetime.datetime.now()
        
        #push to all connected user
        """
        if(True):                
            for id, client in Connection.clients.items():  
                #res_bin= struct.pack(str(len(res))+'s', res)  
                client.stream.write(res)             
        """
        
        self.read_message()
        
          
    def on_close(self):      
        #Connection.clients[str(self._address[0])+ str(self._address[1])].stream.close()
        del Connection.clients[self.uuid]
        redis.zrem('hs:user:session'+ ":"+ server_id, self.uuid)  
        redis.zrem('hs:user:search'+ ":"+ server_id, self.uuid)
        redis.zrem('hs:room:user'+ ":"+ server_id, self.uuid) 
        """  
        for u, client in Connection.clients.items():    
            encoded_data = {"uuid":u, "service": "main", "method": "leavePlayer", "params":{"user": {'uuid':self.uuid}}}
            reqt= request(encoded_data)
            res= reqt.dump()
            #client.stream.write((''.join(res)).encode('utf8')) 
            client.stream.write(res)   
        """
        print "A user has left.", self.uuid, self._address
        #Connection.clients.remove(self)  
  
class GameServer(TCPServer):  
    def handle_stream(self, stream, address): 
        print "New connection :", address, stream 
        Connection(stream, address) 
  
if __name__ == '__main__':  
    options.parse_command_line()
    
    print "Server start ......"      
    server = GameServer()  
    server.listen(options.port) 
    server_id= str(options.port)
    
    #for mutiprocess
    logger=logging.getLogger()
    handler=logging.FileHandler(log.log_path+ "."+ server_id)
    #very important
    logger.removeHandler(logger.handlers[0])
    logger.addHandler(handler)
    logger.setLevel(log.level)
    logger.error = logger.error
    logger.warn = logger.warning
    logger.info = logger.info
    logger.debug = logger.debug  
    
    cls= BaseService.BaseService
    cls.log= logger
    cls.server_id= server_id     
    
    model= BaseModel.BaseModel
    model.log= logger
    model.server_id= server_id     
    
    mongo= Mongo.getInstance(config['MONGO_STAG']['host'], int(config['MONGO_STAG']['port']))
    mongodb= mongo[config['MONGO_STAG']['db']]
    cls.mongodb= mongodb
    model.mongodb= mongodb    
    
    pool = redis.ConnectionPool(host=config['REDIS_STAG']['host'], port= int(config['REDIS_STAG']['port']), \
                                                    db= int(config['REDIS_STAG']['db']), socket_timeout= 2)  
    redis = redis.Redis(connection_pool= pool)
    cls.redis= redis
    model.redis= redis
    
    redis.delete('hs:user:session'+ ":"+ server_id, 'hs:user:search'+ ":"+ server_id)   
     
    loop= IOLoop.instance()
    autoreload.start(loop)
    loop.start()
    
    
    
    
    