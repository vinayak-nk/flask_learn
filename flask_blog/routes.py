from flask import render_template, url_for, flash, redirect
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_blog import app, db, bcrypt

posts = [
    {
        'author': 'vk',
        'title': 'Blogpost 1',
        'content': 'First post content',
        'date_posted': 'March, 7 2022'
    },
    {
        'author': 'vnk',
        'title': 'Blogpost 2',
        'content': 'Second post content',
        'date_posted': 'March, 8 2022'
    }
]


@app.route("/")
@app.route("/home")
def home():
    # return "<p>Hello.---------!!!</p>"
    return render_template('home.html', posts=posts, title="xyz")

@app.route("/about")
def about():
    return render_template('about.html')
    # return "<p>About.---------!!!</p>"


@app.route("/register",  methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} Your account has been created!', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'vnk@gmail.com' and form.password.data == '123':
            flash('Logged In!!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logged Failed', 'danger')
            return redirect(url_for('home'))    
    return render_template('login.html', title="Login", form=form)

