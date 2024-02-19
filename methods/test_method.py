from method import Method

class New_Thing(Method):
	@property
	def name(self):
		return "New_Thing"
	
	@staticmethod
	def Preform_Method():
		return "Hello"