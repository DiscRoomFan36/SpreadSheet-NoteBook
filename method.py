from abc import ABCMeta, abstractmethod

class Method(metaclass=ABCMeta):
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
