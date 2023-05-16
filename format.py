#!/bin/env python

import os
import sys
import re

typesRegExp = {
	r': list\[.*?\]': "",
	r': list': "",
	r'-> list\[.*?\]': "",
	r'-> list': "",
	r': dict': "",
	r'-> dict': "",
	r': int': "",
	r': float': "",
	r': str': "",
	r'-> int': "",
	r'-> float': "",
	r'-> str': "",
	r': Temps': "",
	r'-> Temps': "",
	r' {4}': "\t"
}

def formatFile(filepath: str) -> None:
	if not os.path.exists(filepath):
		print("Le fichier en question n'existe pas:", filepath, file=sys.stderr)
		sys.exit(2)

	if os.path.isdir(filepath):
		files = os.listdir(filepath)
		for file in files:
			formatFile(filepath + "/" + file)

	else:
		if (
			len(filepath) > 3
			and filepath[-1] == "y"
			and filepath[-2] == "p"
			and filepath[-3] == "."
		):
			print("format", filepath)
			file = open(filepath, "r")

			lines = file.readlines()
			file.close()

			for i in range(len(lines)):
				# lines[i] = lines[i].replace("	   ", "\t")
				for regexp in typesRegExp:
					lines[i] = re.sub(regexp, typesRegExp[regexp], lines[i])

			file = open(filepath, "w")
			file.writelines(lines)


args = sys.argv
if len(args) < 2 or type(args[1]) != str:
	print("Passez un string en argument", file=sys.stderr)
	sys.exit(1)


filepath = args[1]
formatFile(filepath)
