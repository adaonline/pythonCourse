#!/usr/bin/env python3
import threading
def hello(name):
    print('child thread: {}'.format(threading.get_ident()))
    print('hello '+name)
def main():
    t=threading.Thread(target=hello,args=('you',))
    t.start()
    t.join()
    print('main thread:{}'.format(threading.get_ident()))
if __name__=='__main__':
    main()
