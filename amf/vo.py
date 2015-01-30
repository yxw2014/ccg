# -*- coding: utf-8 -*-

import copy

def makeVo(data, oo):		
	if isinstance(data, list)== True:
		for index, r in enumerate(data):
			vo= copy.deepcopy(oo) 
			for k, v in r.items():
				#vo.k= v
				if hasattr(vo, k):
					vo.__setattr__(k,v)
			data[index]= vo
		return data
	elif isinstance(data, dict)== True:
		vo= copy.deepcopy(oo) 
		for k, v in data.items():
			if hasattr(vo, k):
				vo.__setattr__(k,v)
		return vo
	else:
		return None

class CardVO(object):
    _id= 0
    name= ''
    type= ''
    detail= ''
    cardClass= ''
    #playerLevel= 0
    #heroLevel= 0
    img= ''
    swf= ''
    hp= 0
    atk= 0
    skillId= 0
    durabilityCount= 0
    rarity= ''
    race= ''
    race1= ''
    element= ''
    version= ''
    versionSerial= 0
    cost= 0
	


class HeroVO(object):
    _id= 0
    jobCards= []
    type= 0
    job= ''
    aliasName= ''

class UserHeroVO(object):
	pass

class UserVO(object):
	pass
