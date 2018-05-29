 # 一个个人所得税计算器

./calculator.py -c /home/shiyanlou/test.cfg -d /home/shiyanlou/user.csv -o /tmp/gongzi.csv

获取cfg中的信息，还有user中的信息，计算出个人税，保存在gongzi文件里
主要考察，类的操作，基本语法，文件读取等等

calculator_tread则加了线程，线程间共享数据