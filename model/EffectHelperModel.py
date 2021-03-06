# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
import copy
from pprint import pprint
from errors import err
from const import *
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.RoomModel import RoomModel
from model.CardModel import CardModel
from model.FightModel import FightModel
from pymongo.errors import AutoReconnect
						
class EffectHelperModel(BaseModel): 
	def __init__(self): 
		super(EffectHelperModel, self).__init__()		
	'''
	@classmethod
	def __getEffectPointerTarget(self, cards, pointer, uniqids, object):
		if isinstance(cards, list)== False or isinstance(pointer, dict)== False or isinstance(uniqids, list)== False:
			return []
		all_uniqids= RoomModel.getRoomCardAllUniqid(cards)
		uniqids= [int(val) for val in uniqids]	
	
		pointer_type= pointer.get('pointerType')
		pointer_value= pointer.get('pointerValue')
		#fix bug
		if pointer_type== None:
			return []
		if str(pointer_type)=='' or (pointer_value!= None and pointer_value<= 0):
			self.log.error('doEffectAddAtk, Configuration error')
			return []
			
		if pointer_type== 'playerPickX':
			print 'here', uniqids, all_uniqids
			tmp= [val for val in uniqids if val in all_uniqids]
			if len(tmp)!= len(uniqids):
				return []	
		elif pointer_type== 'single':
			if len(uniqids)>1:
				return []
			if all_uniqids.count(uniqids[0])== 0:
				return []						
		elif pointer_type== 'all':
			#tmp= [val for val in uniqids if val in all_uniqids]			
			uniqids= all_uniqids
		elif pointer_type== 'randomX':
			pointer_value= int(pointer_value)
			count= min(len(all_uniqids), pointer_value)
			count= max(1, pointer_value)
			if count>= len(all_uniqids):
				uniqids= all_uniqids
			else:
				uniqids= random.sample(all_uniqids, count)
		elif pointer_type== 'others':
			uniqids  = [val for val in all_uniqids if val != object]	
		else:
			return []
		return uniqids
	
	@classmethod
	def getEffectTarget(self, room, pos, effect, uniqids= []):
		if isinstance(room, dict)== False or isinstance(effect, dict)== False or (pos!=1 and pos!= 2):
			return []
		
		range= effect['targetA'].get('range')
		pointer= effect['targetA'].get('pointer')
		attribute= effect['targetA'].get('attribute')
		object= effect['object']
		
		print pointer, range, object, uniqids
		
		if range.get('thisCard')== 1:
			return [object]
		if pointer== None:
			pointer= {'pointerType':'all'}
		elif isinstance(pointer, dict)== True:
			field= range.get('field')
			role= range.get('role')
			camp= range.get('camp')
			pointer_type= pointer.get('pointerType')
			pointer_value= pointer.get('pointerValue')
			
			if role== None:
				role= []
			if isinstance(role, list)== False:
				role= [role]
			
			print type(role), HERO_HERO, camp
			
			if pos== 1:
				if camp== 'me' and len(role)==1 and role[0]== HERO_HERO:
					return [room['cardPlay1'][0]['uniqid']]
					
				if field== 'battleField' or field== None:
					if camp== None or camp== 'all':
						cards= []
						cards.extend(room['cardPlay1'])
						cards.extend(room['cardPlay2'])
					elif camp== 'me':
						k= 'cardPlay1'
						cards= copy.deepcopy(room[k]) 
					elif camp== 'enemy':	
						k= 'cardPlay2'
						cards= copy.deepcopy(room[k]) 
				else:
					return []		
			else:
				if camp== 'me' and len(role)==1 and role[0]== HERO_HERO:
					return [room['cardPlay2'][0]['uniqid']]
				
				if field== 'battleField' or field== None:
					if camp== None or camp== 'all':
						cards= []
						cards.extend(room['cardPlay1'])
						cards.extend(room['cardPlay2'])
					elif camp== 'me':
						k= 'cardPlay2'
						cards= copy.deepcopy(room[k]) 
					elif camp== 'enemy':	
						k= 'cardPlay1'
						cards= copy.deepcopy(room[k])	
				else:
					return []
				
			print range, pointer, camp	
			
			cards= [val for val in cards if role.count(val.get('type'))> 0]
			print '__getEffectPointerTarget', cards, role
			cards= self.__doEffectTargetAttributeFilter(room, pos, effect, cards, attribute)
			
			return self.__getEffectPointerTarget(cards, pointer, uniqids, object)
			
		return []
	
	@classmethod
	def __doEffectTargetAttributeFilter(self, room, pos, effect, cards, attribute):
		if attribute== None or isinstance(cards, list)== False:
			return cards
		
		#受过伤的
		if attribute== "injured":
			cards= [val for val in cards if (val.get('maxHp')> 0 and val.get('maxHp')> val.get('hp'))]	
		else:
			pass
		return cards
	'''
			
	@classmethod
	def getEffectValue(self, room, pos, effect, uniqids= []):
		'''
		效果值分配处理
		modified by tm at 2014-01-28
		1.add summary
		2.整理代码逻辑，支持nForRandom类型
		@return: 返回以uniqid为key，具体分配到的值为value的dict
		'''
		if isinstance(room, dict)== False or isinstance(effect, dict)== False or (pos!=1 and pos!= 2):
			return {}
		
		values = effect.get('value', {})
		if not values:
			return {}
		
		nvalue = int(values.get('value', 0))
		return {
			'n' : (lambda x: {val:nvalue for val in uniqids})(uniqids),
			'nForRandom' : self.__effectValueNForRandom(nvalue, uniqids),
		}[values.get('valueType')]
		
		# return value, tp
	
	@classmethod
	def __effectValueNForRandom(cls, nvalue, uniqids):
		'''
		值随机分配到各对象上
		@author: tm 2014-01-28
		'''
		returnDict = {}
		for i in xrange(nvalue):
			# 随机从list中取出一个元素
			uniqid = random.choice(uniqids)
			returnDict[uniqid] = returnDict.has_key(uniqid) and returnDict[uniqid] + 1 or 1
		
		return returnDict
	
	@classmethod
	def getEffectContinuous(self, room, pos, effect, uniqids= []):
		if isinstance(room, dict)== False or isinstance(effect, dict)== False or (pos!=1 and pos!= 2):
			return 0
		
		continuous= effect.get('continuous')
		if isinstance(continuous, dict)== False:
			return False
		continuousType= continuous.get('continuous')
		continuousValue= continuous.get('continuousValue')
		
		if continuousType== "cardExistence":
			value= -2
		elif continuousType== "once":
			value= -1
			return True
		elif continuousType== "xTurnsFromNext":
			value= int(continuousValue)+1
		elif continuousType== "xTurnsFromNow":
			value= int(continuousValue)
		elif continuousType== "thisMatchEnd":
			value= -3
		elif continuousType== "thisTurnEnd":
			value= 1
		else:
			value= 0		
			
		return value	
	
	
	@classmethod
	def getEffectPointer(self, pos, pointer, targetRange):
		'''
		获取房间内受effect影响的卡牌组（己方，对方，手牌，随从）
		modified by tm 2013-01-27
		1.add commet
		2.重组逻辑
		@return: 受影响的key组成的list
		'''
		if isinstance(targetRange, dict) == False or (pos!=1 and pos!= 2):
			return []
		
		returnList = []
		
		if targetRange.get('thisCard') == 1:
			if pos == 1:
				returnList.append('cardPlay1')
			else:
				returnList.append('cardPlay2')
		else:
			field = targetRange.get('field', 'battleField')
			camp = targetRange.get('camp', 'all')
			card_type_key = (field == 'battleField' and 'cardPlay' or 'cardHand')
			#k = card_type_key + '1'
			#k2 = card_type_key + '2'
				
			if pos == 1:
				returnList = {
					'me' : [card_type_key + '1'],
					'enemy' : [card_type_key + '2'],
					'all' : [card_type_key + '1', card_type_key + '2']
				}[camp]
			else:
				returnList = {
					'me' : [card_type_key + '2'],
					'enemy' : [card_type_key + '1'],
					'all' : [card_type_key + '1', card_type_key + '2']
				}[camp]
				
		return returnList
	
	@classmethod
	def getEffectTurnRedisKey(self, room, uniqid, turn, type= ''):
		if type== EFFECT_TYPE_STUN:
			key= REDIS_KEY_EFFECT_STUN_TURN
		elif type== EFFECT_TYPE_TAUNT:
			key= REDIS_KEY_EFFECT_TAUNT_TURN
		elif type== EFFECT_TYPE_WINDFURY:
			key= REDIS_KEY_EFFECT_WINDFURY_TURN
		else:
			return None
		return key
		
	@classmethod
	def setEffectTurn(self, room, uniqid, turn, type= ''):
		if isinstance(room, dict)== False or isinstance(uniqid, int)== False or isinstance(turn, int)== False or type== '':
			return False
		
		room_id= room['roomId']
		key= self.getEffectTurnRedisKey(room, uniqid, turn, type)
		if key== None:
			return False
		key= key  % (room_id)
		
		turn= min(20, turn)
		turn= max(0, turn)
		self.redis.zadd(key, uniqid, turn)	
		if self.redis.ttl(key)== None:
			self.redis.expire(key, 3600)
		return True
	
	@classmethod
	def checkEffectTurn(self, room, uniqid, type= ''):
		if isinstance(room, dict)== False or isinstance(uniqid, int)== False or type== '':
			return False
		
		room_id= room['roomId']
		key= self.getEffectTurnRedisKey(room, uniqid, turn, type)
		if key== None:
			return False
		key= key  % (room_id)

		turn= self.redis.zscore(key, uniqid)	
		if turn!=0 and turn!= None:
			return True
		else:
			return False

	@classmethod
	def updateEffectTurn(self, room, pos, uniqid, type= ''):
		if isinstance(room, dict)== False or isinstance(uniqid, int)== False or type== '' or (pos!=1 and pos!= 2):
			return False
		room_id= room['roomId']		
		key= self.getEffectTurnRedisKey(room, uniqid, turn, type)
		if key== None:
			return False
		key= key  % (room_id)
		
		turn= min(20, turn)
		turn= max(0, turn)
		
		turn= self.redis.zscore(key, uniqid)
		if turn== None:
			return False
		elif turn== 1 or turn== 0:
			self.redis.zrem(key, uniqid)
			self.removeEffectTurn(room, pos, uniqid, 0, type)
			return True
		else:
			new_turn= int(self.redis.zincrby(key, uniqid, -1))
			return True	
			 
		
	@classmethod
	def removeEffectTurn(self, room, pos, uniqid, type= ''):		
		if isinstance(room, dict)== False or isinstance(uniqid, int)== False or type== '' or (pos!=1 and pos!= 2):
			return False
		
		if pos== 1:
			k= 'cardPlay1'	 
		else:
			k= 'cardPlay2'	 
		
		if type== EFFECT_TYPE_STUN:
			status= STATUS_STUN
		elif type== EFFECT_TYPE_TAUNT:
			status= STATUS_TAUNT
		elif type== EFFECT_TYPE_WINDFURY:
			status= STATUS_WINDFURY
		else:
			return False
		
		p, v= RoomModel.getRoomCardById(room[k], uniqid)
		if p== None:
			return False
		
		room[k][p]['status']= room[k][p]['status'] ^ status
		
		return True	
	
	@classmethod
	def turnEndEffectCallBack(self, room, pos):		
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		keys= [REDIS_KEY_EFFECT_WINDFURY_TURN, REDIS_KEY_EFFECT_TAUNT_TURN, REDIS_KEY_EFFECT_STUN_TURN]
		types= [STATUS_WINDFURY, STATUS_TAUNT, STATUS_STUN]
		
		def doEffectCallBack(key, tp):
			list= self.redis.zrange(key, 0, -1, withscores=False, score_cast_func=int)
			for uniqid in list:
				uniqid= int(uniqid)
				self.updateEffectTurn(room, pos, uniqid, tp)
		
		map(doEffectCallBack, keys, types)
		
	@classmethod
	def getEffectTarget(cls, room, pos, effect, uniqids=[]):
		'''
		获取要作用的目标
		modified by tm at 2014-01-22
		@param room: 房间信息
		@param pos: 请求接口的角色所处房间位置 (1：代表上方，2代表下方 )
		@param effect: 效果配置信息 
		@param uniqids: 用户选择效果作用的卡uniqid
		@return: 返回符合规则的卡信息list
		'''
		if isinstance(room, dict)==False or isinstance(effect, dict)==False or (pos!=1 and pos!=2):
			return []
		
		targetRange = effect['targetA'].get('range')
		pointer = effect['targetA'].get('pointer', {})
		targetObject = effect['object']
		
		if targetRange.get('thisCard') == 1:
			return [int(targetObject)]
		
		returnCards = []
		cardIds = targetRange.get('cardID')
		# 如果是指定卡id的类型
		if cardIds:
			enemyPos = (pos == 1 and 2 or 1)
			returnCards.extend(room['cardPlay'+str(pos)])
			returnCards.extend(room['cardHand'+str(enemyPos)])
			for card in returnCards:
				if card['_id'] in cardIds:
					returnCards.append(card['uniqid'])
					
			return cls.__effectTargetPointerFilter(returnCards, pointer, uniqids, targetObject)
		
		tgCamp = targetRange.get('camp', 'all')
		tgField = targetRange.get('field', 'battleField')
		tgRole = targetRange.get('role', '')
		tgClass = targetRange.get('class', '')
		tgRace = targetRange.get('race', '')
		
		methodDict = {
			'hands' : cls.__effectTargetRangeFilter(room, pos, 'cardHand', tgCamp, tgRole, tgClass, tgRace),
			'battleField' : cls.__effectTargetRangeFilter(room, pos, 'cardPlay', tgCamp, tgRole, tgClass, tgRace),
		}
		returnCards = methodDict.get(tgField, {})
		
		return cls.__effectTargetPointerFilter(returnCards, pointer, uniqids, targetObject)
	
	@classmethod
	def __effectTargetPointerFilter(cls, cards, pointer, uniqids, targetObject):
		'''
		获取要作用的范围群体内的目标群体
		@author: tm
		@param cards: 符合要求的卡集合字典 
		@param pointer: 配置 
		@param targetObject: 本卡uniqueid
		@param uniqids: 用户选择的卡  
		@return: 返回符合规则的卡片列表
		'''
		if isinstance(cards, dict) == False or isinstance(pointer, dict) == False or isinstance(uniqids, list) == False:
			return []
		
		all_uniqids = [int(val) for val in cards.keys()]
	
		pointer_type = pointer.get('pointerType', '')
		pointer_value = pointer.get('pointerValue', 0)
		if not pointer or not pointer_type:
			return all_uniqids
		
		# 因为客户端选择对象后传过来的对象uniqid是string类型的，所以要进行转化
		uniqids = [int(val) for val in uniqids]
		methodDict = {
				'playerPickX': (lambda x, y: [] if x < len(y) else y)(int(pointer_value), uniqids),
				'all': all_uniqids,
				'randomX': (lambda x, y: y if x >= len(y) else random.sample(y, x))(int(pointer_value), all_uniqids),
				'others': [val for val in all_uniqids if val != targetObject],
				'adjacent': cls.__pointerAdjacentFilter(cards, targetObject)
		}
		
		return methodDict.get(pointer_type, [])
		
	@classmethod
	def __effectTargetRangeFilter(cls, room, pos, tgFiledKey, tgCamp, tgRole, tgClass, tgRace):
		'''
		根据range范围来过滤目标卡牌
		@author: tm 2014-01-22
		@param room: 房间信息
		@param pos: 请求接口的角色所处房间位置 (1：代表上方，2代表下方 )
		@param tgFiledKey: 对应的目标牌所处位置的key(cardPlay or cardHand)
		其他参数对应range里的各个key的值
		@return: 返回符合要求的卡的列表
		'''
		targetCards = []
		originCards = {}
		returnCards = {}
		
		enemyPos = (pos == 1 and 2 or 1)
		if not tgCamp or tgCamp == 'all':
			targetCards.extend(room.get(tgFiledKey+str(pos), []))
			targetCards.extend(room.get(tgFiledKey+str(enemyPos), []))
			originCards = dict(room.get('cardOrigin'+str(pos), {}), **(room.get('cardOrigin'+str(enemyPos), {})))
		else:
			targetCards = copy.deepcopy(tgCamp == 'me' and room.get(tgFiledKey+str(pos), []) or room.get(tgFiledKey+str(enemyPos), []))
			originCards = copy.deepcopy(tgCamp == 'me' and room.get('cardOrigin'+str(pos), {}) or room.get('cardOrigin'+str(enemyPos), {}))
			
		for card in targetCards:
			oriCard = originCards.get(str(card['uniqid']), {})
			if not oriCard: # 原始卡不存在
				cls.log.error('the card with uniqid:<'+str(card['uniqid'])+'> is not exist in originCards')
				return {}
				
			if tgRole:
				oType = oriCard.get('type', '')
				if not oType or oType not in tgRole:
					# targetCards.remove(card)
					continue
			if tgClass:
				oJob = oriCard.get('job', '')
				if not oJob or oJob not in tgClass:
					# targetCards.remove(card)
					continue
			if tgRace:
				oRace = oriCard.get('race', '')
				if not oRace or oRace not in tgRace:
					# targetCards.remove(card)
					continue
			
			# 存储locaX,用于做pointer的位置判断
			returnCards[card['uniqid']] = dict(oriCard, **{'locaX':card.get('locaX', 0)})
		
		return returnCards
		
	@classmethod
	def __pointerAdjacentFilter(cls, cards, targetObject):
		'''
		获取邻近随从
		@author: tm
		@param cards: 符合要求的卡集合字典 
		@param targetObject: 本卡uniquid
		@return: 返回符合规则的卡片列表
		'''
		if not cards.has_key(targetObject):
			return []
		localX = cards[targetObject].get('localX', 0)
		if not localX <= 0:
			return []
		leftX, rightX = localX - 1, localX + 1
		returnUniqids = []
		for k, card in cards.items():
			cardX = card.get('localX', 0)
			if (leftX > 0 and cardX == leftX) or cardX == rightX:
				returnUniqids.append(card.get('uniqid'))
				
		return returnUniqids
	
	@classmethod
	def __effectTargetAttributeFilter(cls, cards, attribute=''):
		'''
		根据attribute来过滤目标卡牌
		@author: tanming 2014-01-23
		'''
		if not attribute or not isinstance(cards, list):
			return cards
		
		#受过伤的
		if attribute == "injured":
			cards = [val for val in cards if (val.get('maxHp') > 0 and val.get('maxHp') > val.get('hp'))]	
		else:
			pass
		return cards
	
	
	