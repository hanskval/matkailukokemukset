import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import db
import config
import items

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/find_kokemukset", methods=["GET", "POST"])
def find_kokemukset():
    query = request.args.get("query") or ""
    rating = request.args.getlist("rating")
    
    all_items = items.find_kokemuksia(query, rating) if (query or rating) else [] # haku myös mahdollinen pelkästään arvosanalla
    return render_template("find_kokemukset.html", items=all_items, query=query, selected_ratings=rating)

@app.route("/item/<int:item_id>")
def show_kokemus(item_id):
    item = items.get_item(item_id)
    return render_template("show_kokemukset.html", item=item)

@app.route("/kokemukset")
def kokemukset():
    return render_template("kokemukset.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

@app.route("/create_kokemus", methods=["POST"])
def create_kokemus():
    title = request.form["title"]
    description = request.form["description"]
    rating = request.form["rating"]

    username = session["username"]
    sql = "SELECT id FROM users WHERE username = ?"
    user_id = db.query(sql, [username])[0][0]

    items.add_item(title, description, rating, user_id)

    return redirect("/")

@app.route("/update_experience", methods=["POST"])
def update_experience():
    title = request.form["title"]
    description = request.form["description"]
    rating = request.form["rating"]
    item_id = request.form["item_id"]

    items.update_item(item_id, title, description, rating)

    return redirect("/item/" + str(item_id))

@app.route("/remove_experience/<int:item_id>", methods=["GET", "POST"])
def remove_experience(item_id):
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_experience.html", item=item)
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        results = db.query(sql, [username])
        if results:
            password_hash = results[0][0]
        else:
            return render_template("login.html", error="Väärä tunnus tai salasana")

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä tunnus tai salasana")
            

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/edit_experience/<int:item_id>")
def edit_kokemus(item_id):
    item = items.get_item(item_id)
    return render_template("edit_experience.html", item=item)
