from abc import ABCMeta, abstractmethod

class Method(metaclass=ABCMeta):
	"""
		Abstract class that gets some information from the user and return a string to put in a spreadsheet.

		Methods:
			@property name -> str
			
			@staticmethod Preform_Method -> str
	"""

	@property
	@abstractmethod
	def name(self) -> str:
		"""Name of the class"""
		pass

	@staticmethod
	@abstractmethod
	def Preform_Method() -> str:
		"""Gets Some Input from the user and returns a string to put in the spreadsheet"""
		pass
