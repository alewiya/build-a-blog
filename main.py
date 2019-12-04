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
@app.route('/newpost', methods=['POST','GET'])
def add_post():
    error_title=''
    error_body=''
    if request.method =='POST':
        post_title=request.form['title']
        post_blog=request.form['new-blog']

        if post_title == "":
            error_title='Please insert the title of your new post'
        if post_blog == "":
            error_body='Please insert the body of  your new post'
        if not error_title and not error_body: 
            new_blog=Blog(post_title,post_blog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/get-id?id={}".format(new_blog.id))

        else:
            return render_template('newpost.html', error_title=error_title, error_body=error_body)
    else:
        return render_template('newpost.html')
@app.route('/blog')
def blog():
    blog_posts=  Blog.query.all()
    return render_template('blog.html',blog_posts=blog_posts)
# #create different app route to redirect to /blog?id={id} to display get-id.html template
@app.route('/get-id')
def display_post(): 
    blog_id=request.args.get('id')
    blog_posts=Blog.query.filter_by(id=blog_id).first()
    return render_template('get-id.html',post=blog_posts)
    
@app.route('/')
def index():
    return redirect('/blog')
if __name__=='__main__':
    app.run()