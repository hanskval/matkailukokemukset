import sqlite3
from flask import Flask
from flask import abort
import secrets
from flask import redirect, render_template, flash, request, session
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

@app.route("/profile")
def profile():
    username = session.get("username")
    if not username:
        return redirect("/login")
    
    all_items = items.get_items_by_user(username)
    post_count = len(all_items)
    likes_count = items.get_total_likes(username)
    return render_template("profile.html",
                           username=username,
                           items=all_items,
                           post_count=post_count,
                           likes_count=likes_count)


@app.route("/find_experiences", methods=["GET", "POST"])
def find_experiences():
    query = request.args.get("query") or ""
    rating = request.args.getlist("rating")
    
    all_items = items.find_experiences(query, rating) if (query or rating) else [] # haku myös mahdollinen pelkästään arvosanalla
    return render_template("find_experiences.html", items=all_items, query=query, selected_ratings=rating)

@app.route("/item/<int:item_id>", methods=["POST","GET"])
def show_kokemus(item_id):
    comments = items.get_comments(item_id)
    
    username = session.get("username")
    if username:
        user_id = items.get_user_id(username)
      
    if request.method == "POST":
        check_csrf()
        if not username:
            return redirect("/login")
        
        action = request.form.get("action")
        if action == "like":
            if not items.has_liked(user_id, item_id):
                items.add_like(user_id, item_id)
        elif action == "unlike":
            if items.has_liked(user_id, item_id):
                items.remove_like(user_id, item_id)
        elif action == "comment":
            comment = request.form.get("comment")
            if comment:
                items.comment_experience(user_id, item_id, comment)

        return redirect("/item/" + str(item_id))
    categories = items.get_categories(item_id)
    item = items.get_item(item_id)
    liked = items.has_liked(user_id, item_id) if username else False
    count = items.get_likes_count(item_id)
    if not item:
        abort(404)
    return render_template("show_experiences.html", item=item, liked=liked, count=count, comments=comments, categories=categories)



@app.route("/experiences")
def experiences():
    return render_template("experiences.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if username == "" or password1 == "" or password2 == "":
        flash("Kaikki kentät ovat pakollisia")
        return redirect("/register")
    if password1 != password2:
        flash("Antamat salasanat eivät ole samat")
        return redirect("/register")

    password_hash = generate_password_hash(password1)
    add = items.insert_user(username, password_hash)

    if not add:
        flash("Käyttäjätunnus on jo varattu")
        return redirect("/register")

    return redirect("/login")

@app.route("/create_experience", methods=["POST"])
def create_experience():
    title = request.form["title"]
    check_csrf()
    description = request.form["description"]
    rating = request.form["rating"]
    if not session.get("username"):
        return redirect("/login")

    if len(title) > 25 or len(description) > 5000:
        return render_template("experiences.html", error="Otsikon tulee olla enintään 25 merkkiä ja kuvauksen enintään 5000 merkkiä pitkä.")

    username = session["username"]
    user_id = items.get_user_id(username)
    category = request.form["category"]
    
    if user_id:
        items.add_item(title, description, rating, user_id, category)
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/update_experience", methods=["POST"])
def update_experience():
    title = request.form["title"]
    check_csrf()
    description = request.form["description"]
    rating = request.form["rating"]
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    category = request.form["category"]
    if len(title) > 50 or len(description) > 5000:
        return render_template("edit_experience.html", item=item, error="Otsikon tulee olla enintään 50 merkkiä ja kuvauksen enintään 5000 merkkiä pitkä.")
    if item["username"] != session.get("username"):
        return redirect("/")

    items.update_item(item_id, title, description, rating, category)

    return redirect("/item/" + str(item_id))

@app.route("/remove_experience/<int:item_id>", methods=["GET", "POST"])
def remove_experience(item_id):
    item = items.get_item(item_id)

    if not item:
        abort(404)
    if item["username"] != session.get("username"):
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("remove_experience.html", item=item)
        if request.method == "POST":
            check_csrf()
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

        password_hash = items.get_user_password(username)
        if password_hash and check_password_hash(password_hash, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä tunnus tai salasana")

def check_csrf():
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)

@app.route("/logout")
def logout():
    if not session.get("username"):
        return redirect("/")
    del session["username"]
    return redirect("/")

@app.route("/edit_experience/<int:item_id>")
def edit_kokemus(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["username"] != session.get("username"):
        return redirect("/")
    return render_template("edit_experience.html", item=item)
