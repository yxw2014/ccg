# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from errors import err
from config import config
from  const import *
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.HeroModel import HeroModel
from model.RoomModel import RoomModel
from pymongo.errors import AutoReconnect
						
class FightModel(BaseModel): 
	def __init__(self): 
		super(FightModel, self).__init__()
	

	@classmethod
	def checkGameOver(self, room):
		if isinstance(room, dict)== False:
			return False
		time= room.get('result')
		if time>0:
			return True
		
		return False

	@classmethod
	def checkWeapon(self, room, pos, durability):
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		#durability= durability- 1
		#durability= max(0, durability)
		if durability== None:
			return False
		if int(durability)== 0:
			if pos== 1:
				room['weapon1']= {}
				room['cardPlay1'][0]['atk']= 0
			else:
				room['weapon2']= {}
				room['cardPlay2'][0]['atk']= 0
		
		return True		
	
	@classmethod
	def checkAttackerAtkTime(self, card):
		if isinstance(card, dict)== False:
			return False
		time= card.get('aTime')
		if time== None or int(time)< 1:
			return False
		
		return True	
		
	'''	
	@classmethod
	def checkHeroSkillAtkTime(self, card):
		if isinstance(card, dict)== False:
			return False
		time= card.get('aTime')
		if time== None or int(time)< 1:
			return False
		
		return True
	'''	
	
	'''
	@classmethod
	def checkAttackerStatusFrozen(self, room,  pos, target):
		if isinstance(room, dict)== False or isinstance(target, int)== False or (pos!=1 and pos!= 2):
			return False
		if pos== 1:
			effect= room['effect1'].get('now')
			k= 'cardPlay1'
			
		elif pos==2:
			effect= room['effect2'].get('now')
			k= 'cardPlay2'
			
		p, v= RoomModel.getRoomCardById(room[k], target)
		if v== None:
			return False
		
		if v.get('status') & STATUS_FROZEN== 0:
			return False
		
		if effect== None:
			return False
		
		return True
	'''
		
	@classmethod
	def checkAttackerStatusStun(self, room,  pos, target):
		if isinstance(room, dict)== False or isinstance(target, int)== False or (pos!=1 and pos!= 2):
			return False
		if pos== 1:
			#effect= room['effect1'].get('now')
			k= 'cardPlay1'
			
		elif pos==2:
			#effect= room['effect2'].get('now')
			k= 'cardPlay2'
			
		p, v= RoomModel.getRoomCardById(room[k], target)
		if v== None:
			return False
		
		if v.get('status') & STATUS_FROZEN== 0:
			return False
		
		return True		
		
		 	
	'''
	判断嘲讽状态
	'''		
	@classmethod
	def checkTargetStatusTaunt(self, room,  pos, target): 	
		if isinstance(room, dict)== False or isinstance(target, int)== False or (pos!=1 and pos!= 2):
			return False
		#对手，所以是反的
		if pos== 1:
			cards= room['cardPlay2']
		elif pos== 2:
			cards= room['cardPlay1']
			
		ret= []	
		for k, c in enumerate(cards):
			if c.get('status')== STATUS_TAUNT and c.get('die')== 0 :
				ret.append(c.get('uniqid'))
		print '//////checkTargetStatusTaunt', ret, target, pos		
		if len(ret)>0 and ret.count(target)== 0:
			return True
				
		return False
	
	@classmethod
	def checkPlayCardsLimit(self, room,  pos): 	
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		if pos== 1:
			cards= room['cardPlay1']
		elif pos== 2:
			cards= room['cardPlay2']
			
		count=0
		for k, c in enumerate(cards):
			if c.get('type')!= HERO_HERO and c.get('die')== 0:
				count= count+ 1
				
		if count> int(config['GAME']['playCardsLimit']):
			return True
				
		return False
	
	@classmethod
	def checkHandCardsLimit(self, room,  pos): 	
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		if pos== 1:
			cards= room['cardHand1']
		elif pos== 2:
			cards= room['cardHand2']
			
		count=0
		for k, c in enumerate(cards):
			if c.get('type')!= HERO_HEROSKILL and c.get('die')== 0:
				count= count+ 1
				
		if count> int(config['GAME']['playCardsLimit']):
			return True
				
		return False
	
	@classmethod
	def checkAllCardsLeft(self, room,  pos): 	
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		if pos== 1:
			cards= room['cardAll1']
		elif pos== 2:
			cards= room['cardAll2']
			
					
		if len(cards)== 0:
			return True
				
		return False
	
	@classmethod
	def doCheckAllCardsLeft(self, room,  pos): 	
		'''
		查看牌库中是否还有牌剩余，如果没有了，记录无牌回合次数+1
		add summary by tm at 2014-01-27
		'''
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		
		if pos== 1:		
			if self.checkAllCardsLeft(room,  pos)== True:		
				room['noCardTurn1']= room['noCardTurn1']+ 1 
				noCardTurn= room['noCardTurn1']
				room['crystal1']= room['crystal1']- noCardTurn
				room['crystal1']= max(0, room['crystal1'])
				return True
		elif pos== 2:
			if self.checkAllCardsLeft(room,  pos)== True:		
				room['noCardTurn2']= room['noCardTurn2']+ 1 
				noCardTurn= room['noCardTurn2']
				room['crystal2']= room['crystal2']- noCardTurn
				room['crystal2']= max(0, room['crystal2'])			
				return True
				
		return False
	
	@classmethod
	def doDamage(self, card,  damage):
		if isinstance(card, dict)== False or isinstance(damage, int)== False:
			return False
		
		if damage< 0:
			return False
		
		#if card['type']== HERO_HERO:
		if card['armor']> damage:
			card['armor']= card['armor']- damage
		else:				
			card['hp']= card['hp']- (damage- card['armor'])
			card['armor']= 0
			card['hp']= max(0, card['hp'])
		#else:
			#card['hp']= card['hp']- damage
			#card['hp']= max(0, card['hp'])
			
		return True
			
		
		
		
		 

			
			



