from method import QuietMethod, METHOD_LIST, MEMORY, trim_args

class PointerRight(QuietMethod):
	@property
	def name(self):
		return "PointerRight"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = trim_args(args)
		for arg in args:
			# TODO: Deal with strings
			kwargs[MEMORY][arg] = kwargs[MEMORY].get(arg, 0) + 1

class PointerLeft(QuietMethod):
	@property
	def name(self):
		return "PointerLeft"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = trim_args(args)
		for arg in args:
			# TODO: Deal with strings
			kwargs[MEMORY][arg] = kwargs[MEMORY].get(arg, 0) - 1

class IncPointer(QuietMethod):
	@property
	def name(self):
		return "IncPointer"
	
	# TODO: change to AddPointer and add argument pairs
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = trim_args(args)
		for arg in args:
			kwargs[MEMORY][f"{arg}[{kwargs[MEMORY].get(arg, 0)}]"] = kwargs[MEMORY].get(f"{arg}[{kwargs[MEMORY].get(arg, 0)}]", 0) + 1
	
class DecPointer(QuietMethod):
	@property
	def name(self):
		return "DecPointer"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = trim_args(args)
		for arg in args:
			kwargs[MEMORY][f"{arg}[{kwargs[MEMORY].get(arg, 0)}]"] = kwargs[MEMORY].get(f"{arg}[{kwargs[MEMORY].get(arg, 0)}]", 0) - 1

JUMP_STACK = "Jump Stack"

class JumpPointerZero(QuietMethod):
	@property
	def name(self):
		return "JumpPointerZero"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		jump_to = args[0]

		args = trim_args(args[1:])

		flag = False
		for arg in args:
			if kwargs[MEMORY].get(f"{arg}[{kwargs[MEMORY].get(arg, 0)}]", 0) % 256 == 0:
				flag = True
		
		if flag:
			# remove methods until jump_to
			depth = 0
			while len(kwargs[METHOD_LIST]) > 0 and kwargs[METHOD_LIST][0] != jump_to and depth == 0:
				check_method = kwargs[METHOD_LIST].pop(0)
				if check_method == name: depth += 1
				if check_method == jump_to: depth -= 1
			kwargs[METHOD_LIST].pop(0)
		else:
			# Add the things until jump_to
			stack = []
			depth = 0
			for i in range(len(kwargs[METHOD_LIST])):
				if (kwargs[METHOD_LIST][i] == jump_to) and (depth == 0):
					break
				check_method = kwargs[METHOD_LIST][i]
				if check_method == name: depth += 1
				if check_method == jump_to: depth -= 1
				stack.append(kwargs[METHOD_LIST][i])

			stack.append(kwargs[METHOD_LIST][len(stack)])

			if JUMP_STACK not in kwargs[MEMORY]:
				kwargs[MEMORY][JUMP_STACK] = []
			kwargs[MEMORY][JUMP_STACK].append(stack)

class JumpPointerNonZero(QuietMethod):
	@property
	def name(self):
		return "JumpPointerNonZero"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		args = trim_args(args)

		flag = False
		for arg in args:
			if kwargs[MEMORY].get(f"{arg}[{kwargs[MEMORY].get(arg, 0)}]", 0) % 256 != 0:
				flag = True
		
		if flag:
			# jump back to prev
			for (i, name) in enumerate(kwargs[MEMORY][JUMP_STACK][-1]):
				kwargs[METHOD_LIST].insert(i, name)
		else:
			# Continue and clear jump stack
			kwargs[MEMORY][JUMP_STACK].pop()

class PrintPointer(QuietMethod):
	@property
	def name(self):
		return "PrintPointer"

	def Preform_Method(self, name, description, method, *args, **kwargs) -> str | None:
		args = trim_args(args)
		for arg in args:
			pointer = kwargs[MEMORY].get(f"{arg}[{kwargs[MEMORY].get(arg, 0)}]", 0)
			print(chr(pointer % 256), end="")
		
		pass

# '++>+++++[<+>-]++++++++[<++++++>-]<.
# '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
# '+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+.
	