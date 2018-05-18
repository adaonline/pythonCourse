#!/usr/bin/env python3
import json
courses={1:'linux',2:'vim',3:'git'}
#print(json.dumps(courses))
with open('courses.json','w') as file:
	file.write(json.dumps(courses))
with open('courses.json','r') as file:
	new_courses=json.loads(file.read())
	print(new_courses)
