#!/usr/bin/env python3
import pickle
courses={1:'linuc',2:'vim',3:'git'}
with open('courses.data','wb') as file:
	pickle.dump(courses,file)
with open('courses.data','rb') as file:
	new_courses=pickle.load(file)
	print(new_courses)
