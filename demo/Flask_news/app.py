from flask import Flask
from flask import render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    created_time=db.Column(db.DateTime())
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    content=db.Column(db.Text)
    #??????????
    category=db.relationship('Category',backref=db.backref('posts',lazy='dynamic'))
    def __init__(self,title,created_time,category,content):
        self.title=title
        self.created_time=created_time
        self.content=content
        self.category=category
    def __repr__(self):
        return '<title:%r>' % self.title
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
@app.route('/files/<filename>')
def file(filename):
    f = File.query.filter_by(id=int(filename)).first()
    if not f:
        abort(404)
    ty=Category.query.filter_by(id=f.category_id)
    return render_template('file.html', f=f,ty=ty)                            
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__=="__main__":
    app.run()


