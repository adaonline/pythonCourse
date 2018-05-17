#!/usr/bin/env python3
import sys
try:
	num=int(sys.argv[1])
	if num<0:
		raise ValueError()
	neednum=num-3500;
	result=0
	if neednum<=1500:
		result=neednum*0.03-0
	elif neednum>1500 and neednum<4500:
		result=neednum*0.1-105
	elif neednum>4500 and neednum<=9000:
		result=neednum*0.2-555
	elif neednum>9000 and neednum<=35000:
		result=neednum*0.25-1005
	elif neednum>35000 and neednum<=55000:
		result=neednum*0.3-2755
	elif neednum>55000 and neednum<=80000:
		result=neednum*0.35-5505
	elif neednum>8000:	
		result=neednum*0.45-13505
	print(format(result,'.2f')) 
except ValueError:
	print("Parameter Error")

