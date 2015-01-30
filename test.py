from  model.CardModel import CardModel
from  model.HeroModel import HeroModel
from  model.RoomModel import RoomModel

import sys, json, random

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

class A:

	def bbb(self):
		self.__aaa()
		print 'bbb'

	def __aaa(self):
		print 'aaa'

aa= A()
aa.bbb()
print A.__aaa
print A.bbb