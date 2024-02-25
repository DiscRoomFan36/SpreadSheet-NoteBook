from abc import ABCMeta, abstractmethod

"""key word arg names"""

# TODO: Decide wether needed
# PROGRAM = "Program"
# """The Program currently running"""

MEMORY = "Memory"
"""Dictionary of the outputs from methods. dict[str, str]"""

METHOD_LIST = "Method List"
"""List of methods to perform and their order. list[str]"""

COUNTER = "Counter"
"""The number of methods that have happened. list[int]"""

WORKSHEET = "Worksheet"
"""The Worksheet that the final output will end up in"""


KWARGS = {
	# PROGRAM: {},
	MEMORY: {},
	METHOD_LIST: [],
	COUNTER: [0],
	WORKSHEET: [],
}

class Method(metaclass=ABCMeta):
	"""
		Abstract class that gets some information from the user and return a string to put in a spreadsheet.

		Methods:
			@property name -> str

			@staticmethod Preform_Method -> str

			display -> None
	"""

	@property
	@abstractmethod
	def name(self) -> str:
		"""Name of the class"""
		pass

	def display(self, name: str, description: str, method: str, *args, **kwargs):
		"""display message to the terminal before the Preform_Method is called"""
		print(f"{kwargs[COUNTER][0]}: {name}, {description}")

	@abstractmethod
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs) -> str | None:
		"""Gets Some Input from the user and returns a string to put in the spreadsheet
		
		:param name str: name of colum
		:param description str: description of input
		:param method str: the method to use to fill this colum

		:param args: additional arguments
		
		:return str | None: a string to put in the colum or None
		
		"""
		pass


class QuietMethod(Method):
	"""A Quieter Method"""
	def display(*args, **kwargs):
		pass

def trim_args(args):
	return [arg for arg in args if arg != ""]