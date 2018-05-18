#!/usr/bin/env  python3
import sys

try:
    alldict={}
    for arg in sys.argv[1:]:
        id_num=arg.split(":")

        if alldict.get(int(id_num[0])) is not None:
            raise ValueError()
        else:
            num=int(id_num[1])
            if num<0:
                raise ValueError()
            insur=num-num*0.165-3500
            result=0
            if insur<0:
                result=0
            elif insur<=1500:
                result=insur*0.03-0
            elif insur>1500 and insur<=4500:
                result=insur*0.1-105
            elif insur>4500 and insur<=9000:
                result=insur*0.2-555
            elif insur>9000 and insur<=35000:
                result=insur*0.25-1005
            elif insur>35000 and insur<=55000:
                result=insur*0.3-2755
            elif insur>55000 and insur<=80000:
                result=insur*0.35-5505
            elif insur>80000:
                result=insur*0.4-13505
            alldict[int(id_num[0])]=num-num*0.165-result
    for key,value in alldict.items():
        print("{}:{:.2f}".format(key,value))
except:
	print("Parameter Error")
