# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from errors import err
from  BaseService import BaseService
from pymongo.errors import AutoReconnect
						
class UserService(BaseService): 
	def __init__(self): 
		super(FightService, self).__init__()		
		
	
	def register(self, uid, params):
		if(uid== None or isinstance(params, dict)== False or params.get('uuid')== None or params.get('name')== None): 
				self.result["error"]= {"code":1, "msg": err[1]}           
				return self.result, None
		uuid= params.get('uuid')
		name= params.get('name')
		data={
			"_id":uuid,
			"uid":uid,
			"name":name,
			"login_time": int(time.time()),
			"create_time": int(time.time()),
			"extend_info":{}
		}
				
		try:
			_id= self.mongodb['hs_user'].insert(data)
			userinfo= self.mongodb['hs_user'].find_one({"_id":_id})
			#ret= mongodb['hs_user'].find_and_modify(query={"_id":uuid}, update={"$set":data}, upsert= True, new= True)
			
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			pass	
		return userinfo, None		
		
	
	def login(self, uid, params): 
		if(uid== None or isinstance(params, dict)== False or params.get('uuid')== None): 
				self.result["error"]= {"code":1, "msg": err[1]}           
				return self.result, None
		uuid= params.get('uuid')
		
		try:
			#userinfo= self.mongodb['hs_user'].find_one({"uid": uid})
			userinfo= self.mongodb['hs_user'].find_and_modify(query={"uid": uid}, update={"$set":{"login_time": int(time.time())}})			
			if(userinfo== None):
				return self.register(uid, params)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			pass	
				
		return userinfo, None
	
	def __getUserInfoByUid(self, uid): 
		if(uid== None):      
			return None
		
		try:
			userinfo= self.mongodb['hs_user'].find_one({"uid": uid})		
			return  userinfo
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			pass	
		
	def __getUserInfoByUuid(self, uuid): 
		if(uuid== None):      
			return None
		
		try:
			userinfo= self.mongodb['hs_user'].find_one({"_id": uuid})		
			return  userinfo
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			pass				

		
	