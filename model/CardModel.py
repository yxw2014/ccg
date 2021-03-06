# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from errors import err
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from pymongo.errors import AutoReconnect
						
class CardModel(BaseModel): 
	def __init__(self): 
		super(CardModel, self).__init__()	
		
	@classmethod	
	def getAllCards(self):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_card'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		return ret
	'''
	@classmethod
	def getCards(self, num=10):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_card'].find().limit(num):
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		return ret
	'''

	'''
	@classmethod
	def getCardsByRand(self, num=30):
		ret= []
	
		try:
			if num <= 1:
				find_num= random.randint(20, 40)
			elif num <= 5:
				find_num= num*8
			elif num <= 10:
				find_num= num*4
			elif num <= 20:
				find_num= num*2+ random.randint(5, 10)
			elif num <= 30:
				find_num= num*2+ random.randint(5, 10)
				
			sort= random.randint(-1, 1)
			
			for item in self.mongodb['hs_card'].find().sort("rand", sort).limit(find_num):	
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		#todo, get the random cards
		ret= random.sample(ret, num)
		return ret
		
	'''	
	@classmethod
	def getCardsById(self, id): 
		if(id== None):      
			return None
		
		try:
			data= self.mongodb['hs_card'].find_one({"_id": id})	
			return  data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
		
	@classmethod
	def getCrystalCard(self): 
		if(id== None):      
			return None
		
		try:
			#data= self.mongodb['hs_card'].find_one({'name':'Second Player Coin'})
			data= self.mongodb['hs_card'].find_one({'_id': 900001})
			if data!= None:
				data['uniqid']= self.getUniqid(data['_id'])	
			return  data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

	
	@classmethod
	def getCardsByIds(self, ids=[]):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_card'].find({"_id":{'$in':ids}}):
				#for item in self.mongodb['hs_cards'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		return ret
	
	@classmethod
	def getUniqid(self, id):
		if id> 1000000000:
			id= id % 1000
		return int(time.time())+  id + random.randint(1000000, 9999999)
	
	
	
	