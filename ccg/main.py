# -*- coding: utf-8 -*-

from django.http import HttpResponse
from  CardModel import CardModel
from  HeroModel import HeroModel
import json

from base import Base

class Main(Base):
	@classmethod
	def getAllCards(self, request):
		card = CardModel()
		a= card.getAllCards()
		
		return HttpResponse(json.dumps(a))

	@classmethod
	def getRandCards(self, request):
		#card = CardModel()
		#a= card.getCardsByRand(1)
		a= CardModel.getCardsByRand(2)
		
		return HttpResponse(json.dumps(a))

	@classmethod
	def getRandCardsById(self, request):
		#card = CardModel()
		#a= card.getCardsByRand(1)
		a= CardModel.getCardsById(27)
		
		return HttpResponse(json.dumps(a))

	@classmethod
	def getAllHeros(self, request):
		hero = HeroModel()
		a= hero.getAllHeros()
		
		return HttpResponse(json.dumps(a))

	@classmethod
	def getAllSystemAndUserHeros(self, request):
		hero = HeroModel()
		ret= hero.getAllSystemAndUserHeros('111')
		return HttpResponse(json.dumps(ret))
	
	@classmethod
	def getSystemOrUserHerosById(self, request):
		hero = HeroModel()
		ret= hero.getSystemOrUserHerosById('51', 1386157989)
		return HttpResponse(json.dumps(ret))

	@classmethod
	def getRandHeros(self, request):
		hero = HeroModel()
		a= hero.getAllHerosByRand(2)
		
		return HttpResponse(json.dumps(a))



