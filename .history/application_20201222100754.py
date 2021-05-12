import os

import sqlite3 
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connecting to the database  
connection = sqlite3.connect("amsun_notes.db", check_same_thread=False)

# cursor  
db = connection.cursor()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ROUTES<<<<<<<<<<<<<<<<<<

# ///////////////INDEX\\\\\\\\\\\\\\\\\\
@app.route("/")
def home_page():
    return render_template("home.html")

# ////////////////WRITE NOTES\\\\\\\\\\\\\
@app.route("/home")
@login_required
def index():
    return render_template("index.html")

# //////PROFILE\\\\\\\\
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# /////////////MY NOTES\\\\\\\\\\
@app.route("/my_notes")
@login_required
def my_notes():

    # logged user
    user_id = session['user_id']

    db.execute("SELECT title, notes FROM notes WHERE user_id=:user_id", {'user_id':user_id})
    notes = db.fetchall()

    # Ensure user has notes
    if not notes:
        return render_template("index.html", message = "You Do Not Have Any Stock")

    return render_template("my_notes.html", notes=notes)


@app.route("/my_notes/<note_id>/edit", methods=["GET", "POST"])
@login_required
def edit(note_id):
    if request.method == "GET":

        #  # logged user
        # user_id = session['user_id']

        # db.execute("SELECT note_id, title, notes FROM notes WHERE user_id=:user_id", {'user_id':user_id})
        # notes = db.fetchall()

        # note_id = notes[1][0]
        # print(note_id)

        # # query database for the note 
        # db.execute("SELECT * FROM notes WHERE note_id=:note_id", {'note_id':note_id})
        return render_template("edit.html")

# >>>>>>>>>>>>>REGISTER<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if 'GET' render Reg. form
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form.get("username")
        # Ensure username is submitted
        if not request.form.get("username"):
             return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password") and not request.form.get("confirmation"):
            return apology("must provide password and confirmation", 403)
        else:
            # query db
            db.execute("SELECT * FROM users WHERE username = :username",
                            {'username' : username})
            rows = db.fetchall()

            # check if user exists
            if len(rows) == 1:
                return apology("username already exists", 403)
            else:
                username = request.form.get("username")

            # password
            if request.form.get("password") == request.form.get("confirmation"):
                # hash password
                pwhash = generate_password_hash(request.form.get("password"), method='plain')
            else:
                return apology("passwords do not match", 403)

            # update db
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :pwhash)", {'username':username, 'pwhash':pwhash})

            # To save the changes in the files. Never skip this.  
            # If we skip this, nothing will be saved in the database. 
            connection.commit() 
            
            # # close the connection 
            # connection.close()
            return redirect("/")


# >>>>>>>>>>>>>>>>>>>>>>LOGIN<<<<<<<<<<<<<<<<<<<<<<


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = :username",
                          {'username':request.form.get("username")})
        
        rows = db.fetchall()

        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

    # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>LOGOUT<<<<<<<<<<<<<<<<<<<<<<<<

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# >>>>>>>>>>>>>>>>>>>SAVE NOTES <<<<<<<<<<<<<<<<<<<<<<<<<
@app.route("/notes", methods=["GET", "POST"])
@login_required
def save():
    #save notes to database
    
    # logged user
    user_id = session['user_id']

    if request.method == "POST":

        # get the title
        title = request.form.get("title")

        #get notes
        notes = request.form.get("notes")

        # ensure the fields are not blank
        if not request.form.get("notes"):
            return apology('must write something', 403)
        else:
            db.execute("INSERT INTO notes (user_id, title, notes) VALUES (:user_id, :title, :notes)", {'user_id':user_id, 'title':title, 'notes':notes})

            # save to data base
            connection.commit() 
            return render_template("index.html")
    