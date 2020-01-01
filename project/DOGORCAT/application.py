import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from dorc import dogorcat
from flask_mail import Mail, Message


UPLOAD_FOLDER = 'static/Images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from helpers import apology, login_required

# Configure application
app = Flask(__name__)








# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pets.db")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # look up the current user
    history = db.execute(
        "SELECT time, pet, imagename FROM history WHERE id = :id ORDER BY time ASC", id=session["user_id"])
    return render_template("history.html", history=history)

@app.route("/identify", methods=["GET", "POST"])
@login_required
def identify():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if request.files:
            f = request.files["file"]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            imagename = f.filename
            path = f"static/Images/{imagename}",
            pet = dogorcat(path[0])
            db.execute("INSERT INTO history (id, pet, imagename) VALUES(:id, :pet, :imagename)",
                       id=session["user_id"], pet=pet, imagename=imagename)
            return render_template("identified.html", pet=pet)
        else:
            return apology("Please upload a valid file",400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("identify.html")

@app.route("/")
@login_required
def index():
    return redirect("/identify")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print(request.form.get("username"))
        print(request.form.get("password"))
        print(request.form.get("confirmation"))
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Generate the password's hash and store new login credentials
        hash = generate_password_hash(request.form.get("password"))
        newuser = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                             username=request.form.get("username"),
                             hash=hash)

        # Check if username was taken
        if not newuser:
            return apology("username taken", 400)

        # Remember session
        session["user_id"] = newuser

        # FEEDBACC
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "POST":
        row = db.execute("SELECT COUNT(id) as count FROM users where username = :name", name=request.form.get("name"))
        available = ""
        if row[0]["count"] > 0:
            available = "not available"

        else:
            available = "available"

        return jsonify({"available": available})

    userName = request.args.get("username")
    rows = db.execute("SELECT COUNT(id) as count FROM users where username = :name", name=userName)

    if not userName or rows[0]["count"] > 0:
        return jsonify(False)

    else:
        return jsonify(True), 200


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
