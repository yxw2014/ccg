# -*- coding: utf-8 -*-
import sys
sys.path.append('./service')
sys.path.append('./lib')
from data import data
class AAA:
	def __init__(self): 
		#super(FightService, self).__init__()
		print 'self.data= data'
		self.data= data		
		#self.data= {}	
	#aaa= 'asdf'
	def f(self):
		self.data['s']= 's';
	def ff(self):
		
		print self.data['s']
a= AAA()
print a
a.f()
#print a.aaa

b= AAA()
print b
b.ff()
print data['s']
#print b.aaa
