from method import Method, METHOD_LIST, WORKSHEET

NAME = "Setup"
class Setup(Method):
	@property
	def name(self):
		return NAME
	
	def display(*args, **kwargs):
		pass
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		if args[0] != "":
			kwargs[WORKSHEET].append(args[0])

		args = [arg for arg in args[1:] if arg != ""]
		for (i, arg) in enumerate(args):
			kwargs[METHOD_LIST].insert(i, arg)
