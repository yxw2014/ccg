# -*- coding: utf-8 -*-
'''
用户套牌管理接口
'''
from  django.http import HttpResponse
from  HeroModel import HeroModel
#import json

from vo import *
from base import Base
import bson

class HeroService(Base):
	'''
	套牌相关service
	'''
	
	'''
	@classmethod
	def getAllHeros(self):
		hero = HeroModel()
		ret= hero.getAllHeros()
		obj= HeroVO()
		ret= makeVo(ret, obj)
		return ret
	'''
	@classmethod
	def getAllSystemAndUserHeros(self, params):
		uuid = params[0]
		hero = HeroModel()
		ret = hero.getAllSystemAndUserHeros(uuid)
		'''
		data=[]
		for r in ret:
			data.append({'jobCards': r.get('jobCards'), 'job': r.get('job'), 'type': r.get('type'), '_id': r.get('_id'), 'aliasName': r.get('aliasName')})
		'''
		obj= HeroVO()
		ret= makeVo(ret, obj)
		return ret

	@classmethod
	def getSystemOrUserHerosById(self, params):
		uuid= params[0]
		id= params[1]

		if uuid== None or id== None:
			return -1

		hero = HeroModel()
		ret= hero.getSystemOrUserHerosById(uuid, id)
		#data={'jobCards': ret.get('jobCards'), 'job': ret.get('job'), 'type': ret.get('type'), '_id': ret.get('_id'), 'aliasName': ret.get('aliasName')}


		obj= HeroVO()
		ret= makeVo(ret, obj)
		return ret

	@classmethod
	def updateUserHeros(self, params):
		uuid, id, cardIds= params[0], int(params[1]), params[2]
		if uuid== None or id== None or cardIds== None:
			return -1

		hero = HeroModel()
		ret= hero.updateUserHeros(id, cardIds)
		print params
		print ret
		if isinstance(ret, dict)== True:
			params= [uuid, id]
			return self.getSystemOrUserHerosById(params)	
		else:
			return -2
		
	@classmethod
	def deleteUserHeros(cls, params):
		'''
		删除用户套牌
		@param params:拥有两个元素的list,第一个下标代表用户编号，第二个下标代表用户的套牌编号
		@return: 1代表删除成功，其他代表删除失败
			-1：参数不为list
			-2：参数长度小于2
			-3：参数 list对应元素value不合法
		@author: tanming
		'''
		if not isinstance(params, list):
			return -1;
		
		if len(params) < 2:
			return -2;
		
		userId, uCardId = int(params[0]), int(params[1])
		if not userId or not uCardId:
			return -3
		
		hero = HeroModel()
		ret = hero.deleteUserHeros(userId, uCardId)
		
		if isinstance(ret, dict) == True:
			return 1
		
		return -4;

	@classmethod
	#def createUserHeros(self, uuid, job, name, cardIds):
	def createUserHeros(self, params):
		uuid, job, name, cardIds= params[0], params[1], params[2], params[3]
		if uuid== None or job== None or name== None or cardIds== None:
			return -1
		
		#if(cardIds.find(',')<0):
			#return -2

		name= name.strip()
		#ids= cardIds.split(',')
		hero = HeroModel()
		ret= hero.createUserHeros(uuid, job, name, cardIds)
		if isinstance(ret, int)== True:
			params= [uuid, ret]
			return self.getSystemOrUserHerosById(params)	
		else:
			return -2
		