from method import Method, METHOD_LIST, COUNTER

NAME = "Setup"
class Setup(Method):
	@property
	def name(self):
		return NAME
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		# kwargs[COUNTER].append(kwargs[COUNTER].pop() + 100)

		for arg in args:
			kwargs[METHOD_LIST].append(arg)
