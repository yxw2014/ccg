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
from config import *
from  BaseService import BaseService
from  CardModel import CardModel
from  HeroModel import HeroModel
from  RoomModel import RoomModel
from  FightModel import FightModel
from  SkillModel import SkillModel
from EffectHelperModel import EffectHelperModel

class FightService(BaseService): 
    def __init__(self): 
        super(FightService, self).__init__()
        self.data= copy.deepcopy(ROOM_INIT_DATA)  
        
    
    def testMethod(self, params):
        self.result["data"]= {"data1":11212, "data2": {"room_id":451377, "score":[3,5,6,8]}}
        return self.result, None
    
    def searchRoom(self, params): 
        '''
                        搜寻房间
        modified by tm at 2014-01-27
        1.add comment
        '''
        if(isinstance(params, dict) == False or params.get('uuid') == None or params.get('heroId') == None): 
            self.result["error"] = {"code":1, "msg": err[1]}
            return self.result, None
            
        # 用户唯一id(非用户id，而是标识该次会话的clientsocketid，可理解为bs里的sessionid)
        uuid = params.get('uuid')
        # 用户选择对战的套牌id
        uHeroId = params.get('heroId')
        # 将用户加入匹配列表 member=>uuid,score=>uHeroId
        self.__joinMatching({uuid : int(uHeroId)})
        #self.redis.zadd('hs:user:search'+ ":"+ self.server_id, uuid, int(uHeroId))  
        
        return self.__createRoom(params)
    
    def __joinMatching(self, u_dict):
        '''
                        新加用户进入匹配列表
        @param u_dict:{uuid1:heroid1, uuid2:heroid2}
        '''
        if not u_dict or not isinstance(u_dict, dict):
            return -1
        
        return self.redis.zadd('hs:user:search:' + self.server_id, **u_dict)
        
    def __exitMatcing(self, u_list):
        '''
                        从匹配列表中踢出用户（自己退出or匹配成功or被系统踢出）
        @param u_list:[uuid1,uuid2] 
        '''
        if not u_list or not isinstance(u_list, list):
            return -1
        
        self.redis.zrem('hs:user:search:' + self.server_id, *u_list)
    
    def __createRoom(self, params): 
        '''
                        创建房间
        modified by tm at 2014-01-27
        1.add commet
        2.优化代码逻辑
        @summary: 生成房间信息，将匹配成功的用户从匹配列表中移除
        '''
        if(isinstance(params, dict) == False or params.get('uuid') == None): 
                self.result["error"] = {"code":1, "msg": err[1]}           
                return self.result, None
         
        # 用户和对手的uuid   
        uuid, uuid2 = params.get('uuid'), None
        # 获取匹配列表中用户的总数
        total = self.redis.zcard('hs:user:search'+ ":"+ self.server_id)
        print "total", total
        retry_count = 5
        
        # 如果只有一个
        if total == 1:
            #self.result['error']= {'code':5, 'msg':err[5]}
            self.result['method'] = 'matcheding'
            self.result['data']['status'] = 'only one'
            return self.result, None
        elif total == 2:
            # 获取这两个人
            uuid_list = self.redis.zrange('hs:user:search:' + self.server_id, 0, 1)
            # 在列表中将自己移除
            uuid_list.remove(uuid)
            if len(uuid_list) > 0:
                uuid2 = uuid_list[0]
        else:
            while retry_count > 0:
                # 随机找个位置
                r = random.randint(0, total-1)
                uuid_r = self.redis.zrange('hs:user:search'+ ":"+ self.server_id, r, r)
                
                if len(uuid_r) > 0 and self.redis.zscore('hs:room:user'+ ":"+ self.server_id, uuid_r[0])== None and uuid_r[0] != uuid:
                    uuid2 = uuid_r[0]
                    break
                else:
                    pass  #todo
                retry_count = retry_count -1
        if uuid2 == None:
            self.result['method'] = 'matcheding'
            self.result['data']['status'] = 'uuid2 empty'
            return self.result, None
    
        retry_count = 3
        room_id = None
        # 生成房间号
        while retry_count > 0:
            r = str(random.randint(100000000, 900000000))
            if self.redis.exists('hs:room:info:' + r) == False:
                    room_id= r
                    break
            retry_count = retry_count -1
        if room_id == None:
            self.result['method'] = 'matcheding'
            self.result['data']['status'] = 'room_id empty'
            return self.result, None
        
        heroId1 = int(self.redis.zscore('hs:user:search:' + self.server_id, uuid))
        heroId2 = int(self.redis.zscore('hs:user:search:' + self.server_id, uuid2))
        hero1 = HeroModel.getSystemOrUserHerosById(uuid, heroId1)
        hero2 = HeroModel.getSystemOrUserHerosById(uuid2, heroId2)

        if hero1 == None or hero2 == None:
            self.result["error"] = {"code":21, "msg": err[21]}
            return self.result, None
        
        self.data['room_info']['pos1'] = uuid2
        self.data['room_info']['pos2'] = uuid
        self.data['room_info']['roomId'] = room_id
        self.data['room_info']['heros'] = [hero2, hero1]
        
        #make hero cards
        #hero1['hp']= int(config['GAME']['maxhp'])
        #hero2['hp']= int(config['GAME']['maxhp'])
        
        #user info
        hero1['uuid'] = uuid
        hero2['uuid'] = uuid2
        # 英雄也被视为一张手牌，只是有type为hero的特殊标识
        RoomModel.makeHeroCard(self.data['room_info'], 1, hero2)
        RoomModel.makeHeroCard(self.data['room_info'], 2, hero1)
        
        RoomModel.updateRoomCardsHero(self.data['room_info']['cardPlay1'], {'locaX':0, 'locaY':0})
        RoomModel.updateRoomCardsHero(self.data['room_info']['cardPlay2'], {'locaX':0, 'locaY':0})
        # 卡牌uniqid
        hero2['uniqid'] = self.data['room_info']['cardPlay1'][0]['uniqid']
        hero1['uniqid'] = self.data['room_info']['cardPlay2'][0]['uniqid']
        
        #　将房间信息存入redis
        RoomModel.setRoom(room_id, self.data['room_info'])      
        #self.redis.zadd('hs:room:user'+ ":"+ self.server_id, uuid, room_id, uuid2, room_id)  
        
        del hero1['createTime']
        del hero1['jobCards']
        del hero1['type']
        del hero1['aliasName']
        del hero1['level']
        del hero1['xp']
        del hero1['tutorialCards']
        
        del hero2['createTime']
        del hero2['jobCards']
        del hero2['type']
        del hero2['aliasName']
        del hero2['level']
        del hero2['xp']    
        del hero2['tutorialCards']
        
        #for security 
        room_info = {}
        room_info['roomId'] = self.data['room_info']['roomId']
        
        self.push_result['uuid'] = uuid2
        self.push_result['service'] = "main"
        self.push_result['method'] = "matchedSucceeded"

        self.push_result['params'] = {"heros":[hero2, hero1], "roomInfo": room_info, "first": 0}
        
        data = {"heros":[hero2, hero1], "roomInfo": room_info, "first": 1}
        self.result['data'] = data
        
        # 将该房间的两个用户都从匹配列表中删除
        self.__exitMatcing([uuid, uuid2])
        #self.redis.zrem('hs:user:search'+ ":"+ self.server_id, uuid, uuid2)
        #todo check user
        #self.redis.zadd('hs:room:user'+ ":"+ self.server_id, uuid, room_id)        
        
        self.result['method'] = "matchedSucceeded"
        return self.result, self.push_result
    
    '''
    def changeFirstHC(self, params):
        return None, None   
    '''
   
    def matchedSucceededComplete(self, params):
        '''
                        匹配成功，发手牌
        '''
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        room_id= params.get('roomId')
        room= RoomModel.getRoom(room_id)
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        round= room.get('round')            
        firstGetCardTime1= room.get('firstGetCardTime1')
        firstGetCardTime2= room.get('firstGetCardTime2')
        cardHand1=  room.get('cardHand1')
        cardHand2=  room.get('cardHand2')
        firstGetCardEndTime= room.get('firstGetCardEndTime')
        
        if FightModel.checkGameOver(room)== True:
                self.result["error"]= {"code":30, "msg": err[30]}           
                return self.result, None
            
        #reids have changed the type of the value 
        if round!= 0:
                self.result["error"]= {"code":16, "msg": err[16]}           
                return self.result, None
            
        if pos1== 'None' and pos2== 'None':
                self.result["error"]= {"code":17, "msg": err[17]}           
                return self.result, None
            
       
        if cardHand1== [] and  cardHand2== [] and firstGetCardEndTime== 0:
            #print 'here', pos1, pos2, cardHand1, cardHand2, uuid
            if uuid== pos1: 
                room['firstGetCardTime1']= int(time.time())     
                #room['cardHand1']= random.sample(self.data['hs_card'], 3)
                card_all= RoomModel.getRoomFirstCards(room, 1)                
                room['cardOrigin1']= dict(room['cardOrigin1'], **card_all)
                room['cardAll1']= RoomModel.getRoomCardsAll(card_all)
                #room['cardHand1']= random.sample(card_all, 3)
                room['cardHand1']= RoomModel.getRoomRandCards(room['cardAll1'], 3)
                
                #room['cardHand1']= json.dumps(CardModel.getCardsByRand(3)) 
                RoomModel.setRoom(room_id, room)
                return None, None
            elif uuid== pos2:
                room['firstGetCardTime2']= int(time.time())     
                #room['cardHand2']= random.sample(self.data['hs_card'], 3)
                card_all= RoomModel.getRoomFirstCards(room, 2)                    
                room['cardOrigin2']= dict(room['cardOrigin2'], **card_all) 
                room['cardAll2']= RoomModel.getRoomCardsAll(card_all)  
                #room['cardHand2']= random.sample(card_all, 3)
                room['cardHand2']= RoomModel.getRoomRandCards(room['cardAll2'], 3)
                #room['cardHand2']= json.dumps(CardModel.getCardsByRand(3))
                RoomModel.setRoom(room_id, room)
                return None, None
                
            else:
                return None, None
        else:                
            if (cardHand1!= [] and uuid== pos1) or (cardHand2!= [] and uuid== pos2):
                self.result["error"]= {"code":19, "msg": err[19]}           
                return self.result, None            
            elif (cardHand1!= [] and uuid== pos2):
                #print 'here2', pos1, pos2, type(cardHand1), cardHand1, type(cardHand2), cardHand2, uuid
                
                #push
                self.push_result['uuid']= pos1
                self.push_result['service']= "main"
                self.push_result['method']= "getFirstHC"                      
                    
                card_all= RoomModel.getRoomFirstCards(room, 2)
                room['cardAll2']= RoomModel.getRoomCardsAll(card_all)     
                room['cardOrigin2']= dict(room['cardOrigin2'], **card_all) 
                rand_card= RoomModel.getRoomRandCards(room['cardAll2'], 4)
                self.result['data']['cards']= RoomModel.getRoomCardsResult(rand_card)       
                self.result['data']['isFirst']= 0
                self.result['data']['oppCards']= RoomModel.getRoomCardsOppResult(room['cardHand1'])
                self.result['method']= 'getFirstHC'    
                
                #英雄技能        
                room['cardHand2']= rand_card
                uniqid_1= RoomModel.makeHeroSkillCard(room, 1, room['heros'][0])
                uniqid_2= RoomModel.makeHeroSkillCard(room, 2, room['heros'][1])  
                self.result['data']['skillCardUniqid']= uniqid_2
                
                #update cache
                room['firstGetCardTime2']= int(time.time())     
                room['firstGetCardEndTime']= int(time.time()) 
                room['first']= 1
                
                self.push_result['params']= {"cards": RoomModel.getRoomCardsResult(room['cardHand1']), "isFirst": 1, \
                            'oppCards': RoomModel.getRoomCardsOppResult(room['cardHand2']), 'skillCardUniqid':uniqid_1}                
    
                RoomModel.setRoom(room_id, room)
                
                return self.result, self.push_result                
            elif (cardHand2!= [] and uuid== pos1):
                #print 'here3', pos1, pos2, type(cardHand1), cardHand1, type(cardHand2), cardHand2, uuid
                
                #push
                self.push_result['uuid']= pos2
                self.push_result['service']= "main"
                self.push_result['method']= "getFirstHC"  
                
                card_all= RoomModel.getRoomFirstCards(room, 1)
                room['cardAll1']= RoomModel.getRoomCardsAll(card_all) 
                room['cardOrigin1']= dict(room['cardOrigin1'], **card_all)  
                rand_card= RoomModel.getRoomRandCards(room['cardAll1'], 4)
                self.result['data']['cards']= RoomModel.getRoomCardsResult(rand_card) 
                self.result['data']['isFirst']= 0
                self.result['data']['oppCards']= RoomModel.getRoomCardsOppResult(room['cardHand2'])
                self.result['method']= 'getFirstHC'
                
                #英雄技能        
                room['cardHand1']= rand_card
                uniqid_1= RoomModel.makeHeroSkillCard(room, 1, room['heros'][0])
                uniqid_2= RoomModel.makeHeroSkillCard(room, 2, room['heros'][1]) 
                self.result['data']['skillCardUniqid']= uniqid_1
                
                #update cache
                room['firstGetCardTime1']= int(time.time())     
                room['firstGetCardEndTime']= int(time.time())
                room['first']= 2
                
                self.push_result['params']= {"cards": RoomModel.getRoomCardsResult(room['cardHand2']), "isFirst": 1, \
                            'oppCards': RoomModel.getRoomCardsOppResult(room['cardHand1']), 'skillCardUniqid':uniqid_2} 

                RoomModel.setRoom(room_id, room)    
                    
                return self.result, self.push_result
            else:
                return None, None           
                
        return None, None
    
    def confirmFirstHC(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        room_id= params.get('roomId')
        
        room= RoomModel.getRoom(room_id)
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
        
        pos1= room.get('pos1')
        pos2= room.get('pos2')  
            
        round= room.get('round') 
        first= room.get('first') 
                
        confirmFirstHCTime1= room.get('confirmFirstHCTime1')
        confirmFirstHCTime2= room.get('confirmFirstHCTime2')
    
        if round!= 0:
            self.result["error"]= {"code":16, "msg": err[16]}           
            return self.result, None
            
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None
        if uuid== pos1:
            #print "here1----------"
            if confirmFirstHCTime2!= 0:
                #push
                self.push_result['uuid']= pos2
                self.push_result['service']= "main"
                self.push_result['method']= "startBattel"      
         

                if first==1:  
                    #对方为后手摸一张牌     
                    #new_card= RoomModel.getRoomRandCards(room['cardAll2'], 1)[0]  
                    new_card= CardModel.getCrystalCard() 
                    if new_card== None:
                        self.result["error"]= {"code":26, "msg": err[26]}           
                        return self.result, None
                    room['cardOrigin2'][new_card['uniqid']]= new_card        
                    room["cardHand2"].append(RoomModel.getRoomCardCustomFormat(new_card))                   
                    self.push_result['params']= {"cards":RoomModel.getRoomCardResult(new_card), "crystal": 0, "round": 1, "isFirst": 0}                    
                else:
                    #对方为先手 摸牌,但不是水晶牌
                    new_card= RoomModel.getRoomRandCards(room['cardAll2'], 1)[0] 
                    room["cardHand2"].append(new_card) 
                    self.push_result['params']= {"cards":RoomModel.getRoomCardResult(new_card), "crystal": 1, "round": 1, "isFirst": 1}
            
              
                #更新自己的手牌
                if first== 1:
                    #先手，自己摸牌
                    new_card= RoomModel.getRoomRandCards(room['cardAll1'], 1)[0]
                    room["cardHand1"].append(new_card) 
                    room['crystal1']= 1
                    self.result['data']['cards']= RoomModel.getRoomCardResult(new_card)
                    self.result['data']['isFirst']= 1
                    self.result['data']['crystal']= 1
                    
                    #攻击次数
                    RoomModel.updateRoomCardsPlayAtk(room['cardPlay1'], room['weapon1'])
                    RoomModel.updateRoomCardsSkillAtk(room, 1)                 
                else:  
                    #攻击次数
                    RoomModel.updateRoomCardsPlayAtk(room['cardPlay2'], room['weapon2'])
                    RoomModel.updateRoomCardsSkillAtk(room, 2)  
                       
                    #后手，自己摸一张牌 ，水晶牌 
                    #new_card= RoomModel.getRoomRandCards(room['cardAll1'], 1)[0]
                    new_card= CardModel.getCrystalCard() 
                    if new_card== None:
                        self.result["error"]= {"code":26, "msg": err[26]}           
                        return self.result, None  
                    room['cardOrigin1'][new_card['uniqid']]= new_card                  
                    room["cardHand1"].append(RoomModel.getRoomCardCustomFormat(new_card)) 
                    #对方为先手，加水晶
                    room['crystal2']= 1                                   
                    self.result['data']['cards']= RoomModel.getRoomCardResult(new_card) 
                    self.result['data']['isFirst']= 0 
                    self.result['data']['crystal']= 0
                    
                #opp
                self.result['data']['oppCards']= {'uniqid': self.push_result['params']['cards']['uniqid']}
                self.push_result['params']['oppCards']= {'uniqid': self.result['data']['cards']['uniqid']}
                                    
               
                self.result['data']['round']= 1
                self.result['method']= 'startBattel'
                
                 #回合
                room['round']= 1               
                room['confirmFirstHCTime1']= int(time.time())
                
                RoomModel.setRoom(room_id, room)
                return self.result, self.push_result
            
            room['confirmFirstHCTime1']= int(time.time())   
            RoomModel.setRoom(room_id, room)  
            return None, None
        elif uuid== pos2:
            #print "here2----------"
            if confirmFirstHCTime1!= 0:
                #push
                self.push_result['uuid']= pos1
                self.push_result['service']= "main"
                self.push_result['method']= "startBattel"   
                

                if first== 2:   
                    #对方为后手摸一张牌   
                    #new_card= RoomModel.getRoomRandCards(room['cardAll1'], 1)[0]
                    new_card= CardModel.getCrystalCard() 
                    if new_card== None:
                        self.result["error"]= {"code":26, "msg": err[26]}           
                        return self.result, None
                    room['cardOrigin1'][new_card['uniqid']]= new_card
                    room["cardHand1"].append(RoomModel.getRoomCardCustomFormat(new_card))                
                    self.push_result['params']= {"cards":RoomModel.getRoomCardResult(new_card), "crystal": 0, "round": 1, "isFirst": 0}
                else:
                    #对方为先手摸牌 ,但不是水晶牌
                    new_card= RoomModel.getRoomRandCards(room['cardAll1'], 1)[0]
                    room["cardHand1"].append(new_card) 
                    self.push_result['params']= {"cards":RoomModel.getRoomCardResult(new_card), "crystal": 1, "round": 1, "isFirst": 1}  
                
                #自己为先手，摸牌           
                if first== 2:       
                    new_card= RoomModel.getRoomRandCards(room['cardAll2'], 1)[0]
                    if new_card== None:
                        self.result["error"]= {"code":26, "msg": err[26]}           
                        return self.result, None
                    room["cardHand2"].append(new_card)  
                    room['crystal2']= 1
                    self.result['data']['crystal']= 1              
                    self.result['data']['cards']= RoomModel.getRoomCardResult(new_card)
                    self.result['data']['isFirst']= 1
                    
                    #攻击次数
                    RoomModel.updateRoomCardsPlayAtk(room['cardPlay2'], room['weapon2'])
                    RoomModel.updateRoomCardsSkillAtk(room, 2)
                else: 
                    #攻击次数
                    RoomModel.updateRoomCardsPlayAtk(room['cardPlay1'], room['weapon1'])
                    RoomModel.updateRoomCardsSkillAtk(room, 1)
                    
                    #自己为后手，摸水晶牌
                    #new_card= RoomModel.getRoomRandCards(room['cardAll2'], 1)[0]
                    new_card= CardModel.getCrystalCard() 
                    room['cardOrigin2'][new_card['uniqid']]= new_card
                    #对方为先手，加水晶
                    room['crystal1']= 1   
                    room["cardHand2"].append(RoomModel.getRoomCardCustomFormat(new_card))                    
                    self.result['data']['cards']= RoomModel.getRoomCardResult(new_card)
                    self.result['data']['isFirst']= 0
                    self.result['data']['crystal']= 0
                
                #opp
                self.result['data']['oppCards']= {'uniqid': self.push_result['params']['cards']['uniqid']}
                self.push_result['params']['oppCards']= {'uniqid': self.result['data']['cards']['uniqid']}
                    
                self.result['data']['round']= 1
                self.result['method']= 'startBattel'
                
                #回合
                room['round']= 1  
                room['confirmFirstHCTime2']= int(time.time())  
                
                
                RoomModel.setRoom(room_id, room)
                return self.result, self.push_result
            
            room['confirmFirstHCTime2']= int(time.time())
            RoomModel.setRoom(room_id, room)
            return None, None
        else:
            return None, None       
        
        return None, None
    
    def battleStageEvent(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        room_id= params.get('roomId')   
        
        room= RoomModel.getRoom(room_id)
        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
                
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None
        
        if uuid== pos1:
            uuid2= pos2
        elif uuid== pos2:
            uuid2= pos1
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
        #push
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "battleStageEvent"
        self.push_result['params']= params  
        
        return None, self.push_result           
    
    
    def turnStart(self, params):        
        return None, None 
    
    def turnEnd(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        room_id= params.get('roomId')   
        
        room= RoomModel.getRoom(room_id)
        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None   
             
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        last_turn= room.get('turn')
        
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None
        
        if uuid== pos1:
            uuid2= pos2
            k= "cardAll2"
            k2= "cardHand2"
            pos= 2
            turn= 1
            if turn== last_turn:
                self.result["error"]= {"code":24, "msg": err[24]}           
                return self.result, None
            #crystal= room.get('crystal2')
        elif uuid== pos2:
            uuid2= pos1
            k= "cardAll1"
            k2= "cardHand1"
            pos= 1
            turn= 2
            if turn== last_turn:
                self.result["error"]= {"code":24, "msg": err[24]}           
                return self.result, None
            #crystal= room.get('crystal1')
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
        #push
        obj= {}
        #if len(room.get(k))==0:
        if FightModel.doCheckAllCardsLeft(room,  pos)== True:
            obj['cards']= ''
        else: 
            # 本方回合结束，对方回合开始，对方随机从牌库中取一张牌置入对方手牌中
            new_card= RoomModel.getRoomRandCards(room.get(k), 1)[0]       
            obj['cards']= RoomModel.getRoomCardResult(new_card)
            room[k2].append(new_card)
            
        room['turn']= turn   
        
        #回合数加1
        if room['turnStatus']== 1:
            room['round']= room.get('round')+ 1
            room['turnStatus']= 0
        else:
            room['turnStatus']= 1        
        
        if uuid== pos1:
            #激活桌牌
            RoomModel.updateRoomCardsPlayAtk(room['cardPlay2'], room['weapon2'])
            RoomModel.updateRoomCardsPlaySelfAtk(room['cardPlay1'])
            
            #激活英雄技能            
            RoomModel.updateRoomCardsSkillAtk(room, 2)            
            RoomModel.updateRoomCardsSkillAtk(room, 1, 0)
            
            #武器
            room['wtime2']= 0
            room['wtime1']= 1
            
            #RoomModel.updateRoomCardsSkill(room['cardHand2'], 0)
            room['crystal2']= min(10, room.get('round'))
            
            desktop_card= room['cardPlay1']
            
            EffectHelperModel.turnEndEffectCallBack(room, 1)  
            self.__getDesktopCardsInfo(room, 1)           
            
        elif uuid== pos2:
            #激活桌牌
            RoomModel.updateRoomCardsPlayAtk(room['cardPlay1'], room['weapon1'])
            RoomModel.updateRoomCardsPlaySelfAtk(room['cardPlay2'])
            
            #激活英雄技能           
            RoomModel.updateRoomCardsSkillAtk(room, 1)            
            RoomModel.updateRoomCardsSkillAtk(room, 2, 0)
            
            #武器
            room['wtime2']= 1
            room['wtime1']= 0
            
            #RoomModel.updateRoomCardsSkill(room['cardHand1'], 0)
            room['crystal1']= min(10, room.get('round'))
            
            desktop_card= room['cardPlay2']
            
            EffectHelperModel.turnEndEffectCallBack(room, 2)
            self.__getDesktopCardsInfo(room, 2)
            
        #回复水晶
        self.push_result['params']['crystal']= min(10, room.get('round'))        
        self.push_result['params']['round']= room.get('round')
        #代表是自己的回合了
        self.push_result['params']['turn']= 1  
        self.push_result['params']['cards']= obj['cards']       
       
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "turnStart"
        
        self.result['method']= 'turnStart'    
        self.result['data']['round']= room.get('round')
        self.result['data']['cards']= obj['cards']
        RoomModel.setRoom(room_id, room)
        
        return self.result, self.push_result
    
    def __getDesktopCardsInfo(self, room, pos):
        '''
                        获取桌面上的卡牌信息（随从及英雄武器）
        modified by tm at 2014-01-27 
        1. add summary
        2. 整理代码逻辑
        ''' 
        index1, index2 = (pos == 1 and ('1', '2') or ('2', '1'))
        
        desktop_self= room.get('cardPlay' + index1) 
        desktop_opp= room.get('cardPlay' + index2)
        weapon= room.get('weapon' + index1) 
        weapon2= room.get('weapon' + index2) 
            
        sTime= room.get('stime' + index1) 
        sTime2= room.get('stime' + index2)    
    
        self.result['data']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
        if len(self.result['data']["desktopSelf"])>0:
            self.result['data']["desktopSelf"][0]["weapon"]= weapon
            RoomModel.getRoomStime(room, self.result['data']["desktopSelf"][0], int(index1))
            
        self.result['data']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
        if len(self.result['data']["desktopOpp"])>0:
            self.result['data']["desktopOpp"][0]["weapon"]= weapon2
            RoomModel.getRoomStime(room, self.result['data']["desktopOpp"][0], int(index2)) 

        self.push_result['params']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_opp)    
        if len(self.push_result['params']["desktopSelf"])>0:
            self.push_result['params']["desktopSelf"][0]["weapon"]= weapon2
            self.push_result['params']["desktopSelf"][0]["sTime"]= sTime2
        
        self.push_result['params']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_self)  
        if len(self.push_result['params']["desktopOpp"])>0:
            self.push_result['params']["desktopOpp"][0]["weapon"]= weapon
            self.push_result['params']["desktopOpp"][0]["sTime"]= sTime
    
    def __getDesktopCardsInfo_BAK(self, room, pos):   
        if pos== 1: 
            desktop_self= room.get('cardPlay1') 
            desktop_opp= room.get('cardPlay2')
            weapon= room.get('weapon1') 
            weapon2= room.get('weapon2') 
                
            sTime= room.get('stime1') 
            sTime2= room.get('stime2')    
        
            self.result['data']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            if len(self.result['data']["desktopSelf"])>0:
                self.result['data']["desktopSelf"][0]["weapon"]= weapon
                RoomModel.getRoomStime(room, self.result['data']["desktopSelf"][0], 1)
                
            self.result['data']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            if len(self.result['data']["desktopOpp"])>0:
                self.result['data']["desktopOpp"][0]["weapon"]= weapon2
                RoomModel.getRoomStime(room, self.result['data']["desktopOpp"][0], 2) 
        elif pos== 2: 
            desktop_self= room.get('cardPlay2') 
            desktop_opp= room.get('cardPlay1')
            weapon= room.get('weapon2') 
            weapon2= room.get('weapon1') 
                
            sTime= room.get('stime2') 
            sTime2= room.get('stime1')    
        
            self.result['data']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            if len(self.result['data']["desktopSelf"])>0:
                self.result['data']["desktopSelf"][0]["weapon"]= weapon
                RoomModel.getRoomStime(room, self.result['data']["desktopSelf"][0], 2)
                
            self.result['data']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            if len(self.result['data']["desktopOpp"])>0:
                self.result['data']["desktopOpp"][0]["weapon"]= weapon2
                RoomModel.getRoomStime(room, self.result['data']["desktopOpp"][0], 1) 

        self.push_result['params']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_opp)    
        if len(self.push_result['params']["desktopSelf"])>0:
            self.push_result['params']["desktopSelf"][0]["weapon"]= weapon2
            self.push_result['params']["desktopSelf"][0]["sTime"]= sTime2
        
        self.push_result['params']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_self)  
        if len(self.push_result['params']["desktopOpp"])>0:
            self.push_result['params']["desktopOpp"][0]["weapon"]= weapon
            self.push_result['params']["desktopOpp"][0]["sTime"]= sTime

    
    def atkTarget(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None or params.get('attacker')== None or params.get('target')== None): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        #attacker_cardId= int(params.get('attacker').get('cardId', 0))
        #target_cardId= int(params.get('target').get('cardId', 0))
        
        attacker_id= int(params.get('attacker').get('uniqid', 0))
        
        #todo 扩展攻击多个目标的形式
        if isinstance(params.get('target'), list)== True:
            target_id= int(params.get('target')[0].get('uniqid', 0))
        else:
            target_id= int(params.get('target').get('uniqid', 0))
        
        #attacker_type= int(params.get('attacker').get('type', 0))
        #target_type= int(params.get('target').get('type', 0))
        #do card type checking and losts of other things    
        
        attacker_type= 1
        target_type= 1
        
        room_id= params.get('roomId') 
        room= RoomModel.getRoom(room_id)
        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
               
        pos1= room.get('pos1')
        pos2= room.get('pos2')    
        if uuid!= pos1 and uuid != pos2:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None    
        
        if pos1== 'None' or pos2== 'None': 
            print   '17---------', pos1, pos2    
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None
        
        if attacker_type!= 0: 
            
            if uuid== pos1: 
                pos= 1                
                attacker_card_pos, attacker_card_info= RoomModel.getRoomCardById(room.get('cardPlay1'), attacker_id)
                print '@@@here1', uuid, attacker_id , type(attacker_id), type(attacker_card_info) 
            else:
                pos= 2                
                attacker_card_pos, attacker_card_info= RoomModel.getRoomCardById(room.get('cardPlay2'), attacker_id)
                print '@@@here2', uuid, attacker_id , type(attacker_id), type(attacker_card_info) 
            if(attacker_card_info== None):
                self.result["error"]= {"code":17, "msg": err[17]}           
                return self.result, None
        else:
            attacker_card_pos, attacker_card_info= None, None
            
        if target_type!= 0:          
            if uuid== pos2: 
                
                target_card_pos, target_card_info= RoomModel.getRoomCardById(room.get('cardPlay1'), target_id)
                print '@@@here3', uuid, target_id , type(target_id), type(target_card_info)  
            else:                
                target_card_pos, target_card_info= RoomModel.getRoomCardById(room.get('cardPlay2'), target_id)      
                print '@@@here4', uuid, target_id , type(target_id), type(target_card_info)      
            if(target_card_info== None):
                self.result["error"]= {"code":17, "msg": err[17]}           
                return self.result, None
        else:
            target_card_pos, target_card_info= None, None 
            
        ret= FightModel.checkAttackerAtkTime(attacker_card_info)  
             
        if attacker_card_info['atk']== 0:
            self.result["error"]= {"code":33, "msg": err[33]}           
            return self.result, None  
        
        if(attacker_card_info['hp']== 0 or target_card_info['hp']== 0 or ret== False):
            self.result["error"]= {"code":27, "msg": err[27]}           
            return self.result, None
        
        
        ret= FightModel.checkAttackerStatusStun(room,  pos, target_id)
        print '///////////FightModel.checkAttackerStatusStun', ret       
        if(ret== True):
            self.result["error"]= {"code":35, "msg": err[35]}           
            return self.result, None
        
        ret= FightModel.checkTargetStatusTaunt(room,  pos, target_id)
        print '///////////FightModel.checkTargetStatusTaunt', ret       
        if(ret== True):
            self.result["error"]= {"code":27, "msg": err[27]}           
            return self.result, None
        
        #检查武器耐久度
        if (attacker_card_info['type']== HERO_HERO):            
            if uuid== pos1: 
                if room['weapon1'].get('uniqid')== None:
                    self.result["error"]= {"code":32, "msg": err[32]}           
                    return self.result, None
                
                if room['weapon1'].get('hp')== 0:
                    self.result["error"]= {"code":31, "msg": err[31]}           
                    return self.result, None
                room['weapon1']['hp']= room['weapon1']['hp']- 1
                room['weapon1']['hp']= max(0, room['weapon1']['hp'])
            elif uuid== pos2:  
                if room['weapon2'].get('uniqid')== None:
                    self.result["error"]= {"code":32, "msg": err[32]}           
                    return self.result, None
                
                if room['weapon2'].get('hp')== 0:
                    self.result["error"]= {"code":31, "msg": err[31]}           
                    return self.result, None
                room['weapon2']['hp']= room['weapon2']['hp']- 1
                room['weapon2']['hp']= max(0, room['weapon2']['hp']) 
 
            
        return self.__doAtkTarget(room, params, uuid, pos1, pos2, attacker_card_pos, target_card_pos, attacker_card_info, target_card_info, attacker_type, target_type)

    
    def __doAtkTarget(self, room, params, uuid, pos1, pos2, attacker_card_pos, target_card_pos, attacker_card_info, target_card_info, attacker_type, target_type):
        #todo paramers check
        #type=0为英雄,type=1为随从卡，type=2 法术卡， typ=3 奥秘卡    
        #怪物攻击怪物
        if attacker_type== 1 and target_type== 1: 
            damage= attacker_card_info.get('atk')
            damage2= target_card_info.get('atk')   
                
            if uuid== pos1:
                uuid2= pos2
                #if attacker_card_info.get('type')== HERO_HERO:
                    #damage= damage+ room['weapon1']['atk']
                '''
                room['cardPlay1'][attacker_card_pos]['hp']= room['cardPlay1'][attacker_card_pos]['hp']- damage2
                room['cardPlay1'][attacker_card_pos]['hp']= max(room['cardPlay1'][attacker_card_pos]['hp'], 0)
                
                room['cardPlay2'][target_card_pos]['hp']= room['cardPlay2'][target_card_pos]['hp']- damage
                room['cardPlay2'][target_card_pos]['hp']= max(room['cardPlay2'][target_card_pos]['hp'], 0)
                '''
                if room['cardPlay2'][target_card_pos]['type']!= HERO_HERO:
                    FightModel.doDamage(room['cardPlay1'][attacker_card_pos], damage2)
                
                FightModel.doDamage(room['cardPlay2'][target_card_pos], damage)
                
                
                #死亡
                RoomModel.checkCardDie(room, 1, room['cardPlay1'][attacker_card_pos])
                
                RoomModel.checkCardDie(room, 2, room['cardPlay2'][target_card_pos])        
                
                #modified aTime
                room['cardPlay1'][attacker_card_pos]['aTime']= max(0, (room['cardPlay1'][attacker_card_pos]['aTime'] -1))
                #modified  durability
                if room['cardPlay1'][attacker_card_pos]['type']== HERO_HERO:
                    #当前回合已经使用过武器，不能再使用武器
                    room['wtime1']= 1
                    FightModel.checkWeapon(room, 1, room['weapon1']['hp'])                     
                    #武器
                    params['attacker']['weapon']= room['weapon1']  
         
                if room['cardPlay2'][target_card_pos]['type']== HERO_HERO:                     
                    FightModel.checkWeapon(room, 2, room['weapon2'].get('hp'))   
                    
                    #武器
                    params['target']['weapon']= room['weapon2'] 
                    
                params['attacker']['hp']= room['cardPlay1'][attacker_card_pos]['hp']
                params['attacker']['aTime']= room['cardPlay1'][attacker_card_pos]['aTime']
                params['target']['hp']= room['cardPlay2'][target_card_pos]['hp'] 
                self.__getDesktopCardsInfo(room, 1)
            elif uuid== pos2:
                uuid2= pos1
                #if attacker_card_info.get('type')== HERO_HERO:
                    #damage= damage+ room['weapon2']['atk']
                '''
                room['cardPlay2'][attacker_card_pos]['hp']= room['cardPlay2'][attacker_card_pos]['hp']- damage2
                room['cardPlay2'][attacker_card_pos]['hp']= max(room['cardPlay2'][attacker_card_pos]['hp'], 0)
                    
                room['cardPlay1'][target_card_pos]['hp']= room['cardPlay1'][target_card_pos]['hp']- damage
                room['cardPlay1'][target_card_pos]['hp']= max(room['cardPlay1'][target_card_pos]['hp'], 0)
                '''
                if room['cardPlay1'][target_card_pos]['type']!= HERO_HERO:
                    FightModel.doDamage(room['cardPlay2'][attacker_card_pos], damage2)
                
                FightModel.doDamage(room['cardPlay1'][target_card_pos], damage)
                
                #死亡
                RoomModel.checkCardDie(room, 2, room['cardPlay2'][attacker_card_pos])
                
                RoomModel.checkCardDie(room, 1, room['cardPlay1'][target_card_pos])                   
                
                #modified aTime
                room['cardPlay2'][attacker_card_pos]['aTime']= max(0, (room['cardPlay2'][attacker_card_pos]['aTime'] -1))
                
                
                #modified  durability
                if room['cardPlay2'][attacker_card_pos]['type']== HERO_HERO: 
                    #当前回合已经使用过武器，不能再使用武器
                    room['wtime2']= 1
                    FightModel.checkWeapon(room, 2, room['weapon2']['hp'])  
                    
                    #武器
                    params['attacker']['weapon']= room['weapon2']    
                
                if room['cardPlay1'][target_card_pos]['type']== HERO_HERO: 
                    
                    FightModel.checkWeapon(room, 1, room['weapon1'].get('hp'))  
                    
                    #武器
                    params['target']['weapon']= room['weapon1']               
     
                params['attacker']['hp']= room['cardPlay2'][attacker_card_pos]['hp']
                params['attacker']['aTime']= room['cardPlay2'][attacker_card_pos]['aTime']
                params['target']['hp']= room['cardPlay1'][target_card_pos]['hp']
                self.__getDesktopCardsInfo(room, 2)        
        else:
            return None, None 
        
        #上方英雄死了，
        if room['cardPlay2'][0]['hp']==0:
            params['attacker']['state']= {'over': 1, 'win': 0}
            room['result']= 1
        elif room['cardPlay1'][0]['hp']== 0:
            params['attacker']['state']= {'over': 1, 'win': 1} 
            room['result']= 2
        #都输了    
        if room['cardPlay2'][0]['hp']==0 and  room['cardPlay1'][0]['hp']== 0:
            room['result']= 3  
                   
        #push               
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "atkTarget"
        #self.push_result['params']= params  
        self.push_result['params']= dict(self.push_result['params'], **params) 
                
        self.result['data']= dict(self.result['data'], **params) 
        self.result['method']= 'atkTarget'
        
        RoomModel.setRoom(room['roomId'], room)
        
        return self.result, self.push_result   
   
    #使用武器卡                  
    def UseWeaponCard(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None or params.get('card')== None):                                                                    
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uuid= params.get('uuid')     
           
        cards= params.get('card')        
        if isinstance(cards, dict)== False:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uniqid= int(cards.get('uniqid'))
                
        if uniqid== None:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        room_id= params.get('roomId')   
        room= RoomModel.getRoom(room_id)  
              
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
                
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None        

        if uuid== pos1:
            uuid2= pos2
                        
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand1'), room.get('cardOrigin1'), uniqid)
            
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None    
            
            cards['_id']= info.get('_id')     
            skill_id= info.get('skillId')
            
            type= info.get('type')  
            if type!= HERO_WEAPON:
                self.result["error"]= {"code":29, "msg": err[29]}           
                return self.result, None
            
            #not enough crystal
            if info.get('cost')> room.get('crystal1'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None  
            
            room['cardPlay1'][0]['atk']= info['atk']  
            
            room['crystal1']= room['crystal1']- info.get('cost')             
            room['crystal1']= max(0, room['crystal1'])  
            
            desktop_opp= room.get('cardPlay2')       
            desktop_self= room.get('cardPlay1')  
            weapon2= room.get('weapon2')
            sTime2= room.get('stime2')           
            
            self.result['data']["crystal"]= room['crystal1'] 
            if room['wtime1']== 0:
                RoomModel.updateRoomCardsHeroAtk(room, 1)
            room['wtime1']=1
                 
            room['weapon1']= RoomModel.getRoomCardsWeaponResult(info)
            
            self.result['data']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            self.result['data']["card"]= cards 
            
            self.result['data']["desktopSelf"][0]["weapon"]= room['weapon1']
            self.result['data']["desktopOpp"][0]["weapon"]= weapon2
            
            RoomModel.getRoomStime(room, self.result['data']["desktopSelf"][0], 1)
            RoomModel.getRoomStime(room, self.result['data']["desktopOpp"][0], 2) 
                       
            weapon= room.get('weapon1') 
            sTime= room.get('stime1')  
        elif uuid== pos2:
            uuid2= pos1
            
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand2'), room.get('cardOrigin2'), uniqid)
            
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None 
            
            cards['_id']= info.get('_id') 
            skill_id= info.get('skillId')
            
            type= info.get('type')  
            if type!= HERO_WEAPON:
                self.result["error"]= {"code":29, "msg": err[29]}           
                return self.result, None            
            
            #not enough crystal
            if info.get('cost')> room.get('crystal2'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None  
            
            room['cardPlay2'][0]['atk']= info['atk'] 
            
            room['crystal2']= room['crystal2']- info.get('cost') 
            room['crystal2']= max(0, room['crystal2'])              
              
            desktop_opp= room.get('cardPlay1')       
            desktop_self= room.get('cardPlay2') 
            weapon2= room.get('weapon1') 
            sTime2= room.get('stime1') 
            
            self.result['data']["crystal"]= room['crystal2']
            
            if room['wtime2']== 0:
                RoomModel.updateRoomCardsHeroAtk(room, 2)
            room['wtime2']== 1 
            room['weapon2']= RoomModel.getRoomCardsWeaponResult(info)
            
            self.result['data']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp) 
            self.result['data']["card"]= cards 
            
            self.result['data']["desktopSelf"][0]["weapon"]= room['weapon2']
            self.result['data']["desktopOpp"][0]["weapon"]= weapon2
            
            RoomModel.getRoomStime(room, self.result['data']["desktopSelf"][0], 2)
            RoomModel.getRoomStime(room, self.result['data']["desktopOpp"][0], 1)             
            
            weapon= room.get('weapon2') 
            sTime= room.get('stime2') 
            
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
        #push               
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "desktopWeaponChange"
        
        self.push_result['params']["desktopSelf"]= RoomModel.getRoomCardsPlayResult(desktop_opp)   
        self.push_result['params']["desktopSelf"][0]["weapon"]= weapon2
        self.push_result['params']["desktopSelf"][0]["sTime"]= sTime2  
        
        self.push_result['params']["desktopOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_self)  
        self.push_result['params']["desktopOpp"][0]["weapon"]= weapon 
        self.push_result['params']["desktopOpp"][0]["sTime"]= sTime 
        
        self.push_result['params']["card"]= cards   
   
        self.result['method']= 'desktopWeaponChange'
        
        RoomModel.setRoom(room_id, room)
        
        return self.result, self.push_result
    
    #使用技能卡                  
    def UseSkillCard(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None or params.get('card')== None):                                                                    
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uuid= params.get('uuid')     
           
        cards= params.get('card')  
        target= params.get('target')    
    
        if isinstance(target, list)== False:
            target= []
               
        if isinstance(cards, dict)== False:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uniqid= int(cards.get('uniqid'))
                
        if uniqid== None:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        room_id= params.get('roomId')   
        room= RoomModel.getRoom(room_id)        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
                
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None        

        if uuid== pos1:
            uuid2= pos2
                        
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand1'), room.get('cardOrigin1'), uniqid)
            type= info.get('type') 
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None   
            
            if type!= HERO_SKILL and type!= HERO_HEROSKILL:
                self.result["error"]= {"code":29, "msg": err[29]}           
                return self.result, None
            
            if type== HERO_HEROSKILL and room['stime1']== 0:
                self.result["error"]= {"code":34, "msg": err[34]}           
                return self.result, None  
            '''
            #not enough crystal            
            if info.get('cost')> room.get('crystal1'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None    
            '''
            cards['_id']= info.get('_id')     
            skill_id= str(info.get('skillId'))
            #skill_id= '10000301'
            
            #skill= SkillModel.getSkillById(skill_id)
            skill= SkillModel.getSkillByIds(skill_id)   
            effects= SkillModel.parseEffects(room, 1, uniqid, skill)  
            print 'UseSkillCard', skill_id, skill, effects  
            effect_stack= room['effect1']   
        
            SkillModel.triggerEffects(room, effects, 1, target)

            room['crystal1']= room['crystal1']- info.get('cost')             
            room['crystal1']= max(0, room['crystal1'])  
            room['stime1']= 1  
            
            #加法力水晶
            #room['crystal1']= room['crystal1']+  1 
            
            #if type!= 'Spell':
                #room['cardHand1'][pos]['die']= 1
                
            
            self.result['data']["crystal"]= room['crystal1']
            
            '''
            self.result['data']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["dSelf"][0]["weapon"]= weapon
            
            self.result['data']["dOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            self.result['data']["dOpp"][0]["weapon"]= weapon2
            '''
            if type== HERO_HEROSKILL:
                RoomModel.updateRoomCardsSkillAtk(room, 1, 0)
            else:
                room['cardHand1'][pos]['die']= 1
                
            '''
            RoomModel.getRoomStime(room, self.result['data']["dSelf"][0], 1)
            RoomModel.getRoomStime(room, self.result['data']["dOpp"][0], 2)             
            '''
            self.__getDesktopCardsInfo(room, 1)
            
            self.result['data']["card"]= cards 
            self.result['data']["target"]= target 
        elif uuid== pos2:
            uuid2= pos1
            
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand2'), room.get('cardOrigin2'), uniqid)
            type= info.get('type')
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None 
            
            if type!= HERO_SKILL and type!= HERO_HEROSKILL:
                self.result["error"]= {"code":29, "msg": err[29]}           
                return self.result, None
            
            if type== HERO_HEROSKILL and room['stime2']== 0:
                self.result["error"]= {"code":34, "msg": err[34]}           
                return self.result, None 
            '''
            #not enough crystal
            if info.get('cost')> room.get('crystal2'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None 
            '''
            cards['_id']= info.get('_id') 
            skill_id= str(info.get('skillId'))
            #skill_id= '10000301' 
            
            #skill= SkillModel.getSkillById(skill_id)
            skill= SkillModel.getSkillByIds(skill_id)       
            effects= SkillModel.parseEffects(room, 2, uniqid, skill)          
            print 'UseSkillCard', skill_id, skill, effects         
            effect_stack= room['effect2']   
      
            SkillModel.triggerEffects(room, effects, 2, target)   

            room['crystal2']= room['crystal2']- info.get('cost') 
            room['crystal2']= max(0, room['crystal2'])
            room['stime2']= 1  
            
            #加水晶  
            #room['crystal2']= room['crystal2']+ 1 
            
            #if type!= 'Spell':
                #room['cardHand2'][pos]['die']= 1
            
            self.result['data']["crystal"]= room['crystal2'] 
            '''
            self.result['data']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["dSelf"][0]["weapon"]= weapon
            
            self.result['data']["dOpp"]= RoomModel.getRoomCardsPlayResult(desktop_opp) 
            self.result['data']["dOpp"][0]["weapon"]= weapon2
            '''
            if type== HERO_HEROSKILL:
                RoomModel.updateRoomCardsSkillAtk(room, 2, 0)
            else:
                room['cardHand2'][pos]['die']= 1
            
            '''
            RoomModel.getRoomStime(room, self.result['data']["dSelf"][0], 2)
            RoomModel.getRoomStime(room, self.result['data']["dOpp"][0], 1)             
            '''
            self.__getDesktopCardsInfo(room, 2)
            
            self.result['data']["card"]= cards 
            self.result['data']["target"]= target 
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
        #push               
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "desktopSkillchange"
        '''
        self.push_result['params']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_opp)    
        self.push_result['params']["dSelf"][0]["weapon"]= weapon2
        self.push_result['params']["dSelf"][0]["sTime"]= sTime2
        
        self.push_result['params']["dOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_self)  
        self.push_result['params']["dOpp"][0]["weapon"]= weapon
        self.push_result['params']["dOpp"][0]["sTime"]= sTime
        '''
        self.push_result['params']["card"]= cards   
        self.push_result['params']["target"]= target 
        if uuid== pos1:
            self.push_result['params']["crystal"]= room['crystal2']
        else:
            self.push_result['params']["crystal"]= room['crystal1']        
            
        self.result['method']= 'desktopSkillchange'
        
        RoomModel.setRoom(room_id, room)
        
        return self.result, self.push_result
    
    
    def putCardOnDesk(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None or params.get('card')== None):                                                                    
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uuid= params.get('uuid')     
           
        cards= params.get('card')      
        target= params.get('target')    
    
        if isinstance(target, list)== False:
            target= []
              
        if isinstance(cards, dict)== False:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        uniqid= int(cards.get('uniqid'))
                
        if uniqid== None:
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        
        room_id= params.get('roomId')   
        room= RoomModel.getRoom(room_id)        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
                
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None        

        if uuid== pos1:
            uuid2= pos2
                        
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand1'), room.get('cardOrigin1'), uniqid)
            
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None    
            cards['_id']= info.get('_id')     
            skill_id= str(info.get('skillId'))    
   
            skills= SkillModel.getSkillByIds(skill_id)   
            effects= SkillModel.parseEffects(room, 1, uniqid, skills)  
            print skills, effects
            effect_stack= room['effect1']
            
            
            #not enough crystal
            if info.get('cost')> room.get('crystal1'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None             
            
            update_result= RoomModel.putCardOnDesk(room['cardHand1'] , room['cardPlay1'] , cards)
            print '######update_result', update_result  
            if update_result== 1:
                SkillModel.triggerEffects(room, effects, 1, target)  
                SkillModel.addRoomEffectToStack(effect_stack, effects)
                
            #todo    
            #print '@target', SkillModel.triggerStackEffects(room, 2, 1)
            '''
            desktop_opp= room.get('cardPlay2')       
            desktop_self= room.get('cardPlay1') 
            weapon= room.get('weapon1') 
            weapon2= room.get('weapon2') 
            sTime= room.get('stime1') 
            sTime2= room.get('stime2') 
            '''
            room['crystal1']= room['crystal1']- info.get('cost') 
            room['crystal1']= max(0, room['crystal1'])      
            '''
            self.result['data']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["dSelf"][0]["weapon"]= weapon
            self.result['data']["dOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            self.result['data']["dOpp"][0]["weapon"]= weapon2
            
            RoomModel.getRoomStime(room, self.result['data']["dSelf"][0], 1)
            RoomModel.getRoomStime(room, self.result['data']["dOpp"][0], 2) 
            '''
            self.result['data']["crystal"]= room['crystal1'] 
            self.__getDesktopCardsInfo(room, 1)
            self.result['data']["card"]= cards 
        elif uuid== pos2:
            uuid2= pos1
            
            pos, info= RoomModel.getRoomCardWithInfoById(room.get('cardHand2'), room.get('cardOrigin2'), uniqid)
            
            if pos== None or info== None:
                self.result["error"]= {"code":22, "msg": err[22]}           
                return self.result, None 
            cards['_id']= info.get('_id') 
            skill_id= str(info.get('skillId'))

            skills= SkillModel.getSkillByIds(skill_id)   
            effects= SkillModel.parseEffects(room, 2, uniqid, skills)         
            print skills, effects
                    
            effect_stack= room['effect2']             
            
            #not enough crystal
            if info.get('cost')> room.get('crystal2'):
                self.result["error"]= {"code":23, "msg": err[23]}           
                return self.result, None                  
            
            update_result= RoomModel.putCardOnDesk(room['cardHand2'] , room['cardPlay2'] , cards)  
            print '######update_result', update_result
            if update_result== 1:
                SkillModel.triggerEffects(room, effects, 2, target)
                SkillModel.addRoomEffectToStack(effect_stack, effects)
            
            #todo
            #print '@target', SkillModel.triggerStackEffects(room, 2, 2)
            '''
            desktop_self= room.get('cardPlay2') 
            desktop_opp= room.get('cardPlay1') 
            weapon= room.get('weapon2') 
            weapon2= room.get('weapon1') 
            sTime= room.get('stime2') 
            sTime2= room.get('stime1') 
            '''
            room['crystal2']= room['crystal2']- info.get('cost')
            room['crystal2']= max(0, room['crystal2'])
            '''
            self.result['data']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_self)
            self.result['data']["dSelf"][0]["weapon"]= weapon
            self.result['data']["dOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_opp)
            self.result['data']["dOpp"][0]["weapon"]= weapon2 
            
            RoomModel.getRoomStime(room, self.result['data']["dSelf"][0], 2)
            RoomModel.getRoomStime(room, self.result['data']["dOpp"][0], 1) 
            '''
            self.result['data']["crystal"]= room['crystal2'] 
            self.__getDesktopCardsInfo(room, 2)
            
            self.result['data']["card"]= cards 
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
        #push               
        self.push_result['uuid']= uuid2
        self.push_result['service']= "main"
        self.push_result['method']= "desktopChange"
        '''
        self.push_result['params']["dSelf"]= RoomModel.getRoomCardsPlayResult(desktop_opp)    
        self.push_result['params']["dSelf"][0]["weapon"]= weapon2
        self.push_result['params']["dSelf"][0]["sTime"]= sTime2
        self.push_result['params']["dOpp"]= RoomModel.getRoomCardsOppPlayResult(desktop_self) 
        self.push_result['params']["dOpp"][0]["weapon"]= weapon
        self.push_result['params']["dOpp"][0]["sTime"]= sTime
        '''
        if uuid== pos1:
            self.push_result['params']["crystal"]= room['crystal2']
        else:
            self.push_result['params']["crystal"]= room['crystal1']  
        self.push_result['params']["card"]= cards   
            
        self.result['method']= 'desktopChange'
        
        RoomModel.setRoom(room_id, room)
        
        return self.result, self.push_result

    def changeFirstHC(self, params):
        if(isinstance(params, dict)== False or params.get('uuid')== None or params.get('roomId')== None \
                        or params.get('uniqid')== None  or isinstance(params.get('cards'), list)== False): 
            self.result["error"]= {"code":1, "msg": err[1]}           
            return self.result, None
        uuid= params.get('uuid')
        uniqid= params.get('uniqid')
        cards= params.get('cards')
        
        room_id= params.get('roomId')   
        room= RoomModel.getRoom(room_id)        
        if FightModel.checkGameOver(room)== True:
            self.result["error"]= {"code":30, "msg": err[30]}           
            return self.result, None
                
        pos1= room.get('pos1')
        pos2= room.get('pos2')
        
        cardHand1=  room.get('cardHand1')
        cardHand2=  room.get('cardHand2')
        
        count= len(cards)
            
        if pos1== 'None' or pos2== 'None':
            self.result["error"]= {"code":17, "msg": err[17]}           
            return self.result, None      
      
        if uuid== pos1:
            uuid2= pos2 
                    
            cardHand1= room.get('cardHand1')
            if cardHand1== []:
                self.result["error"]= {"code":17, "msg": err[17]}           
                return self.result, None
            else:
                #new_cards= CardModel.getCardsByRand(count)
                new_cards= RoomModel.getRoomRandCards(room['cardAll1'], count)
            
                for k, c in enumerate(cardHand1): 
                    if cards.count(str(c.get('uniqid')))> 0:
                        tmp= cardHand1.pop(k)
                        #被换的排放回仓库
                        room['cardAll1'].append(tmp)
                        
                cardHand1+= new_cards

            room["cardHand1"]= cardHand1
        elif uuid== pos2:
            uuid2= pos1         
            cardHand2= room.get('cardHand2')
            if cardHand2== []:
                self.result["error"]= {"code":17, "msg": err[17]}           
                return self.result, None
            else:
                #new_cards= CardModel.getCardsByRand(count)
                new_cards= RoomModel.getRoomRandCards(room['cardAll2'], count)            
                for k, c in enumerate(cardHand2): 
                    if cards.count(c.get('uniqid'))> 0:
                        tmp= cardHand2.pop(k)
                        #被换的排放回仓库
                        room['cardAll2'].append(tmp)
                        
                cardHand2+= new_cards   
            room["cardHand2"]= cardHand2    
        else:
            self.result["error"]= {"code":6, "msg": err[6]}           
            return self.result, None
        
    
        self.result['data']["cards"]= new_cards 
        self.result['method']= 'changeFirstHC'
        #pprint(room["cardHand1"])
        #pprint(room["cardHand2"])
        
        RoomModel.setRoom(room_id, room)
        
        return self.result, None
    
    
    

