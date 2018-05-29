#!/usr/bin/env python3
import sys
import getopt
import configparser
from datetime import date,datetime
from multiprocessing import Process,Queue
class Config():
    def __init__(self):
        global args
        self._config={}
        a=args.getParam("-c")
        b=""
        if "-C" in args.param.keys():
            b=args.getParam("-C")
        parser = configparser.ConfigParser()
        parser.read(a)
        if b=="":
            for key,value in paeset.items("DEFAULT"):
                self._config[key.strip()]=float(value.strip())
        else:
            for key,value in parser.items(b.upper()):
                print(key,value)
                self._config[key.strip()]=float(value.strip())
    def get_config(self,param):
        return self._config.get(param)
    def getRemoveconfig(self):
        return self._config["YangLao".lower()]+self._config["YiLiao".lower()]+self._config["ShiYe".lower()]+self._config["GongShang".lower()]+self._config["ShengYu".lower()]+self._config["GongJiJin".lower()]
def init(queue):
    global args
    data={}
    with open(args.getParam("-d"),'r') as file:
        for line in file:
            id_data=line.split(",")
            data[id_data[0].strip()]=int(id_data[1].strip())
    queue.put(data)
def calculator(queue):
    global config
    data=queue.get()
    #print(data)
    result={}
    for key,value in data.items():
        a=[]
        if value<0:
            raise ValueError()
        else:
            shebao=0
            a.append(value)
            if value<int(config.get_config("JiShuL".lower())):
                shebao=int(config.get_config("JiShuL".lower()))*config.getRemoveconfig()
                a.append(shebao)
            elif value>int(config.get_config("JiShuH".lower())):
                shebao=int(config.get_config("JiShuH".lower()))*config.getRemoveconfig()
                a.append(shebao)
            else:
                shebao=value*config.getRemoveconfig()
                a.append(shebao)
            value=value-shebao
            topay=value
            if topay<3500:
                a.append(0)
                a.append(value)
            elif topay>3500:
                myup=topay-3500
                #print(a)
                #print(myup)
                #print(value)
                if myup<=1500:
                    rr=float(myup*0.03-0)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>1500 and myup<=4500:
                    rr=float(myup*0.1-105)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>4500 and myup<=9000:
                    rr=float(myup*0.2-555)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>9000 and myup<=35000:
                    rr=float(myup*0.25-1005)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>35000 and myup<=55000:
                    rr=float(myup*0.3-2755)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>55000 and myup<=80000:
                    rr=float(myup*0.35-5505)
                    a.append(rr)
                    a.append(value-rr)
                elif myup>80000:
                    rr=float(myup*0.45-13505)
                    a.append(rr)
                    a.append(value-rr)
        result[key]=a
    queue.put(result)	
def outTofile(queue):
    global args
    result=queue.get()
    with open(args.getParam("-o"),'w') as file:
        for key,value in result.items():
            outstr=key+","
            for num in value:
                i=value.index(num)
                if i==0:
                    outstr+=str(num)+","
                else: 
                    outstr+="{:.2f}".format(num)+","
            t=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
            outstr=outstr[0:-1]
            file.write(outstr+"\n")
class Args():
    def __init__(self):
        self.param={}		
        opts,args=getopt.getopt(sys.argv[1:],"C:c:d:o:",[])
        for o,a in opts:
            self.param[o]=a
    def getParam(self,ask):
        return self.param.get(ask)
def main():
    queue=Queue(maxsize=10)
    #args=Args()
    #config=Config()
    
    p1=Process(target=init,args=(queue,))
    p1.start()
    p1.join()
    p2=Process(target=calculator,args=(queue,))
    p2.start()
    p2.join()
    p3=Process(target=outTofile,args=(queue,))
    p3.start()
    p3.join()
if __name__=="__main__":
    try:
        args=Args()
        config=Config()
        main()
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)


