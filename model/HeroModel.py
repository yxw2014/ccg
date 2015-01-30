# -*- coding: utf-8 -*-

'''
用户套牌管理模块
'''
import sys
import os
import random
import time
import json
import random
from errors import err
from model.BaseModel import BaseModel
from pymongo.errors import AutoReconnect
						
class HeroModel(BaseModel): 
	def __init__(self): 
		super(HeroModel, self).__init__()		
	"""
	@classmethod
	def getAllHeros(self):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_hero'].find():
				#for item in self.mongodb['hs_cards'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		return ret
	
	@classmethod
	def getAllUserHeros(self, uuid):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_user_hero'].find({"uuid": uuid}):
				#for item in self.mongodb['hs_cards'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
	
		return ret
	
	@classmethod
	def getAllSystemAndUserHeros(self, uuid):
		ret= []
		
		job_info= self.getUserAllJobInfo(uuid)
		
		system_hero= self.getAllHeros()
		for hero in system_hero:
			hero['uuid']= uuid
			hero['type']= '1'
			hero['aliasName']= ''
			hero['creatTime']= 0
			hero['level']= 0
			hero['xp']= 0
			hero['jobCards']= hero['jobCards'].split(',')
			if job_info.get(hero['job']) !=None and job_info.get(hero['job']).get('level') !=None:
				hero['level']= job_info.get(hero['job']).get('level')
				
			if job_info.get(hero['job']) !=None and job_info.get(hero['job']).get('xp') !=None:
				hero['xp']= job_info.get(hero['job']).get('xp')
		ret.extend(system_hero)
		
		user_hero= self.getAllUserHeros(uuid)
		
		for hero in user_hero:	
			if job_info.get(hero['job']) !=None and job_info.get(hero['job']).get('level') !=None:
				hero['level']= job_info.get(hero['job']).get('level')
				
			if job_info.get(hero['job']) !=None and job_info.get(hero['job']).get('xp') !=None:
				hero['xp']= job_info.get(hero['job']).get('xp')			
		
		
		ret.extend(user_hero)
		
		return ret
	
	@classmethod
	def getHeros(self, num=1):
		ret= []
		try:
			#data= self.mongodb['hs_cards'].find()	
			for item in self.mongodb['hs_hero'].find().limit(num):
				#for item in self.mongodb['hs_cards'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
	
		return ret
	
	@classmethod
	def getHerosByRand(self, num= 1):
		ret= []
	
		try:
			'''
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
			'''	
			sort= random.randint(-1, 1)
			
			for item in self.mongodb['hs_hero'].find().sort("rand", sort).limit(num*2):
				#for item in self.mongodb['hs_cards'].find():
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
		
		ret= random.sample(ret, num)		
		return ret
	"""	

	@classmethod
	def getHerosById(self, id): 
		if(id== None):      
			return None
		
		try:
			data= self.mongodb['hs_hero'].find_one({"_id": id})		
			return  data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			
	@classmethod
	def getUserHerosById(self, userId, uHeroId): 
		'''
		根据用户套牌id获取套牌信息
		@summary: modified by tm 2014-01-26
		'''
		if(id == None or userId == None):      
			return None
		
		try:
			#data= self.mongodb['hs_user_hero'].find_one({"userId": userId,"_id": id})
			data = self.mongodb['hsg_user_hero'].find_one({"_id": uHeroId})
			if not data:
				print 'the hero with id:' + str(uHeroId) + ' is not exists'
				return None
			#return data
			heroInfo = self.getHerosByJob(data['job'])
			if not heroInfo:
				print 'the hero\'s job named ' + data['job'] + ' with id:' + str(uHeroId) + ' is not exists'
				return None
				
			return dict(heroInfo, **data)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
	
	@classmethod
	def getSystemOrUserHerosById(self, userId, id): 
		if(id== None or userId== None):      
			return None
		'''
		if id< 1000000:
			data= self.getHerosById(id)
			if data!= None:
				data['type']=1 
				data['uuid']=uuid 
				data['createTime']= 0
				data['aliasName']= ''
				data['jobCards']= data['jobCards'].split(',')
				for k, v in enumerate(data['jobCards']):
					data['jobCards'][k]= int(v)			
		else:
		'''
		data= self.getUserHerosById(userId, id)

		if data!= None:
			job= data['job']
			job_info= self.getUserJobInfo(userId, job)
			data['xp']= 0 
			data['level']= 0 
			if job_info and job_info.get('level')!= None and job_info.get('xp')!= None:
				data['xp']= job_info.get('xp') 
				data['level']=job_info.get('level')
			for k, v in enumerate(data['jobCards']):
					data['jobCards'][k]= int(v)	
		
		return data
			
		
	@classmethod
	def getHerosByJob(self, job): 
		if(job== None):      
			return None
		
		try:
			data= self.mongodb['hs_hero'].find_one({"job": job})		
			return  data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

	"""	
	@classmethod
	def updateUserHeros(self, id, cardIds):
		if isinstance(id, int)== False or isinstance(cardIds, list)== False:
			return False
		
		try:
			ret= self.mongodb['hs_user_hero'].update({"_id": id}, {"$set": {"jobCards": cardIds}})
	
			return  ret
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
	
	
	@classmethod
	def deleteUserHeros(cls, userId, uCardId):
		'''
		删除用户的套牌
		@param userId: 用户编号
		@param uCardId: 用户套牌编号
		@return: 成功则返回删除成功描述的字典，否则返回None
		@author: tanming
		'''
		try:
			ret = self.mongodb['hs_user_hero'].remove({'_id': uCardId});
			return ret
		except AutoReconnect:
			cls.log.error("mongodb error, AutoReconnect!")
		
		return None;
		
	@classmethod
	def createUserHeros(self, uuid, job, name, cardIds):
		hero= self.getHerosByJob(job)
		if hero== None:
			return False
		
		hero_name, element, atk, hp, skillId, skillCardId, flavorText, img= hero['name'], hero['element'], hero['atk'], hero['hp'], hero['skillId'], hero['skillCardId'], hero['flavorText'], hero['img']
		
		t= int(time.time())
		data= {
			'uuid': uuid,
			
			'aliasName':name,
			'name':hero_name,
			'job':job,
			'element':element,
			'atk': atk,
			'hp':hp,
			'skillId': skillId,
			'skillCardId': skillCardId,
			'flavorText': flavorText,	
			'img': img,
			'jobCards':cardIds,
			
			'type': 0,
			#'level':0,
			#'xp': 0,	
			'creatTime': t,
			
			#'_id': t+ ord(uuid[0])+ ord(uuid[1])+ ord(uuid[2])+ ord(uuid[3]),
			'_id': t+ ord(uuid[0]),								
		}
		
		try:
			ret= self.mongodb['hs_user_hero'].insert(data)		
			return  ret
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

	"""
	
	@classmethod
	def getUserJobInfo(self, userId, job): 
		if(job== None or userId== None):      
			return None
		
		try:
			data= self.mongodb['hs_user_job'].find_one({"userId": userId, "job": job})		
			return data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
		
	@classmethod
	def getUserAllJobInfo(self, userId): 
		if(userId== None):      
			return None
		
		ret= {}
		try:

			for j in self.mongodb['hs_user_job'].find({"userId": userId}):
				#make a dict
				ret[j['job']]= j
				
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
		
		return ret
	
	
	
				

		
	