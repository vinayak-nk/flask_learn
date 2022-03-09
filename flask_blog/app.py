from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e4fbcd72d53972a48b59a0807882e41a' #import secrets, secrets.token_hex(16)

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
        flash(f'Account created for {form.username.data}!', 'success')
        
        return redirect(url_for('home'))
    
    return render_template('register.html', title='Registre', form=form)

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


if __name__ == '__main__':
    app.run(debug=True)

