from method import QuietMethod, METHOD_LIST, MEMORY, POINTER_MEMORY

class PointerRight(QuietMethod):
	@property
	def name(self):
		return "PointerRight"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = [arg for arg in args if arg != ""]
		for arg in args:
			kwargs[POINTER_MEMORY][arg] = kwargs[POINTER_MEMORY].get(arg, 0) + 1

class PointerLeft(QuietMethod):
	@property
	def name(self):
		return "PointerLeft"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = [arg for arg in args if arg != ""]
		for arg in args:
			kwargs[POINTER_MEMORY][arg] = kwargs[POINTER_MEMORY].get(arg, 0) - 1

class IncPointer(QuietMethod):
	@property
	def name(self):
		return "IncPointer"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = [arg for arg in args if arg != ""]
		for arg in args:
			kwargs[MEMORY][kwargs[POINTER_MEMORY][arg]] = kwargs[MEMORY].get(kwargs[POINTER_MEMORY][arg], 0) + 1
	
class DecPointer(QuietMethod):
	@property
	def name(self):
		return "DecPointer"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		assert method == self.name

		args = [arg for arg in args if arg != ""]
		for arg in args:
			kwargs[MEMORY][kwargs[POINTER_MEMORY][arg]] = kwargs[MEMORY].get(kwargs[POINTER_MEMORY][arg], 0) - 1

class JumpPointerZero(QuietMethod):
	@property
	def name(self):
		return "JumpPointerZero"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		flag = False
		args = [arg for arg in args if arg != ""]
		for arg in args:
			if kwargs[MEMORY].get(kwargs[POINTER_MEMORY][arg], 0) == 0:
				flag = True
		
		# TODO: figure out a way to do this? or maybe something else
		if flag:
			# remove methods until JumpPointerNonZero
			kwargs[METHOD_LIST]
		else:
			# Add the things until JumpPointerNonZero
			kwargs[MEMORY]["Jump Stack"] = []



class PrintPointer(QuietMethod):
	@property
	def name(self):
		return "PrintPointer"
	
	def display(*args, **kwargs):
		args = [arg for arg in args if arg != ""]
		for arg in args:
			a = kwargs[MEMORY].get(kwargs[POINTER_MEMORY][arg], 0)
			print(a)

	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs):
		pass




