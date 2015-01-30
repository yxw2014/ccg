# -*- coding: utf-8 -*-

from  django.http import HttpResponse
from  CardModel import CardModel
import json

from vo import *
from amf.base import Base

class CardService(Base):

	@classmethod
	def getAllCards(self, params= None):
		card = CardModel()
		ret= card.getAllCards()
		obj= CardVO()
		ret= makeVo(ret, obj)
		return ret



