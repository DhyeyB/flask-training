from flask import Flask, render_template, request;
from flask_sqlalchemy import SQLAlchemy;
from datetime import datetime
from flask_mail import Mail
import json



local_server = True
with open('/home/bs/dhyey/bs/practice/flask/tutorial/config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    # MAIL_USER_SSL = True,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = params["gmail-user"],
    MAIL_PASSWORD = params["gmail-password"]
)
mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)





class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))





@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params =params, posts=posts)

@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params =params, post=post)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()

        mail.send_message("New msg from " + name, 
                          sender=email, 
                          recipients=[params['gmail-user']],
                          body = message + "\n" + phone
                          )

    return render_template('contact.html', params =params)

@app.route("/login", methods = ['GET', 'POST'])
def dashboard():
    if request.method=='POST':
        pass
    else:
        return render_template('login.html', params =params)

@app.route("/about")
def about():
    return render_template('about.html', params =params)

app.run(debug=True)