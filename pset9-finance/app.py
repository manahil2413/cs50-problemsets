import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_stock = db.execute(
        "SELECT symbol,SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares)>0", session["user_id"])
    user_cash = db.execute("SELECT cash FROM users WHERE id =?", session["user_id"])[0]["cash"]

    total_cash = 0
    for stock in user_stock:
        stock_data = lookup(stock["symbol"])
        stock["name"] = stock_data["name"]
        stock["price"] = stock_data["price"]
        stock["total_price"] = stock["price"] * stock["shares"]
        total_cash = total_cash + stock["total_price"]

    total_amount = total_cash + user_cash
    return render_template("index.html", user_stock=user_stock, user_cash=user_cash, total_amount=total_amount)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if not symbol:
        return apology("Symbol required")
    if not shares:
        return apology("Shares required")

    try:
        shares = int(shares)
    except ValueError:
        return apology("Shares must be a number")

    if shares <= 0:
        return apology("Shares must be positive")

    stock = lookup(symbol)
    if not stock:
        return apology("Invalid symbol")

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    cost = shares * stock["price"]
    if cost > cash:
        return apology("Not enough cash available")

    db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
               session["user_id"], symbol, shares, stock["price"])
    flash(f"Bought {shares} shares of {symbol} for {usd(cost)}")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    stock = db.execute(
        "SELECT symbol, shares, price, transacted_at FROM transactions WHERE user_id = ? ORDER BY transacted_at DESC",
        session["user_id"])
    return render_template("history.html", stock=stock)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        dictionary = lookup(symbol)
        if not dictionary:
            return apology("Symbol not found")
        else:
            return render_template("quoted.html", dict=dictionary)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return apology("Username required")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirmation")
        if not password:
            return apology("Password required")
        elif password != confirm_pass:
            return apology("passwords donot match")
        hash_password = generate_password_hash(password)
        try:
            new_user = db.execute(
                "INSERT INTO users (username,hash) VALUES(?,?)", username, hash_password)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_portfolio = db.execute(
            "SELECT symbol ,sum(shares) AS shares FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares)>0 ORDER BY symbol", session["user_id"])
        return render_template("sell.html", user_portfolio=user_portfolio)

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if not symbol:
        return apology("Symbol required")
    if not shares or not shares.isdigit():
        return apology("Shares required")
    shares = int(shares)
    if shares <= 0:
        return apology("Share must be a positive integer")

    rows = db.execute(
        "SELECT SUM(shares) AS total_share FROM transactions WHERE user_id=? AND symbol = ?", session["user_id"], symbol)
    total_shares = rows[0]["total_share"] or 0

    if total_shares < shares:
        return apology("Not enough shares to sell")

    stock_quote = lookup(symbol)
    if not stock_quote:
        return apology("Invalid symbol")
    price = stock_quote["price"]
    new_cash = price*shares
    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    db.execute("UPDATE users SET cash=? WHERE id=?", user_cash + new_cash, session["user_id"])
    db.execute("INSERT INTO transactions (user_id,symbol,shares,price) VALUES (?,?,?,?)",
               session["user_id"], symbol, price, -shares)
    flash(f"Sold {shares} shares of {symbol} for {usd(new_cash)}")
    return redirect("/")
