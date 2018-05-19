# 多进程与多线程
### 多进程
multi.py  ---multiprocessing下的 Process 类的多进程操作
pipe_test.py ---multiprocessing 模块提供了 Pipe支持进程间通信
queue_test.py ---multiprocessing 模块提供了 queue支持进程间通信
lock_test.py  ---进程同步问题，用一个lock防止并发问题
pool_test.py  ---进程池的应用，池内有进程，就去处理，没有就等待执行完放回
### 多线程
threading_moudle_test.py ---threading多线程支持，与多进程multiprocessing很类似