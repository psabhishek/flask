from flask import Flask, render_template, flash, redirect, url_for, session, request
from functools import wraps
import hashlib
import json
from settings import SUPERUSERMASTER

from forms import RegisterForm
from utility.messages import M_REGISTRATION_SUCCESS, FLASH_SUCCESS, M_LOGIN_SUCCESS, M_UNAUTHORISED, FLASH_DANGER, \
    M_LOGOUT_SUCCESS, FLASH_FAILURE, M_EMPTY_FORM_SUMBITTED, M_FORM_SUBMITTED, M_BULK_UPLOAD
from settings import FLASK_HOST, FLASK_PORT,FLASK_SECRET_KEY
from models import Movies, User

import requests


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY


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


@app.route('/search_es' ,methods = ["GET" , "POST"])
def search_on_es():


    if request.method == "POST":
        return_ele = []
        import pdb;pdb.set_trace()
        value = request.form.get("search")
        ele = {"serch_key":value}
        elements = requests.post("http://35.244.38.4:5001/search",data = json.dumps(ele))
        json_element = json.loads(elements.text)["hits"]["hits"]
        for es_ele in  json_element:
            es_obj = es_ele["_source"]
            movie_ele = (str(es_obj["popularity"]),es_obj["director"],",".join(es_obj["genre"]),
                               str(es_obj["imdb_score"]),es_obj["name"])
            return_ele.append(movie_ele)




        if len(return_ele) > 0:
            return render_template("dashboard.html",movies=list(set(return_ele)))
        else:
            msg = 'No Movies Found'
            return render_template('dashboard.html', msg=msg)

    return render_template('search.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data ## will be hashed in pre_save form
            isadmin = "False"
            user = User(name = name,email = email , username = username , password = password , isadmin = isadmin)
            user.save()

            flash(M_REGISTRATION_SUCCESS, FLASH_SUCCESS)

            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        import pdb;pdb.set_trace()
        username = request.form['username']
        password_candidate = request.form['password']
        result = User.get(User.username == username)
        if result is not None:
            password = result.password
            if hashlib.md5( str(password_candidate).encode()).hexdigest() == password:
                session['logged_in'] = True
                session['username'] = username
                flash(M_LOGIN_SUCCESS, FLASH_SUCCESS)
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
            flash(M_UNAUTHORISED, FLASH_DANGER)
            return redirect(url_for('login'))
    return wrap



@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash(M_LOGOUT_SUCCESS, FLASH_SUCCESS)
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
    if session.get("username") == SUPERUSERMASTER["username"]:

        if request.method == 'POST':
            if request.form.get('name',None):
                try:
                    popularity = float(request.form.get('popularity'))
                    director = request.form.get('director')
                    genre = request.form.get('genre')
                    imdb_score = float(request.form.get('imdb_score'))
                    name = request.form.get('name')
                    movies = Movies(popularity=popularity, director=director, genre=genre, imdb_score=imdb_score, name=name)
                    es_element = {
                        "popularity": popularity,
                        "director": director,
                        "genre":  genre.split(","),
                        "imdb_score": imdb_score,
                        "name": name}
                    requests.post("http://35.244.38.4:5001/add_movies",data= json.dumps(es_element) )
                    movies.save()
                    flash(M_FORM_SUBMITTED, FLASH_SUCCESS)
                    return redirect(url_for('dashboard'))
                except Exception as e:
                    flash("error", FLASH_FAILURE)
                    return redirect(url_for('add_movies'))
            else:
                flash(M_EMPTY_FORM_SUMBITTED, FLASH_FAILURE)
                return render_template('add_movie.html',)
        return render_template('add_movie.html',)
    else:
        flash(M_UNAUTHORISED, FLASH_FAILURE)

        return redirect(url_for('dashboard'))




@app.route('/bulkadd', methods=['GET', 'POST'])
@is_logged_in
def add_bulk():
    if session.get("username") == SUPERUSERMASTER["username"]:

        if request.method == 'POST':
            file = request.files['file']
            myfile = file.read()
            json_element = json.loads(myfile)
            for ele in json_element:
                popularity = ele["popularity"]
                director = ele["director"]
                genre = ",".join(ele["genre"])
                imdb_score = ele["imdb_score"]
                name = ele["name"]

                movies = Movies(popularity=popularity, director=director, genre=genre, imdb_score=imdb_score, name=name)

                es_element = {
                    "popularity": popularity,
                    "director": director,
                    "genre": genre.split(","),
                    "imdb_score": imdb_score,
                    "name": name}
                requests.post("http://35.244.38.4:5001/add_movies", data=json.dumps(es_element))
                movies.save()


            flash(M_BULK_UPLOAD, FLASH_SUCCESS)

            return redirect(url_for('dashboard'))
        return render_template('bulk_upload.html',)
    else:
        flash(M_UNAUTHORISED, FLASH_FAILURE)

        return redirect(url_for('dashboard'))


@app.route('/analytics', methods=['GET', 'POST'])
@is_logged_in
def analytics():
        return render_template('analytics.html', )




if __name__ == '__main__':
    app.run(host=FLASK_HOST,port=FLASK_PORT)

