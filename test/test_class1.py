from test_class0 import A

class B(A):
	def __init__(self): 
		#super(B, self).__init__()

		print self.aaa
		self.aaa= '456'
		print self.aaa
		pass
	def bbb(self): 
		#super(B, self).__init__()

		print self.aaa


    