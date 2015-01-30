# -*- coding: utf-8 -*-

import sys
import os
from config import config
from errors import err

class BaseService(object):
	log= None
	mongodb= None
	redis= None
	server_id= None	
	
	#result= {"error":{"code": 0, "msg": ''}, "data":{}, "push_uuid":None, "push_result":None}
	#push_result= {"error":{"code": 0, "msg": ''}, "data":{}}
	#push_result= {"uuid":None, "service":"fight", "method":"push", "params":{}}
	
	def __init__(self): 
		self.result= {"error":{"code": 0, "msg": ''}, "data":{}, "service":"main", "method":"error"}
		self.push_result= {"uuid":None, "service":"main", "method":"error", "params":{}}
		