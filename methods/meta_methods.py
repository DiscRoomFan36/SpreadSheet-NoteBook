from method import Method, QuietMethod, METHOD_LIST, WORKSHEET, MEMORY, trim_args

class Setup(QuietMethod):
	@property
	def name(self):
		return "Setup"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		if args[0] != "":
			kwargs[WORKSHEET].append(args[0])

		args = trim_args(args[1:])
		for (i, arg) in enumerate(args):
			kwargs[METHOD_LIST].insert(i, arg)

class Append(QuietMethod):
	@property
	def name(self):
		return "Append"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = trim_args(args)
		for arg in args:
			kwargs[METHOD_LIST].append(arg)

class Clear(QuietMethod):
	@property
	def name(self):
		return "Clear"

	def Preform_Method(*args, **kwargs):
		kwargs[METHOD_LIST].clear()
		args = trim_args(args)
		for arg in args:
			kwargs[METHOD_LIST].append(arg)


def get_input(enter_text: str, validation, error_message="Invalid, Try Again"):
	string = input(enter_text)
	while not validation(string):
		print(error_message)
		string = input(enter_text)
	return string

class Select(Method):
	@property
	def name(self):
		return "Select"
	
	def Preform_Method(self, name, description, method, *args, **kwargs):
		args = trim_args(args)

		print(f"Select an option from 1-{len(args)}")
		for (i, arg) in enumerate(args):
			print(f"{i + 1}: {arg}")
		
		def validate(s: str):
			if not s.isdecimal(): return False
			n = int(s)
			return 1 <= n <= len(args)


		i = int(get_input("Enter Selection: ", validate))
		kwargs[METHOD_LIST].insert(0, args[i - 1])

class Optional(Method):
	@property
	def name(self):
		return "Optional"
	
	def Preform_Method(self, name, description, method, optional, *args, **kwargs):
		selected = input("Yes/No?: ")
		if "y" in selected.lower():
			kwargs[METHOD_LIST].insert(0, optional)
		elif len(args) > 0 and args[0] != "":
			kwargs[MEMORY][optional] = args[0]

class SetOutput(QuietMethod):
	@property
	def name(self):
		return "Set Output"
	
	# TODO: Make more robust in case of setting some values to ""
	def Preform_Method(self, name, description, method, *args, **kwargs):
		pairs = [(args[i-1], args[i]) for i in range(1, len(args), 2)]

		for (name, value) in pairs:
			kwargs[MEMORY][name] = value

