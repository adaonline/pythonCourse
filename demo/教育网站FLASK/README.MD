#在线教育网站
##索引
1. 初始的一个基础版本吧
2. 搭建正式的一个框架(目录下有一些内容讲解)
3. 增加用户页面


一些初始化操作
```
sudo pip3 install flask flask-sqlalchemy mysqlclient #安装flask数据库连接
sudo service mysql start
mysql -uroot
create database simpledu; #创建数据库
```
配置环境变量：

```
export FLASK_APP=app.py
export FLASK_DEBUG=1

```
进入 flask shell，创建几条测试数据：
```
>>> from app import db, User, Course
>>> db.create_all()
>>> user = User(username='admin')
>>> course1 = Course(name='python course', author=user)
>>> course2 = Course(name='flask course', author=user)
>>> db.session.add(user)
>>> db.session.add(course1)
>>> db.session.add(course2)
>>> db.session.commit()
```