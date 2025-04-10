#!/bin/python3

"""
This project is supposed to help create a notebook
for my progress thought the game "Void Stranger"
"""

import gspread

from method import KWARGS, MEMORY, METHOD_LIST, COUNTER, WORKSHEET
from get_methods import INPUT_METHODS

def get_method(input_method):
	for method in INPUT_METHODS:
		if method.name == input_method:
			return method
	raise KeyError

def connect(args):
	gc = gspread.service_account(filename='credentials.json')
	try:
		sh = gc.open(args.SpreadSheet)
	except gspread.SpreadsheetNotFound:
		print("Error: Spreadsheet Not Found")
		exit(1)

	try:
		formatSheet = sh.worksheet(args.FormatSheet)
	except gspread.WorksheetNotFound:
		print("Error: Format Sheet Not Found")
		exit(1)

	return (sh, formatSheet)

def list_of_list_to_dict_of_array(list_of_list: list[list]):
	headers, rest = list_of_list[0], list_of_list[1:]
	dictionary: dict[str, list[str]] = {}
	for header in headers:
		dictionary[header] = []
	
	for line in rest:
		for i in range(len(line)):
			if i < len(headers) and headers[i] in dictionary:
				dictionary[headers[i]].append(line[i])

	return dictionary


DESCRIPTION_INDEX = 0
METHOD_INDEX = 1
import copy
class Engine():

	program = None
	headers = None
	input_methods = INPUT_METHODS
	init_kwargs = None
	kwargs = None

	@staticmethod
	def valid_format_methods(method_inputs):
		flag = True
		for input_method in method_inputs:
			unseen = True
			for method in INPUT_METHODS:
				if input_method == method.name:
					unseen = False
					break
			if unseen:
				print(f"Invalid Format(s) in Program: ({input_method}) is not a Input Method")
				flag = False
		return flag

	def __init__(self, program) -> None:
		self.program = program
		self.headers = [k for k in self.program.keys()]

		methods = [item[METHOD_INDEX] for (_, item) in program.items()]

		if not Engine.valid_format_methods(methods): exit(1)

		TOP_LEFT_CELL = all_formatting[0][0]

		self.init_kwargs = KWARGS.copy()
		self.init_kwargs[METHOD_LIST] = [f"{TOP_LEFT_CELL}"]

		self.kwargs = copy.deepcopy(self.init_kwargs)

	def run(self, step_limit: int | None = None):
		while (len(self.kwargs[METHOD_LIST]) > 0):
			if DEBUG: print(f"current: {self.kwargs[METHOD_LIST][0]}, kwargs: {self.kwargs}")

			name = self.kwargs[METHOD_LIST].pop(0)
			method = get_method(self.program[name][METHOD_INDEX])
			args = self.program[name]

			method.display(name, *args, **self.kwargs)
			output = method.Preform_Method(name, *args, **self.kwargs)
			if output != None: self.kwargs[MEMORY][name] = output
			
			self.kwargs[COUNTER].append(self.kwargs[COUNTER].pop() + 1)
			if step_limit is not None and self.kwargs[COUNTER][0] > step_limit:
				print("Counter Limit Exceeded")
				break
	def reset(self):
		self.kwargs = copy.deepcopy(self.init_kwargs)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Interact with a Spreadsheet NoteBook")
	parser.add_argument("SpreadSheet", help="The name of the Spreadsheet to access")
	parser.add_argument("-f", "--FormatSheet", help="The name of the format sheet in the SpreadSheet", default="Format")
	parser.add_argument("-d", "--Debug", help="Provides more debug information", action='store_true')
	args = parser.parse_args()

	DEBUG = args.Debug

	print("Welcome to the SpreadSheet NoteBook app")
	sh, formatSheet = connect(args)
	print("Successfully Connected!")

	all_formatting = formatSheet.get_all_values()
	formats = list_of_list_to_dict_of_array(all_formatting)

	# TODO: Maybe remove limit at some point
	COUNTER_LIMIT = 100000
	engine = Engine(formats)

	while True:
		engine.run(COUNTER_LIMIT)
		kwargs = engine.kwargs

		if len(kwargs[WORKSHEET]) == 0:
			print("No Sheet Supplied, no output")
		else:
			try:
				worksheet = sh.worksheet(kwargs[WORKSHEET][-1])
			except gspread.WorksheetNotFound:
				print("Error: NoteBook Sheet Not Found")
				exit(1)

			headers = [f'{x}' for x in worksheet.row_values(1)] # header names
			new_row = [kwargs[MEMORY].get(name, "") for name in headers]

			if len([r for r in new_row if r != ""]) > 0:
				worksheet.append_row(new_row, gspread.worksheet.ValueInputOption.user_entered)
				print("\nSuccessfully added to Spreadsheet")	

		print("Finished!")

		answer = input("\n\n\nDo you want to do that again? (Yes/No)?")
		if 'y' not in answer.lower():
			break

		engine.reset()
		print("\n", end="")


