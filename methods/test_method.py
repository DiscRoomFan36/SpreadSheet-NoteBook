from method import Method

class New_Thing(Method):
	@property
	def name(self):
		return "New_Thing"
	
	def Preform_Method(*args, **kwargs):
		return "Hello"