#! /usr/bin/python3

import sys

if len(argv) < 2:
    raise Exception("Require a tree file as argument")

f = open(argv[-1], "r")

escape = False
read_br_length = False

while True:
    char = f.read(1)
    if !escape and char == '(':
	print('{')
	print('children=['
    elif !escape and char == ')':
	print(']')
	print('}')
    elif !escape and char == ',':
	print(',', end='')
    elif !escape and char == ':':
	read_br_length = True
