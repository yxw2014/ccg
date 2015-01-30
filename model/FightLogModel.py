# -*- coding: utf-8 -*-
import sys
import os
import random
import time
import json
from pprint import pprint
from errors import err
#<class 'model.BaseModel.BaseModel'>
from model.BaseModel import BaseModel
from model.CardModel import CardModel
from model.RoomModel import RoomModel
from model.SkillModel import SkillModel
from pymongo.errors import AutoReconnect
						
class FightLogMode(BaseModel): 
	def __init__(self): 
		super(FightLogMode, self).__init__()			
