#!/usr/bin/env python3
from multiprocessing import Process,Queue
queue=Queue(maxsize=10)
def f1(q):
    q.put("hello")
def f2(q):
    data=q.get()
    print(data)
def main():
    Process(target=f1,args=(queue,)).start()
    Process(target=f2,args=(queue,)).start()

if __name__=='__main__':
    main()
