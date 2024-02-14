"""
This project is supposed to help create a notebook
for my progress thought the game "Void Stranger"
"""

import gspread

def test():
	gc = gspread.service_account(filename='credentials.json')
	sh = gc.open_by_key("15DneN76Jgohv3YBvCDv_LMqBjNFubChwEn_l_cmjAmQ")
	worksheet = sh.worksheet('test')

	print("cell A1", worksheet.get('A1'))
	print("row values:", worksheet.row_values(1))
	print("col values:", worksheet.col_values(1))
	print("all values:", worksheet.get_all_values())
	print("cell A1:B4:", worksheet.get("A1:B4"))

	nums = [i + 20 for i in range(6)]
	worksheet.update([nums], "A1")
	worksheet.freeze(1)

	multi = "This is a multi line string\nits on two lines"
	multi2 = ["next", "test"]
	worksheet.append_row(["a", 1, "c", multi, "\n".join(multi2)])

import abc
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

		return directions

INPUT_METHODS: list[Method] = [
	String(),
	Movement(),
]

def get_method(input_method):
	for method in INPUT_METHODS:
		if method.name == input_method:
			return method
	raise KeyError

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Interact with a Spreadsheet NoteBook")
	parser.add_argument("SpreadSheet", help="The name of the Spreadsheet to access")
	parser.add_argument("NoteBook", help="The name of the workspace the note is in")
	parser.add_argument("-f", "--FormatSheet", help="The name of the format sheet in the SpreadSheet", default="Format")
	args = parser.parse_args()

	print("Welcome to the SpreadSheet NoteBook app")

	gc = gspread.service_account(filename='credentials.json')
	try:
		sh = gc.open(args.SpreadSheet)
	except gspread.SpreadsheetNotFound:
		print("Error: Spreadsheet Not Found")
		exit(1)

	try:
		noteBook = sh.worksheet(args.NoteBook)
	except gspread.WorksheetNotFound:
		print("Error: NoteBook Sheet Not Found")
		exit(1)

	try:
		formatSheet = sh.worksheet(args.FormatSheet)
	except gspread.WorksheetNotFound:
		print("Error: Format Sheet Not Found")
		exit(1)

	print("Successfully Connected!")

	note_format_names = formatSheet.row_values(1)
	note_format_descriptions = formatSheet.row_values(2)
	note_format_inputs = formatSheet.row_values(3)

	note_format = zip(note_format_names, note_format_inputs, note_format_descriptions)

	flag = False
	for input_method in note_format_inputs:
		unseen = True
		for method in INPUT_METHODS:
			if input_method == method.name:
				unseen = False
				break

		if unseen:
			print(f"Invalid Format(s) in ({args.FormatSheet}) WorkSheet: ({input_method}) is not a Input Method")
			flag = True
	if flag: exit(1)

	values = []

	for (i, (name, input_method, description)) in enumerate(note_format):
		print(f"{i}: {name}, {description}")

		method = get_method(input_method)

		output = method.Preform_Method()

		values.append(output)

	noteBook.append_row(values)

	
