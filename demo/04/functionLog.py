#!/usr/bin/env python3
from datetime import datetime
from functools import wraps
def log(func):
	@wraps(func)
	def decorator(*args,**kwargs):
		print('function' + func.__name__+'has been called at'+datetime.now().strftime('%y-%m-%d %H:%M:%S'))
		return func(*args,**kwargs)
	return decorator

@log
def add(x,y):
	return x+y

add(1,2)
