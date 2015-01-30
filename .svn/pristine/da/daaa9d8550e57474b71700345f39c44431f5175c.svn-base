# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from lib.mongo import Mongo
m= Mongo.getInstance('50.23.111.162', 27017)
db= m.myninja
tb= db['test']

i= 1000000
while i:
	data={
	"_id": i,
    "roomId":0,
    "pos1": None,
    "pos2": None,
	#首次摸牌者，1 or 2
    "first": 0,

	#战斗结果
    "result": 0,

	#回合
    "round": 0,
	#上一次是谁结束回合，1 or 2
    "turn": 0,
	#回合是否双方都结束
	"turnStatus": 0,

	#上一次攻击时间
    "actTime1": 0,
    "actTime2": 0,

	#换首牌时间
    "firstChangeCardTime1": 0,
    "firstChangeCardTime2": 0,
    
	#摸牌时间
    "firstGetCardTime1": 0,
    "firstGetCardTime2": 0,
	#双方全部完成摸牌时间
    "firstGetCardEndTime": 0,

	#确认首牌时间
    "confirmFirstHCTime1": 0,
    "confirmFirstHCTime2": 0,
	
	#当前法力水晶数量
    "crystal1":0 ,
    "crystal2":0 ,

	#首次摸牌 1 or 2
    "first": 0,

	#双方英雄
    "heros": [],

	#手牌
    "cardHand1": [],
    "cardHand2": [],

	#原始牌库, dict(10张)
	"cardOrigin1": {},
	"cardOrigin2": {},
	
	#牌库
	"cardAll1": [],
	"cardAll2": [],
	
	#桌面上的牌
    "cardPlay1": [],
    "cardPlay2": [],

	#武器 uniqid
	"weapon1": {},
	#武器 uniqid
	"weapon2": {},

	#特殊效果堆栈
	'effect1':{},

	#特殊效果堆栈
	'effect2':{},
	}
	tb.insert(data)
	i=i -1