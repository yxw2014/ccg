# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from errors import err
from  BaseService import BaseService

class TestService(BaseService): 
		
	def __init__(self): 
		super(TestService, self).__init__()		
		
	
	def testMethod(self, params):
		self.result["data"]= {"test":10086, "info": {"room_id":451377, "score":[3,5,6,8]}}
		return self.result, None