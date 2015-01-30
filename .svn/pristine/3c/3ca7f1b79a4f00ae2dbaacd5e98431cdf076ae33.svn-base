# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from pprint import pprint
from errors import err
from  const import *
from config import *
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.RoomModel import RoomModel
from model.CardModel import CardModel
from model.FightModel import FightModel
from model.EffectHelperModel import EffectHelperModel

class EffectModel(BaseModel): 
	def __init__(self): 
		super(EffectModel, self).__init__()			
	
	@classmethod	
	def doEffectDash(self, room, pos, effect, uniqids = []):
		'''
		处理冲锋的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')	
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectDash--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
			
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqids:
					#uniqids.remove(uniqid)
					if card['aTime'] >= 1: # 如果此牌还没有攻击过
						if card['status'] & STATUS_WINDFURY: # 如果此牌有风怒状态
							card['aTime'] = 2
						else:
							card['aTime'] = 1
					card['status'] = card['status'] | STATUS_DASH
		
		return True
		
	@classmethod		
	def doEffectTaunt(self, room, pos, effect, uniqids = []):
		'''
		处理嘲讽的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range= effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')	
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectTaunt--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
			
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqids:
					#uniqids.remove(uniqid)
					card['status'] = card['status'] | STATUS_TAUNT
		
		return True
		
	@classmethod	
	def doEffectHp(self, room, pos, effect, uniqids = [], hp_type=EFFECT_TYPE_HEAL):
		'''
		处理回血的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')
		
		# 获取受到影响的卡uniqid列表
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectHealHp--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取值分配
		uniqid_values = EffectHelperModel.getEffectValue(room, pos, effect, uniqids)
		print uniqid_values
		if not uniqid_values:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
		
		uniqid_keys = uniqid_values.keys()
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqid_keys:
					if hp_type == EFFECT_TYPE_HEAL: # 回血（不能超过血上限）
						card['hp'] = min(card['hp'] + uniqid_values[uniqid], card['maxHp'])
					elif hp_type == EFFECT_TYPE_ADDHP: # 加血（血上限不变）
						card['hp'] = card['hp'] + uniqid_values[uniqid]
					elif hp_type == EFFECT_TYPE_ADDMAXHP: # 加血上限（也要加血）
						card['maxHp'] = card['maxHp'] + uniqid_values[uniqid]
						card['hp'] = card['hp'] + uniqid_values[uniqid]
					
		return True
	
	@classmethod		
	def doEffectArmor(self, room, pos, effect, uniqids = []):
		'''
		处理加护甲的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')	
		
		# 获取受到影响的卡uniqid列表
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectArmor--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取值分配
		uniqid_values = EffectHelperModel.getEffectValue(room, pos, effect, uniqids)
		print uniqid_values
		if not uniqid_values:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		print c_keys
		if not c_keys:
			self.log.error(str(effect))
			return False
		
		uniqid_keys = uniqid_values.keys()
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqid_keys:
					print uniqid
					#uniqids.remove(uniqid)
					card['armor'] = card['armor'] + uniqid_values[uniqid]
		
		return True
	
	@classmethod		
	def doEffectStun(self, room, pos, effect, uniqids= []):
		'''
		处理眩晕的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')	
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectStun--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
		
		continuous = EffectHelperModel.getEffectContinuous(room, pos, effect, uniqids)
		
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqids:
					#uniqids.remove(uniqid)
					card['status'] = card['status'] | STATUS_STUN
					if isinstance(continuous, int) == True:
						EffectHelperModel.setEffectTurn(room, uniqid, continuous, EFFECT_TYPE_STUN)
		
		return True
	

	@classmethod
	def doEffectWindfury(self, room, pos, effect, uniqids= []):
		'''
		处理风怒的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range= effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')	
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectWindfury--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
			
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqids:
					#uniqids.remove(uniqid)
					card['status'] = card['status'] | STATUS_WINDFURY
					
		return True

	@classmethod
	def doEffectAddDamage(self, room, pos, effect, uniqids= []):
		'''
		处理伤害的效果（造成伤害，如火球术）
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')
		field = target_range.get('field', 'battleField')
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectAddDamage--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取值分配
		uniqid_values = EffectHelperModel.getEffectValue(room, pos, effect, uniqids)
		print uniqid_values
		if not uniqid_values:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
					
		uniqid_keys = uniqid_values.keys()
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqid_keys:
					#uniqids.remove(uniqid)
					FightModel.doDamage(card, uniqid_values[uniqid])
					if field == 'battleField':
						RoomModel.checkCardDie(room, pos, card)
		
		return True
	
	@classmethod		
	def doEffectAddAtk(self, room, pos, effect, uniqids = []):
		'''
		处理增加攻击力的效果
		modified by tm at 2014-01-27
		1. add summary
		2. 重新整理代码逻辑
		'''
		if isinstance(room, dict)== False or isinstance(effect, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		target_range= effect['targetA'].get('range')
		pointer= effect['targetA'].get('pointer')	
		
		uniqids = EffectHelperModel.getEffectTarget(room, pos, effect, uniqids)
		print 'doEffectAddAtk--------------------------', uniqids
		if not uniqids:
			return False
		
		# 获取值分配
		uniqid_values = EffectHelperModel.getEffectValue(room, pos, effect, uniqids)
		print uniqid_values
		if not uniqid_values:
			return False
		
		# 获取受到effect影响的上卡牌组的key组成的list(cardPlay1,cardPlay2,cardHand1,cardHand2)
		c_keys = EffectHelperModel.getEffectPointer(pos, pointer, target_range)	
		if not c_keys:
			self.log.error(str(effect))
			return False
		
		uniqid_keys = uniqid_values.keys()
		for ck in c_keys:
			for card in room[ck]:
				uniqid = card.get('uniqid')
				if uniqid in uniqid_keys:
					#uniqids.remove(uniqid)
					card['atk'] = card['atk'] + uniqid_values[uniqid]
		
		return True
	
	@classmethod		
	def doEffectSummon(self, room, pos, effect, uniqids = []):
		'''
		处理召唤效果
		modified by tm at 2014-01-27
		1. add summary
		2. 召唤产生的牌入原始库
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		target_range = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer')
		uniqid = effect['object']
		
		if isinstance(pointer, dict)== True:
			pointer_type= pointer.get('pointerType')
			pointer_value= pointer.get('pointerValue')
		else:
			pointer_type= None
			pointer_value= None
						

		if pos== 1:
			locaX = RoomModel.getRoomPlayCardsMaxLocaX(room['cardPlay1'])
		else:
			locaX = RoomModel.getRoomPlayCardsMaxLocaX(room['cardPlay2'])		
		
		ids = target_range.get('cardID')
		if isinstance(ids, list)== False:
			ids= [ids]
			
		if ids== None:
			return False		
		
		if pointer_type== 'randomX':
			count= min(len(ids), pointer_value)
			count= max(1, pointer_value)
			ids= random.sample(ids, count)
		
		print 'doEffectSummon--------------------------', ids
		
		x= 0		
		for index, val in enumerate(ids):
			#ids[index]= int(val)
			x = x + 1	
			lx = locaX + x
			data = CardModel.getCardsById(int(val))
			if data == None:
				continue
			data['uniqid'] = uniqid = int(time.time()) + data['_id'] + random.randint(100000, 999999)
			format_data = RoomModel.getRoomCardCustomFormat(data)
				
			if pos == 1:
				room['cardOrigin1'][uniqid] = data
				format_data['locaX'] = lx
				format_data['locaY'] = 0
				room['cardPlay1'].append(format_data)
				
			else:
				room['cardOrigin2'][uniqid] = data
				format_data['locaX'] = lx
				format_data['locaY'] = 0
				room['cardPlay2'].append(format_data)		
		
				RoomModel.updatePlayCardsLocX(room, pos, lx, uniqid)
		
		return True	
	
	@classmethod		
	def doEffectAddCrystal(self, room, pos, effect, uniqids = []):
		'''
		处理水晶效果（加或减）
		modified by tm at 2014-01-27
		1. add summary
		2. 代码简单整理
		'''
		if isinstance(room, dict) == False or isinstance(effect, dict) == False or (pos!=1 and pos!= 2):
			return False
		
		# value, tp= EffectHelperModel.getEffectValue(room, pos, effect)
		value = int(effect.get('value', {}).get('value', 0))
		print 'doEffectSummon--------------------------', value
		if value < 1:
			return False

		if pos == 1:
			room['crystal1'] = room['crystal1'] + value
		else:
			room['crystal2'] = room['crystal2'] + value
		
		return True
