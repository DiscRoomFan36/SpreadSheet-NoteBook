"""
This project is supposed to help create a notebook
for my progress thought the game "Void Stranger"
"""

import gspread

from get_methods import get_all_methods

INPUT_METHODS = get_all_methods()

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

	
