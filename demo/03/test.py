#!/usr/bin/env python3
filename=input("enter the file name:")
with open(filename) as file:
	count=0
	for line in file:
		count+=1
		print(line)
	print('lines:',count)
