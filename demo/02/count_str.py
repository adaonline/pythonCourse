#!/usr/bin/env python3
def char_count(str):
	charlist=set(str)
	for char in charlist:
		print(char,str.count(char))
if __name__=='__main__':
	s=input("enter your str:")
	char_count(s)
