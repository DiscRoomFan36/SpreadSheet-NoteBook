#!/bin/python3

import importlib, inspect, os

from method import Method, QuietMethod

METHOD_FOLDER = "methods"

def get_all_methods() -> list[Method]:
	methods = []

	for x in os.listdir(METHOD_FOLDER):
		if not x.endswith(".py"):
			continue

		module_name = f"{METHOD_FOLDER}.{x[:-3]}"
		for _, cls in inspect.getmembers(importlib.import_module(module_name), inspect.isclass):
			if issubclass(cls, Method) and cls != Method and cls != QuietMethod:
				methods.append(cls())
	
	return methods

INPUT_METHODS = get_all_methods()

if __name__ == "__main__":
	for m in get_all_methods():
		print(m.name)