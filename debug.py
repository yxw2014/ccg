from  model.CardModel import CardModel
from  model.HeroModel import HeroModel
from  model.RoomModel import RoomModel

import sys, json, random,redis

from config import config
from model import BaseModel
from lib.mongo import Mongo

from pprint import pprint

model= BaseModel.BaseModel
"""
mongo= Mongo.getInstance(config['MONGO_STAG']['host'], int(config['MONGO_STAG']['port']))
mongodb= mongo[config['MONGO_STAG']['db']]
model.mongodb= mongodb 
print CardModel.getFirstCards()
"""

pool = redis.ConnectionPool(host=config['REDIS_STAG']['host'], port= int(config['REDIS_STAG']['port']), \
                                                    db= int(config['REDIS_STAG']['db']), socket_timeout= 2)  
redis = redis.Redis(connection_pool=pool)
model.redis= redis

r= RoomModel.getRoom("881397070")
'''
print(len(r["cardAll1"]))
print(len(r["cardAll2"]))

print(len(r["cardHand1"]))
print(len(r["cardHand2"]))
'''
pprint(r)


