#!/usr/bin/env python3
def char_count(str):
	chardict={}
	charlist=set(str)
	for char in str:
		num=chardict.get(char)
		if num is None:
			chardict[char]=1
		else:
			chardict[char]=num+1
	print(chardict)
if __name__=='__main__':
	s=input("enter your str:")
	char_count(s)
