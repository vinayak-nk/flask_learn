from flask import render_template, url_for, flash, redirect, request
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Logged Failed', 'danger')
    return render_template('login.html', title="Login", form=form)


# @app.route("/login",  methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'vnk@gmail.com' and form.password.data == '123':
#             flash('Logged In!!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Logged Failed', 'danger')
#             return redirect(url_for('home'))    
#     return render_template('login.html', title="Login", form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='account')
