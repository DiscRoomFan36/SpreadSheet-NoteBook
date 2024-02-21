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

def valid_format_methods(args, note_format_inputs):
	flag = True
	for input_method in note_format_inputs:
		unseen = True
		for method in INPUT_METHODS:
			if input_method == method.name:
				unseen = False
				break

		if unseen:
			print(f"Invalid Format(s) in ({args.FormatSheet}) WorkSheet: ({input_method}) is not a Input Method")
			flag = False
	return flag

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
	headers = [k for k in formats.keys()]

	DESCRIPTION_INDEX = 0
	METHOD_INDEX = 1

	methods = [item[METHOD_INDEX] for (_, item) in formats.items()]

	if not valid_format_methods(args, methods): exit(1)

	TOP_LEFT_CELL = all_formatting[0][0]

	kwargs: dict = KWARGS.copy()
	kwargs[METHOD_LIST] = [f"{TOP_LEFT_CELL}"]

	# TODO: Maybe remove limit at some point
	COUNTER_LIMIT = 10

	index = 0
	while (len(kwargs[METHOD_LIST]) > 0):
		if DEBUG: print(f"current: {kwargs[METHOD_LIST][0]}, kwargs: {kwargs}")

		name = kwargs[METHOD_LIST].pop(0)
		method = get_method(formats[name][METHOD_INDEX])
		args = formats[name]

		method.display(name, *args, **kwargs)
		output = method.Preform_Method(name, *args, **kwargs)
		if output != None: kwargs[MEMORY][name] = output
		
		kwargs[COUNTER].append(kwargs[COUNTER].pop() + 1)
		if kwargs[COUNTER][0] > COUNTER_LIMIT:
			print("Counter Limit Exceeded")
			break

	if len(kwargs[WORKSHEET]) == 0:
		print("No Sheet Supplied, no output")
		exit(0)

	try:
		worksheet = sh.worksheet(kwargs[WORKSHEET][-1])
	except gspread.WorksheetNotFound:
		print("Error: NoteBook Sheet Not Found")
		exit(1)

	headers = [f'{x}' for x in worksheet.row_values(1)] # header names
	new_row = [kwargs[MEMORY].get(name, "") for name in headers]

	if len([r for r in new_row if r != ""]) > 0:
		worksheet.append_row(new_row, gspread.worksheet.ValueInputOption.user_entered)
		print("Successfully added to Spreadsheet")	

	print("Finished!")
