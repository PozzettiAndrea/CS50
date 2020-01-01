import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # look up the current user
    user = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    stocks = db.execute(
        "SELECT symbol, SUM(sharenumber) as total_shares FROM transactions WHERE id = :id GROUP BY symbol HAVING total_shares > 0", id=session["user_id"])
    symbols = []
    quotes = []
    number = []
    totstockvalue = []
    totalitems = 0
    portvalue = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        quotes.append(quote["price"])
        symbols.append(stock["symbol"])
        number.append(stock["total_shares"])
        totstockvalue.append(quote["price"] * (stock["total_shares"]))
        portvalue += quote["price"] * (stock["total_shares"])
        totalitems += 1

    balance = user[0]["cash"]
    total = balance + portvalue
    print(totalitems)
    return render_template("index.html", symbols=symbols, quotes=quotes, number=number, total=total, balance=balance, totstockvalue=totstockvalue, totalitems=totalitems)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        sharez = request.form.get("shares")
        shares = 0

        try:
            shares = int(sharez)
        except:
            return apology("share number must be a positive integer")

        if shares < 1:
            return apology("share number must be a positive integer")

        if not stock:
            return apology("invalid symbol", 400)

        if (not shares) or (shares < 1):
            return apology("share number must be a positive integer")

        money = float((db.execute("SELECT cash FROM users WHERE id = :id",
                                  id=session["user_id"]))[0]["cash"])

        totprice = (stock["price"] * shares)
        # check if enough money
        if totprice > money:
            return apology("Stop being poor")

        else:
            # subtract the money from their balance
            db.execute("UPDATE users SET cash = cash - :totprice WHERE id = :id",
                       id=session["user_id"],
                       totprice=totprice)

            # update transactions history
            db.execute("INSERT INTO transactions (id, symbol, sharenumber, price) VALUES(:id, :symbol, :sharenumber, :price)",
                       id=session["user_id"], symbol=stock["symbol"], sharenumber=shares, price=totprice)

            flash("Transaction completed :)")
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


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


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # look up the current user
    transactions = db.execute(
        "SELECT time, symbol, sharenumber, price FROM transactions WHERE id = :id ORDER BY time ASC", id=session["user_id"])
    return render_template("history.html", transactions=transactions)


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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symboll = request.form.get("symbol")

        if not symboll:
            return apology("invalid symbol", 400)

        stock = lookup(symboll)

        if not stock:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        CASH = request.form.get("cash")
        db.execute("UPDATE users SET cash = cash + :CASH WHERE id = :id",
                   id=session["user_id"], CASH=CASH)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addcash.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        price = stock["price"]
        profit = price * shares

        if not stock:
            return apology("invalid symbol", 403)

        if (not shares) or (shares < 1):
            return apology("share number must be a positive integer")

        availablestocks = ((db.execute(
            "SELECT SUM(sharenumber) FROM transactions WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=stock["symbol"])))[0]['SUM(sharenumber)']

        if availablestocks < shares:
            return apology("you don't have enough stocks!")

        else:
                        # subtract the money from their balance
            db.execute("UPDATE users SET cash = cash + :profit WHERE id = :id",
                       id=session["user_id"], profit=profit)

            # update transactions history
            db.execute("INSERT INTO transactions (id, symbol, sharenumber, price) VALUES(:id, :symbol, :sharenumber, :price)",
                       id=session["user_id"], symbol=stock["symbol"], sharenumber=- shares, price=profit)

            flash("Transaction completed :)")
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        symblist = []
        symbols = db.execute(
            "SELECT symbol, SUM(sharenumber) as total_shares FROM transactions WHERE id = :id GROUP BY symbol HAVING total_shares > 0", id=session["user_id"])
        for i in symbols:
            symblist.append(i["symbol"])
        return render_template("sell.html", symblist=symblist)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
