import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import google.generativeai as genai
import random

from helpers import apology, login_required

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# copied above code from app.py from finance assignment

# configure gemini api
genai.configure(api_key=API_KEY) 
model = genai.GenerativeModel("gemini-2.0-flash")


# configuring db
con = sqlite3.connect("users.db", check_same_thread=False)
con.row_factory = sqlite3.Row
db = con.cursor()

db.execute(
    """ CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0.00
) """)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("userName"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        userName = request.form.get("userName")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (userName,)
        ).fetchone()

        if rows:
            user_dict = dict(rows)

            print(user_dict)

            print(len(user_dict))

            print(rows)

            # Ensure username exists and password is correct
            if len(user_dict) != 4 or not check_password_hash(
                user_dict['hash'], password
            ):
                return apology("invalid username or password", 403)
                

            # Remember which user has logged in
            session["user_id"] = user_dict["id"]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# sign-up route


@app.route('/signup',  methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not username or not password1 or not password2:
            return apology("Something's Missing")

        elif password1 != password2:
            return apology("Passwords don't match")

        hash = generate_password_hash(password1)

        
       

        try:
            # insert user in db and redirect to login page
            db.execute(
                """INSERT INTO users (username, hash) VALUES(?, ?)""", (username, hash)
            )
            return redirect("/login")

        except:
            # return apology if username taken
            return apology("User Aleady Taken", 403)

    return render_template('signup.html')


@app.route('/', methods=['POST', 'GET'])
@login_required
def home():
    # redirect to /play to start the game
    if request.method == 'POST':
        return redirect('/play')

    return render_template('home.html')


# leaderboard, shows users and their scores
@app.route('/leaderboard')
@login_required
def leaderboard():
    users = db.execute(""" SELECT * FROM users ORDER BY score DESC""")
    return render_template('leadb.html', users=users)

# Description about site


@app.route('/about')
@login_required
def about():
    return render_template('about.html')

# Main route, where user play


@app.route('/play',  methods=['POST', 'GET'])
@login_required
def play():

    userid = session['user_id']
    if request.method == 'POST':
        # end game if all guesses are used
        if session['guesses'] == 1:
            return render_template('failed.html')

        # getting userinput
        userinput = request.form.get('userInput')
        action = request.form.get('action')

        movie_text = session.get('movie_text')

        if not userinput:
            return apology('You can\'t submit without any input, game session expired')

        # checking if user asked a question or passed a guess
        if action == 'ask':

            # increasing number of question, as points will be calculated on base of number of questoin asked
            session['question_asked'] += 1

            # generating a hint for movie using gemini api
            hint = model.generate_content(f""" \'{userinput}\', \'{movie_text}\',
                                           your answer should be as short as possible few words at most or a sentnce at most, DO NOT tell me the title
                                          of this movie \'{movie_text}\' in your answer""")

            # checking if ai mistakenly revealed the movie in hint
            if movie_text in hint.text.lower():
                return render_template('play.html', hint="I can't answer that.")

            # otherwise re-rendering the page with new data
            return render_template('play.html', hint=hint.text, guess=session['guesses'], question=session['question_asked'])

        elif action == 'guess':

            # checking if user guessed the correct movie
            if userinput.lower() in movie_text:
                questions = session['question_asked']
                # calculating score on bases of question asked by user
                if questions > 9:
                    score = 10
                else:
                    score = 100 - (questions*10)

                # updating score of user in db
                db.execute(""" UPDATE users SET score = score + ? WHERE id = ?""", (score, userid))
                return render_template('congrats.html', question=session['question_asked'], score=score)

            else:
                # decrementing guesses if user guessed wrong
                session['guesses'] -= 1
                return render_template('play.html', hint="No it's not that movie", guess=session['guesses'], question=session['question_asked'])

    else:

        # generating a random movie name using ai
        seed = random.randint(1000, 9999)
        rating = random.randint(3,10)
        movie = model.generate_content(
            f"give me a random marvel movie, your answer should only contain the name of the movie. Seed{seed}")

        print(movie.text)

        # storing movie name and other data in user sessions
        session['movie_text'] = movie.text.lower()
        session['question_asked'] = 0
        session['guesses'] = 5

        # generating the first hint for user
        hint = model.generate_content(
            f"Generate a 1-2 line funny hint for this movie \'{movie.text}\' it shouldn't include anything major which can just give away what this movie is.")

        return render_template('play.html', hint=hint.text, guess=session['guesses'], question=session['question_asked'])


@app.route('/logout')
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
