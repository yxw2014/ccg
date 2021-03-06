# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
import copy
from pprint import pprint
from errors import err
from  const import *
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.CardModel import CardModel
from model.HeroModel import HeroModel
#from model.FightModel import FightModel 
from pymongo.errors import AutoReconnect
						
class RoomModel(BaseModel): 
	def __init__(self): 
		super(RoomModel, self).__init__()	
		
	@classmethod	
	def getRoom(self, room_id):
		if int(room_id)<= 0:
			return None
		room_id= str(room_id)
		room= self.redis.hgetall('hs:room:info:'+ room_id)	
		#pprint(room)
		for k, v in room.items():
			if(k== 'cardOrigin1' and room['cardOrigin1']!={}):
				room['cardOrigin1']= json.loads(room['cardOrigin1'])			
		
			elif(k== 'cardOrigin2' and room['cardOrigin2']!={}):
				room['cardOrigin2']= json.loads(room['cardOrigin2'])
			
			elif(k== 'weapon1' and room['weapon1']!={}):
				room['weapon1']= json.loads(room['weapon1'])
				
			elif(k== 'weapon2' and room['weapon2']!={}):
				room['weapon2']= json.loads(room['weapon2'])

			elif(k== 'effect1' and room['effect1']!={}):
				room['effect1']= json.loads(room['effect1'])			
		
			elif(k== 'effect2' and room['effect2']!={}):
				room['effect2']= json.loads(room['effect2'])
				
			elif(k== 'cardAll1' and room['cardAll1']!=[]):	
				room['cardAll1']= json.loads(room['cardAll1'])
			
			elif(k== 'cardAll2' and room['cardAll2']!=[]):	
				room['cardAll2']= json.loads(room['cardAll2'])				
		
			elif(k== 'cardHand1' and room['cardHand1']!=[]):	
				room['cardHand1']= json.loads(room['cardHand1'])
				
			elif(k== 'cardHand2' and room['cardHand2']!=[]):
				room['cardHand2']= json.loads(room['cardHand2'])
				
			elif(k== 'cardPlay1' and room['cardPlay1']!=[]):
				room['cardPlay1']= json.loads(room['cardPlay1'])
				
			elif(k== 'cardPlay2' and room['cardPlay2']!=[]):
				room['cardPlay2']= json.loads(room['cardPlay2'])

			elif(k== 'heros' and room['heros']!=[]):
				room['heros']= json.loads(room['heros'])
			elif(k== 'pos1'):
				pass
			elif(k== 'pos2'):
				pass
			elif room[k]== []:
				pass
			else:
				#try:
				room[k]= int(v)
				#except:
				#pass					
			
		return room
	
	@classmethod	
	def setRoom(self, room_id, room):
		if int(room_id)<= 0:
			return False
		room_id= str(room_id)
		#print len(room['cardAll1']), len(room['cardAll2'])
		if(isinstance(room['cardOrigin1'], dict)== True):
			room['cardOrigin1']= json.dumps(room['cardOrigin1'])
		
		if(isinstance(room['cardOrigin2'], dict)== True):
			room['cardOrigin2']= json.dumps(room['cardOrigin2'])
			
		if(isinstance(room['weapon1'], dict)== True):
			room['weapon1']= json.dumps(room['weapon1'])
			
		if(isinstance(room['weapon2'], dict)== True):
			room['weapon2']= json.dumps(room['weapon2'])
			
		if(isinstance(room['effect1'], dict)== True):
			room['effect1']= json.dumps(room['effect1'])
		
		if(isinstance(room['effect2'], dict)== True):
			room['effect2']= json.dumps(room['effect2'])
			
			
		if(isinstance(room['cardAll1'], list)== True):
			room['cardAll1']= json.dumps(room['cardAll1'])

		
		if(isinstance(room['cardAll2'], list)== True):
			room['cardAll2']= json.dumps(room['cardAll2'])

			
		if(isinstance(room['cardHand1'], list)== True):
			room['cardHand1']= json.dumps(room['cardHand1'])

			
		if(isinstance(room['cardHand2'], list)== True):
			room['cardHand2']= json.dumps(room['cardHand2'])

			
		if(isinstance(room['cardPlay1'], list)== True):
			room['cardPlay1']= json.dumps(room['cardPlay1'])

			
		if(isinstance(room['cardPlay2'], list)== True):
			room['cardPlay2']= json.dumps(room['cardPlay2'])

		if(isinstance(room['heros'], list)== True):	
			room['heros']= json.dumps(room['heros'])

		
		self.redis.hmset('hs:room:info:'+ room_id, room)
		if self.redis.ttl('hs:room:info:'+ room_id)== None:
			self.redis.expire('hs:room:info:'+ room_id, 3600)
			
		return True	
	
	@classmethod	
	def getRoomCardAllUniqid(self, cards):
		if isinstance(cards, list)== False:
			return []
		ret= []
		for k, c in enumerate(cards):
			uniqid= c.get('uniqid')
			if uniqid!= None:
				ret.append(uniqid)
		return ret	
	
	'''
	use uniqid
	'''
	@classmethod	
	def getRoomCardPosById(self, cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, list)== False:
			return -1
		
		for k, c in enumerate(cards):
			if c.get('uniqid')== id and c.get('die')== 0:
				return k
		return -1
	

	@classmethod	
	def getRoomCardById(self, cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, list)== False:
			return None,None
		
		for k, c in enumerate(cards):
			if c.get('uniqid')== id and c.get('die')== 0:
				return k, c
		return None, None
	
	@classmethod	
	def delRoomCardById(self, cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, list)== False:
			return False
		
		for k, c in enumerate(cards):
			if c.get('uniqid')== id:
				cards.pop(k)
			
		return True


	@classmethod	
	def getRoomCardWithInfoById(self, cards, all_cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, list)== False or isinstance(all_cards, dict)== False:
			return None, None
			
		for k, c in enumerate(cards):
			if c.get('uniqid')== id and c.get('die')== 0:
				
				info= all_cards.get(str(id))
				if info== None:
					return None, None
				else:
					r= dict(c, **info)
					return k, r
		return None, None
	
	
	@classmethod	
	def getRoomOriginCardInfoById(self, cards, id):
		return self.getRoomCardInfoById(cards, id)	
	
	'''
	use room cardOrigin
	'''
	@classmethod	
	def getRoomCardInfoById(self, cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, dict)== False:
			return None
		id= str(id)
		ret= cards.get(str(id))
		
		return ret
	
	@classmethod	
	def getRoomCardAtkById(self, cards, id):
		if isinstance(id, int)== False or int(id)<= 0 or isinstance(cards, dict)== False:
			return None
		info= self.getRoomCardInfoById(cards, id)
		if info== None:
			return None
		else:
			return info.get('atk')				

	@classmethod		
	def getRoomFirstCards(self, room, pos): 
		if isinstance(pos, int)== False or int(pos)<= 0 or isinstance(room, dict)== False:
			return None
		
		hero= room.get('heros')
		if hero== None:
			return None
		if pos== 1:
			jobCards= hero[0]['jobCards']
		elif pos== 2:
			jobCards= hero[1]['jobCards']
		
		ret= {}	
		for k, v in enumerate(jobCards):
			#jobCards[k]= int(v)
			data= CardModel.getCardsById(int(v))
			if(data!= None):
				data['uniqid']= int(time.time())+ k + data['_id']+ random.randint(100000, 999999)
				#ret.append(data)
				ret[data['uniqid']]= data

		return ret	

	@classmethod
	def getRoomRandCards(self, data, num=1): 
		if(isinstance(data, list)== False) or num< 0:
			return None
		
		ret= []
		le= len(data)
		if num> le:
			return []
		
		for i in xrange(0, num):
			#le= len(data)
			#rand= random.randint(0, le-1)
			
			p= data.pop(i)
			ret.append(p)

		return ret
	
	@classmethod
	def getRoomCardResult(self, data): 	
		if isinstance(data, dict)== True:
			buf= {}
			buf['uniqid']= data.get('uniqid')
			buf['_id']= data.get('_id')
			return buf
		else:
			return {}	
		
	@classmethod
	def getRoomCardsResult(self, data): 
		ret= copy.deepcopy(data) 	
		
		data= [self.getRoomCardResult(val) for val in ret if (val.get('type')!= HERO_HEROSKILL)]	
			
		return data
		'''
		if isinstance(ret, list)== True:
			for index, val in enumerate(ret):
				if isinstance(val, dict)== False:
					continue	
				if val.get('type')== HERO_HEROSKILL:
					ret.pop(index)
					continue	
				ret[index]= self.getRoomCardResult(val)
			return ret	
		else:
			return []
		'''
		
	@classmethod
	def getRoomCardOppResult(self, data): 	
		if isinstance(data, dict)== True:
			buf= {}
			buf['uniqid']= data.get('uniqid')
			#buf['_id']= data.get('_id')
			return buf
		else:
			return {}	
		
	
		
	@classmethod
	def getRoomCardsOppResult(self, data): 	
		ret= copy.deepcopy(data) 
		data= [self.getRoomCardOppResult(val) for val in ret if (val.get('type')!= HERO_HEROSKILL)]	
			
		return data
	
		'''
		if isinstance(ret, list)== True:
			for index, val in enumerate(ret):
				if isinstance(val, dict)== False:
					continue	
				if val.get('type')== HERO_HEROSKILL:
					ret.pop(index)
					continue
				ret[index]= self.getRoomCardOppResult(val)
			return ret	
		else:
			return []
		'''	

	@classmethod
	def getRoomCardOppPlayResult(self, data): 	
		if isinstance(data, dict)== True:
			buf= {}
			buf['uniqid']= data.get('uniqid')
			buf['_id']= data.get('_id')
			buf['locaX']= data.get('locaX')
			buf['hp']= data.get('hp')
			buf['atk']= data.get('atk')
			#buf['locaY']= data.get('locaY')
			buf['status']= data.get('status')
			buf['type']= data.get('type')
			#buf['die']= data.get('die')
			#buf['aTime']= data.get('aTime')
			buf['armor']= data.get('armor')	
			'''
			if buf['type']== HERO_HERO:					
				if data.get('atk')== 0:
					buf['aTime']= 0	
				else:
					#todo check EFFECT_TYPE_WINDFURY
					if buf['status'] & STATUS_WINDFURY:
						buf['aTime']= 2
					else:
						buf['aTime']= 1
			'''
			if buf['hp']== 0:
				buf['aTime']= 0	
				
			if data.get('atk')== 0:
				buf['aTime']= 0	
			return buf
		else:
			return {}	
		
	@classmethod
	def updateRoomCardsHeroAtk(self, room, pos): 	
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False
		if pos== 1:
			k= 'cardPlay1'
		else:
			k= 'cardPlay2'
		if room[k][0]['status'] & STATUS_WINDFURY:
			room[k][0]['aTime']= 2
		else:
			room[k][0]['aTime']= 1
		
	@classmethod
	def getRoomCardsOppPlayResult(self, data): 	
		ret= copy.deepcopy(data) 
		data= [self.getRoomCardOppPlayResult(val) for val in ret if (val.get('die')== 0 or val.get('type')== HERO_HERO)]			
			
		return data

		
	@classmethod
	def getRoomCardPlayResult(self, data): 	
		if isinstance(data, dict)== True:
			buf= {}
			buf['uniqid']= data.get('uniqid')
			buf['_id']= data.get('_id')
			buf['locaX']= data.get('locaX')
			buf['hp']= data.get('hp')
			buf['atk']= data.get('atk')
			#buf['locaY']= data.get('locaY')
			buf['status']= data.get('status')
			buf['type']= data.get('type')
			buf['die']= data.get('die')
			buf['aTime']= data.get('aTime')	
			buf['armor']= data.get('armor')
				
			'''
			if buf['type']== HERO_HERO:				
				if data.get('atk')== 0:
					buf['aTime']= 0
				else:
					#todo check EFFECT_TYPE_WINDFURY
					if buf['status'] & STATUS_WINDFURY:
						buf['aTime']= 2
					else:
						buf['aTime']= 1	
			'''
						
			if buf['hp']== 0:
				buf['aTime']= 0	
				
			if data.get('atk')== 0:
				buf['aTime']= 0	
		
			return buf
		else:
			return {}	
		
	@classmethod
	def getRoomCardsPlayResult(self, data): 	
		ret= copy.deepcopy(data) 
		
		data= [self.getRoomCardPlayResult(val) for val in ret if (val.get('die')== 0 or val.get('type')== HERO_HERO)]	
			
		return data
	
		'''
		if isinstance(ret, list)== True:
			for index, val in enumerate(ret):
				if isinstance(val, dict)== False:
					ret.pop(index)
					continue
				#过滤英雄牌
				if(val.get('type')== HERO_HERO):
					pass
				#死亡
				if(val.get('die')!= 0):
					ret.pop(index)	
					continue			
				val= self.getRoomCardPlayResult(val)
			return ret	
		else:
			return []
		'''	
		
	@classmethod	
	def getRoomCardsWeaponResult(self, data): 	
		if isinstance(data, dict)== True:
			buf= {}
			buf['uniqid']= data.get('uniqid')
			buf['_id']= data.get('_id')
			buf['atk']= data.get('atk')
			buf['hp']= data.get('hp')			
			return buf
		else:
			return {}	
		
	@classmethod
	def getRoomCardsAll(self, data): 
		ret= []	
		if isinstance(data, dict)== True:
			for id, val in data.items(): 
				if isinstance(val, dict)== False:
					continue
				
				buf= self.getRoomCardCustomFormat(val)
			
				ret.append(buf)
			return ret	
		else:
			return []
	
	@classmethod
	def getRoomCardCustomFormat(self, card): 
		if isinstance(card, dict)== False:
			return None
		buf= {}
		buf['_id']= card.get('_id')	
		buf['uniqid']= card.get('uniqid')		
		buf['type']= card.get('type')				
		buf['hp']= card.get('hp')
		buf['maxHp']= card.get('hp')
		buf['atk']= card.get('atk')
		buf['armor']= 0		
		buf['cost']= card.get('cost')
		buf['skill']= []
				
		#buf['durability']= card.get('durabilityCount')
		'''
		if card.get('type')== HERO_WEAPON:
			buf['durability']= card.get('hp')
		else:
			buf['durability']= 0
		'''
		buf['status']= 0
		buf['die']= 0
		buf['aTime']= 0
		buf['skillId']= card.get('skillId')
		
		return buf

	'''
	@classmethod
	def updateRoomCardsPlayStatus(self, data): 		
		if isinstance(data, list)== True:
			for index, val in enumerate(data):
				if isinstance(val, dict)== False:
					continue	
				if(val.get('status')== 0):
					#修改疲劳状态
					val['status']= 1
	'''
				
	@classmethod
	def updateRoomCardsPlayAtk(self, data, weapon= None): 		
		if isinstance(data, list)== True:
			for index, val in enumerate(data):
				if isinstance(val, dict)== False:
					continue	
				if val.get('aTime')== 0 and val.get('hp')> 0 and val.get('type')!= HERO_HERO:
					#修改疲劳状态
					if val['status'] & STATUS_WINDFURY:
						val['aTime']= 2
					else:
						val['aTime']= 1
				#英雄
				if val.get('type')== HERO_HERO:
					if weapon!= None and weapon!= {}:
						#修改疲劳状态
						if val['status'] & STATUS_WINDFURY:
							val['aTime']= 2
						else:
							val['aTime']= 1
							
	@classmethod
	def updateRoomCardsPlaySelfAtk(self, data): 		
		if isinstance(data, list)== True:
			for index, val in enumerate(data):
				if isinstance(val, dict)== False:
					continue
				val['aTime']= 0
	
	
	@classmethod
	def updateRoomCardsSkillAtk(self, room, pos, num= 1): 
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2):
			return False		
		if pos== 1:			
			room['stime1']= num
		else:
			room['stime2']= num
		return True
					
	'''
	@classmethod
	def updateRoomCardsSkill(self, data, die= 0): 
				
		if isinstance(data, list)== True:
			for index, val in enumerate(data):					
				if(val.get('type')== HERO_HEROSKILL):
					#修改卡生死状态
					val['die']= die
	'''
									
	@classmethod
	def addRoomCardPlayAtk(self, data, uniqid, count= 1): 		
		if isinstance(data, list)== True:
			for index, val in enumerate(data):					
				if(val.get('uniqid')== uniqid):
					#修改疲劳状态
					val['aTime']= val['aTime']+ count
	
	@classmethod
	def updateRoomCardsHero(self, card_play, card_arr):
		x= card_arr.get('locaX')
		y= card_arr.get('locaY')
		card_play[0]['locaX']= x
		card_play[0]['locaY']= y
		 
	@classmethod
	def updateRoomCardsPlay(self, card_play, card , card_arr): 	
		#print 'updateRoomCardsPlay',card_play, card , card_arr
		if isinstance(card_play, list)== True and isinstance(card, dict)== True and isinstance(card_arr, dict)== True:		
			
			ret= 0
			type= card.get('type')	
			uniqid= card.get('uniqid')

			#check type, creature怪物 spell魔法 weapon武器  armor防具
			if type== HERO_CREATURE:
				#info= copy.deepcopy(card)
				info= card
				
				x= card_arr.get('locaX')
				y= card_arr.get('locaY')
				info['locaX']= x
				info['locaY']= y
				if info['hp']== 0:
					info['die'] = 1
				
				card_play.append(info)
				self.updatePlayCardsLocX2(card_play, x, uniqid)
				ret= 1
			elif type== HERO_SKILL:
				ret= 2
			elif type== HERO_EQUIPMENT:
				pass
			elif type== HERO_CREATURE_TOKEN:
				pass
			else:
				pass
				
			return ret
	
		else:
			return 0		
		
	@classmethod
	def putCardOnDesk(self, card_hand, card_play, card_arr): 	
		if isinstance(card_hand, list)== True and isinstance(card_play, list)== True and isinstance(card_arr, dict)== True:
			uniqid= int(card_arr.get('uniqid'))		
			if uniqid== None:
				return 0	
			
			pos, card= self.getRoomCardById(card_hand, uniqid)
			
			if card== None:
				return 0	
			
			ret= self.updateRoomCardsPlay(card_play, card, card_arr)	
			if ret== 0:
				return 0
					
			for m, n in enumerate(card_hand):
				if n.get('uniqid')== uniqid:
					card_hand.pop(m)
				
			return ret
	
		else:
			return 0
		
	@classmethod
	def updatePlayCardsLocX(self, room, pos, locax, uniqid, die= 0): 	
		if isinstance(room, dict)== False or isinstance(locax, int)== False or (pos!=1 and pos!= 2):
			return False
		if uniqid== None:
			return False
		
		if pos== 1:
			cards= room['cardPlay1']
		else:
			cards= room['cardPlay2']
		
		for index, val in enumerate(cards):
			x= int(val.get('locaX'))
			if x>= locax and val.get('die')== 0 and val.get('uniqid')!= uniqid  and val.get('type')!= HERO_HERO:
				if die== 0:
					val['locaX']= val['locaX']+ 1	
				else:
					val['locaX']= val['locaX']- 1	
					
	@classmethod
	def updatePlayCardsLocX2(self, cards, locax, uniqid, die= 0): 	
		if isinstance(cards, list)== False or isinstance(locax, int)== False:
			return False
		if uniqid== None:
			return False

		for index, val in enumerate(cards):
			x= int(val.get('locaX'))
			if x>= locax and val.get('die')== 0 and val.get('uniqid')!= uniqid and val.get('type')!= HERO_HERO:
				if die== 0:
					val['locaX']= val['locaX']+ 1	
				else:
					val['locaX']= val['locaX']- 1
					

				
	@classmethod	
	def getRoomPlayCardsMaxLocaX(self, cards):
		if isinstance(cards, list)== False:
			return 0
		
		x= 0
		for k, c in enumerate(cards):
			if c.get('locaX')>x and c.get('die')== 0 and c.get('hp')> 0 and c.get('type')!= HERO_HERO:
				x= c.get('locaX')
		return x		
		
	@classmethod
	def makeHeroCard(self, room, pos, hero):
		if isinstance(pos, int)== False or int(pos)<= 0 or isinstance(room, dict)== False or isinstance(hero, dict)== False:
			return 0
		_id= hero.get('_id')
		uniqid= self.getUniqid(_id)
		
		hero_card= self.getRoomCardCustomFormat(hero)
		hero_card['uniqid']= uniqid
		hero_card['type']= HERO_HERO
		hero_card['cost']= 0				
		#hero_card['durability']= 0
		hero_card['status']= 0
		hero_card['aTime']= 0		
		
		if pos== 1:
			# modified by tm：修改存储英雄信息为卡牌信息（因为英雄技能是当成一张卡牌来使用的）
			room['cardOrigin1'][uniqid] = hero_card # hero
			room['cardPlay1'].append(hero_card)
			return uniqid
		elif pos==2:
			room['cardOrigin2'][uniqid]= hero_card
			room['cardPlay2'].append(hero_card)
			return uniqid
		else:
			return 0
		
	@classmethod
	def makeHeroSkillCard(self, room, pos, hero):
		if isinstance(pos, int)== False or int(pos)<= 0 or isinstance(room, dict)== False or isinstance(hero, dict)== False:
			return 0
		_id= hero.get('_id')
		uniqid= self.getUniqid(_id)
		
		skill_card_id= hero['skillCardId']
		
		skill_card= CardModel.getCardsById(int(skill_card_id))
		
		skill_card['uniqid']= uniqid= self.getUniqid(skill_card['_id'])
		skill_card= self.getRoomCardCustomFormat(skill_card)
		
		if pos== 1:
			room['cardOrigin1'][uniqid]= skill_card
			room['cardHand1'].append(skill_card)
			return uniqid
		elif pos==2:
			room['cardOrigin2'][uniqid]= skill_card
			room['cardHand2'].append(skill_card)
			return uniqid
		else:
			return 0	
			
	@classmethod
	def getRoomStime(self, room, card, pos):
		if isinstance(room, dict)== False or isinstance(card, dict)== False or (pos!=1 and pos!= 2):
			return False
		if pos== 1:
			card['sTime']= room['stime1']	
		else:
			card['sTime']= room['stime2']	
			
	@classmethod
	def checkCardDie(self, room, pos, card): 	
		if isinstance(room, dict)== False or (pos!=1 and pos!= 2) or isinstance(card, dict)== False:
			return False
		
 	    #死亡
		if card['hp']== 0:
			card['die']= 1 
			RoomModel.updatePlayCardsLocX(room, pos, card['locaX'], card['uniqid'], 1)  
			return True
				
		return False
	
	@classmethod
	def getUniqid(self, id):
		if id> 1000000000:
			id= id % 1000
		return int(time.time())+  id + random.randint(1000000, 9999999)


			
		

