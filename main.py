from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://build-a-blog:bepassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] =True
db = SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120))
    body=db.Column(db.String(120))
    def __init__(self,title,body):
        self.title=title
        self.body=body
@app.route('/add', methods=['POST','GET'])
def add_post():
    if request.method =='POST':
        post_title=request.form['title']
        post_blog=request.form['new-blog']
        # error_title=''
        # error_body=''
        new_blog=Blog(post_title,post_blog)
        db.session.add(new_blog)
        db.session.commit()
    # if int(len(post_title)) <= 0:
    #     error_title='Please insert the title of your new post'
    #     post_title=''
    # elif int(len(post_blog)) <= 0:
    #     error_boby='Please insert the body of  your new post'
    #     post_blog=''
    # if not error_title and not error_body and not post_title == '' and not post_blog == "":
    #     return redirect('/blog')
    posts=Blog.query.all()
    return render_template('newpost.html', posts=posts)#,error_title=error_title,error_boby=error_boby,
    #post_title=post_title,post_blog=post_blog)
@app.route('/blog')
def blog():
    blog_posts=  Blog.query.all()
    return render_template('blog.html',blog_posts=blog_posts)
@app.route('/')
def index():
    return render_template('newpost.html')
if __name__=='__main__':
    app.run()
