import secrets, os
from flask import render_template, url_for, flash, redirect, request
from flask_blog.forms import RegistrationForm, LoginForm, UpdateaccountForm
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

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    # f_name, f_ext = os.path.splitext(form_pic.filename)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_file_name = random_hex + f_ext    
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_file_name)
    form_pic.save(pic_path)
    
    return pic_file_name
    

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateaccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_picture(form.picture.data)        
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)
