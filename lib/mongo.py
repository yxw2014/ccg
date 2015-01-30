# -*- coding: utf-8 -*-
from pymongo import MongoClient


class Mongo(object):

    mongo_instance= None

    @staticmethod 
    def connect(host, port):    
        return MongoClient(host= host, port= port, connectTimeoutMS= 2000, socketTimeoutMS= 2000)

    @staticmethod 
    def getInstance(host, port):    
        if(Mongo.mongo_instance == None):
            Mongo.mongo_instance= Mongo.connect(host, port)
            return Mongo.mongo_instance
        else:
            return Mongo.mongo_instance    
