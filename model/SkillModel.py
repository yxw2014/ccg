# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from pprint import pprint
from errors import err
from config import *
from const import *
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.FightModel import FightModel
from model.EffectModel import EffectModel
from pymongo.errors import AutoReconnect
						
class SkillModel(BaseModel): 
	def __init__(self): 
		super(SkillModel, self).__init__()	
		
	@classmethod	
	def getSkillById(self, _id):
		if(_id== None):      
			return None
		
		try:
			data= self.mongodb['hs_skill'].find_one({"_id": _id})		
			return  data
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")
			
	@classmethod
	def getSkillByIds(self, ids):
		if isinstance(ids, str)== False:
			return []
		ids= ids.split(',')
		for index, val in enumerate(ids):
			ids[index]= int(val)
			 
		ret= []
		try:
			for item in self.mongodb['hs_skill'].find({"_id":{'$in':ids}}):
				ret.append(item)
		except AutoReconnect:
			self.log.error("mongodb error, AutoReconnect!")

		return ret
	
	@classmethod	
	def parseEffects(self, room, pos, uniqid, skills):
		if isinstance(room, dict)== False or isinstance(skills, list)== False or uniqid== None or (pos!=1 and pos!= 2):
			return []

		ret= []
		for skill in skills:
			effect= self.parseEffect(room, pos, uniqid, skill)
			ret.append(effect)
		return ret
			
	
	@classmethod	
	def parseEffect(self, room, pos, uniqid, skill):
		if isinstance(room, dict)== False or isinstance(skill, dict)== False or uniqid== None or (pos!=1 and pos!= 2):
			return {}		
		
		script= skill.get('script')
		if script== None:
			return {}
		try:
			effect= json.loads(script)	
		except:	
			self.log.error(str(script))	
	
		obj= {}
		#技能id
		obj['skill_id']= skill.get('_id')
		
		obj['skill_name']= skill.get('name')
		#触发条件	
		obj['trigger']= effect['trigger']
		obj['trigger_condition']= effect['trigger']['triggerType']		
		#触发者
		obj['object']= uniqid 
		#触发目标A
		obj['targetA']= effect['targetA']
		#触发目标B
		obj['targetB']= effect.get('targetB')
		#效果类型
		obj['type']= effect['effectType']
		#效果数值
		obj['value']= effect.get('effectValue')
		#效果持续时间
		obj['continuous']= effect['continuous']		
		#经历的回合
		#obj['turn_count']= 0

		return obj
	
	'''
	@classmethod	
	def parseSkillTarget(self, room, pos, uniqid, target):
		if isinstance(room, dict)== False or isinstance(target, dict)== False or uniqid== None or (pos!=1 and pos!= 2):
			return []
		ret= []
		
		range= target.get('range')
		attribute= target.get('attribute')		
		attribute_condition= target.get('attributeCondition')
		pointer= target.get('pointer')
		
		return ret
	'''

	@classmethod	
	def triggerEffects(self, room, effects, pos, uniqids= []):
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False

		if isinstance(effects, list)== True:
			for effect in effects:
				self.doEffect(room, pos, effect, uniqids)			
		else:
			return False
		
		return False	
	
	
	@classmethod
	def doEffect(self, room, pos, effect, uniqids= []):
		if isinstance(room, dict)== False or isinstance(effect, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		print '----------------doEffect', pos, effect			
		
		#立即触发，比如冲锋,嘲讽
		if effect['type']== EFFECT_TYPE_CHARGE:
			return 	EffectModel.doEffectDash(room, pos, effect, uniqids)
		elif effect['type']== EFFECT_TYPE_TAUNT:
			return 	EffectModel.doEffectTaunt(room, pos, effect, uniqids)	
		elif effect['type']== EFFECT_TYPE_SUMMON:
			return 	EffectModel.doEffectSummon(room, pos, effect, uniqids)
		elif effect['type']== EFFECT_TYPE_DAMAGE:
			return 	EffectModel.doEffectAddDamage(room, pos, effect, uniqids)	
		elif effect['type'] in [EFFECT_TYPE_HEAL, EFFECT_TYPE_ADDHP, EFFECT_TYPE_ADDMAXHP]:
			return 	EffectModel.doEffectHp(room, pos, effect, uniqids, effect['type'])
		elif effect['type']== EFFECT_TYPE_WINDFURY:
			return 	EffectModel.doEffectWindfury(room, pos, effect, uniqids)	
		elif effect['type']== EFFECT_TYPE_ARMOR:
			return 	EffectModel.doEffectArmor(room, pos, effect, uniqids)	
		elif effect['type']== EFFECT_TYPE_STUN:
			return 	EffectModel.doEffectStun(room, pos, effect, uniqids)
		elif effect['type']== EFFECT_TYPE_ADDATTK:
			return 	EffectModel.doEffectAddAtk(room, pos, effect, uniqids)
		elif effect['type']== EFFECT_TYPE_ADDCRYSTAL:
			return 	EffectModel.doEffectAddCrystal(room, pos, effect, uniqids)	
			
		else:
			return True
			
		return True

	@classmethod	
	def triggerStackEffects(self, room,  pos, trigger_condition= 'now', uniqids= []):
		if isinstance(room, dict)== False or trigger_condition== None or (pos!=1 and pos!= 2):
			return False
		
		trigger_condition= str(trigger_condition)
		if pos== 1:
			effect_stack=  room['effect1']
		elif pos==2:
			effect_stack=  room['effect2']
		
		effects= effect_stack.get(trigger_condition)
		
		print '----------------triggerStackEffects', pos, effects	
		
		if isinstance(effects, list)== True:
			if len(effects)> 0: 
				for e in effects:
					return self.doEffect(room,  pos, e)
			else:
				return True
		else:
			return True
		
		return True
	
	'''
	@classmethod	
	def getEffectsByTriggerCondition(self, effects, condition):
		if isinstance(effects, list)== False or isinstance(condition, str)== False:
			return []
		
		ret= []
		
		for index, val in enumerate(effects):
			#trigger_condition= int(val.get('trigger_condition'))
			trigger_condition= str(val.get('trigger_condition'))
			if(trigger_condition== condition):
				ret.append(val)
		return ret
	'''
	
	@classmethod
	def addRoomEffectToStack(self, stack, effects):
		if isinstance(stack, dict)== True and isinstance(effects, list)== True:	
			for index, val in enumerate(effects):
				trigger_condition= str(val.get('trigger_condition'))
				if stack.get(trigger_condition)== None:			
					stack[trigger_condition]= []
				stack[trigger_condition].append(val)
			return True		
		else:			
			return False
	
	
	
	
