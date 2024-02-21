from method import Method, METHOD_LIST, WORKSHEET

class Setup(Method):
	@property
	def name(self):
		return "Setup"
	
	def display(*args, **kwargs):
		pass
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		if args[0] != "":
			kwargs[WORKSHEET].append(args[0])

		args = [arg for arg in args[1:] if arg != ""]
		for (i, arg) in enumerate(args):
			kwargs[METHOD_LIST].insert(i, arg)

class Append(Method):
	@property
	def name(self):
		return "Append"
	
	def display(*args, **kwargs):
		pass
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = [arg for arg in args if arg != ""]
		for arg in args:
			kwargs[METHOD_LIST].append(arg)