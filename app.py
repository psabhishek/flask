from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,DecimalField,FieldList
from passlib.hash import sha256_crypt
from functools import wraps
import hashlib
import json


from data import Movies,User




app = Flask(__name__)
app.secret_key = 'secret123'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search' ,methods = ["GET" , "POST"])
def search_on_db():


    if request.method == "POST":
        return_ele = []

        value = request.form.get("search")
        popularity_element = Movies.select().where(Movies.popularity.contains(value)).execute()
        director_element = Movies.select().where(Movies.director.contains(value)).execute()
        genre_element = Movies.select().where(Movies.genre.contains(value)).execute()
        imdb_score_element = Movies.select().where(Movies.imdb_score.contains(value)).execute()
        name_element = Movies.select().where(Movies.name.contains(value)).execute()
        elements = [name_element,director_element,popularity_element,genre_element,imdb_score_element]
        for ele in elements:
            for movie in ele:
                movie_element = str(movie.popularity),str(movie.director),str(movie.genre),str(movie.imdb_score),str(movie.name)
                return_ele.append(movie_element)



        if len(return_ele) > 0:
            return render_template("dashboard.html",movies=list(set(return_ele)))
        else:
            msg = 'No Movies Found'
            return render_template('dashboard.html', msg=msg)

    return render_template('search.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = hashlib.md5( str(form.password.data).encode()).hexdigest()
            isadmin = "False"
            user = User(name = name,email = email , username = username , password = password , isadmin = isadmin)
            user.save()

            flash('You are now registered and can log in', 'success')

            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        result = User.get(User.username == username)
        if result is not None:
            password = result.password
            if hashlib.md5( str(password_candidate).encode()).hexdigest() == password:
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')




def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap



@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))




@app.route('/dashboard')
@is_logged_in
def dashboard():
    element = []
    for user in Movies.select():
        ele = str(user.popularity),str(user.director),str(user.genre),str(user.imdb_score),str(user.name)
        element.append(ele)

    if len(element)>0:
        return render_template('dashboard.html', movies=element)
    else:
        msg = 'No Movies Found'
        return render_template('dashboard.html', msg=msg)


@app.route('/add_movies', methods=['GET', 'POST'])
@is_logged_in
def add_movies():

    if request.method == 'POST':
        popularity = float(request.form.get('popularity'))
        director = request.form.get('director')
        genre = request.form.get('genre')
        imdb_score = float(request.form.get('imdb_score'))
        name = request.form.get('name')
        movies = Movies(popularity=popularity, director=director, genre=genre, imdb_score=imdb_score, name=name)
        movies.save()



        flash('movie Created', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_movie.html',)



@app.route('/bulkadd', methods=['GET', 'POST'])
@is_logged_in
def add_bulk():

    if request.method == 'POST':
        file = request.files['file']
        myfile = file.read()
        json_element = json.loads(myfile)
        for ele in json_element:


            popularity = ele["99popularity"]
            director = ele["director"]
            genre = ",".join(ele["genre"])
            imdb_score = ele["imdb_score"]
            name = ele["name"]

            movies = Movies(popularity=popularity, director=director, genre=genre, imdb_score=imdb_score, name=name)
            movies.save()


        flash('BULK UPLOAD SUCCESS', 'success')

        return redirect(url_for('dashboard'))
    return render_template('bulk_upload.html',)

if __name__ == '__main__':
    app.run()
