from method import Method

from typing import Callable

def get_input(enter_text: str, validation: Callable[[str], bool], error_message="Invalid, Try Again"):
	string = input(enter_text)
	while not validation(string):
		print(error_message)
		string = input(enter_text)
	return string

class String(Method):
	@property
	def name(self):
		return "String"
	
	@staticmethod
	def Preform_Method():
		return get_input("Enter: ", lambda _: True)

class Number(Method):
	@property
	def name(self):
		return "Number"
	
	@staticmethod
	def Preform_Method():
		return get_input("Enter a number: ", lambda x: x.isdigit(), "Invalid Number")


class Movement(Method):
	@property
	def name(self):
		return "Movement"
	
	@staticmethod
	def Preform_Method():
		def valid(s: str):
			s = s.lower()
			for c in s:
				if c not in "wasd ":
					return False
			return True
		directions = get_input("Enter Directions: ", valid, "WASD and <SPACE> only")
		directions = directions.upper()

		directions.replace(" ", "( )")

		return directions
