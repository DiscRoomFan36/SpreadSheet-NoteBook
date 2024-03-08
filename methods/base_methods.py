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
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs) -> str | None:
		args = [arg for arg in args if arg != ""]
		if len(args) == 0:
			return get_input("Enter: ", lambda _: True)
		
		lines = []
		for arg in args:
			# TODO: if arg is string, use pointer
			lines.append(get_input(f"Enter ({arg}): ", lambda s: len(s) < int(arg), "String to long, Try Again."))
		return "\n".join(lines)


class Number(Method):
	@property
	def name(self):
		return "Number"
	
	def Preform_Method(*args, **kwargs):
		return get_input("Enter a number: ", lambda x: x.isdigit(), "Invalid Number")


class Movement(Method):
	@property
	def name(self):
		return "Movement"
	
	def Preform_Method(*args, **kwargs):
		def valid(s: str):
			s = s.lower()
			for c in s:
				if c not in "wasd ":
					return False
			return True
		directions = get_input("Enter Directions: ", valid, "WASD and <SPACE> only")
		directions = directions.upper()

		directions = directions.replace(" ", "*")

		return directions

class Dialog(Method):
	@property
	def name(self):
		return "Dialog"
	
	def Preform_Method(self, *args, **kwargs):
		log = []
		print("Enter in the lines of dialog. type 'END()' to quit.\n")
		while True:
			next_dialog = input()
			if next_dialog == "END()":
				break
			log.append(next_dialog)
		
		while log[-1] == "":
			log.pop()
		
		return log



