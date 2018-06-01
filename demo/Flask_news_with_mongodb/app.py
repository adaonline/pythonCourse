from flask import Flask
from flask import render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import *
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)
mongo=MongoClient('127.0.0.1',27017).shiyanlou

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    created_time=db.Column(db.DateTime())
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    content=db.Column(db.Text)
    category=db.relationship('Category',backref=db.backref('posts',lazy='dynamic'))
    def __init__(self,title,created_time,category,content):
        self.title=title
        self.created_time=created_time
        self.content=content
        self.category=category
    def __repr__(self):
        return '<title:%r>' % self.title
    def add_tag(self,tag_name):
        file_item=mongo.files.find_one({'file_id':self.id})
        if file_item:
            tags=file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id':self.id},{'$set':{'tags':tags}})
        else:
            tags=[tag_name]
            mongo.files.insert_one({'file_id':self.id,'tags':tags})
        return tags
    def remove_tag(self,tag_name):
        file_item=mongo.files.find_one({'file_id':self.id})
        if file_item:
            tags=file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags=tags
            except ValueError:
                return tags
            mongo.files.update_one({'file_id':self.id},{'$set':{'tags':new_tags}})
            return new_tags
        return []
    @property
    def tags(self):
        file_item=mongo.files.find_one({'file_id':self.id})
        if file_item:
            print(file_item)
            return file_item['tags']
        else:
            return []
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    def __init__(self,category):
        self.name=category
        def __repr__(self):
            return '<name:%r>' % self.name                              
@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)                   
@app.route('/files/<int:file_id>')
def file(file_id):
    f = File.query.filter_by(id=file_id).first_or_404()
    return render_template('file.html', f=f)                            
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

def insert_datas():
    db.create_all()
    java=Category('Java')
    python=Category("Python")
    file1=File('Hello Java',datetime.utcnow(),java,'File Content - Java is cool!')
    file2=File('Hello Python',datetime.utcnow(),python,'File content - Pyhton is cool')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('python')
    file2.add_tag('tech')
if __name__=="__main__":
    app.run()


