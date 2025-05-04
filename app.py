from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import sqlite3
import items
import users
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", items = items, user = user)


@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []

    return render_template("find_item.html", query = query, results = results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    ratings = items.get_ratings(item_id)
    comments = items.get_comments(item_id)
    avg_rating = items.get_avg_rating(item_id)
    return render_template("show_item.html", item = item, classes = classes, ratings = ratings, comments = comments, avg_rating = avg_rating)

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods = ["POST"])
def create_item():
    require_login()
    check_csrf()
    name = request.form["name"]
    team = request.form["team"]
    player_number = request.form["player_number"]
    PPG = request.form["PPG"]
    RPG = request.form["RPG"]
    APG = request.form["APG"]
    position = request.form["position"]
    user_id = session.get("user_id")

    if not name or len(name) > 100 or "<" in name or ">" in name:
        return "Virheellinen nimi"
    if not team or len(team) > 100 or "<" in name or ">" in name:
        return "Virheellinen joukkue"


    classes = []
    if position:
        classes.append(("Pelipaikka", position))

    accolades = request.form.getlist("accolades[]")
    for accolade in accolades:
        classes.append(("Palkinnot", accolade))

    items.add_item(name, team, player_number, PPG, RPG, APG, user_id, classes)

    return redirect("/")

@app.route("/ranking")
def ranking():
    rankings = items.get_rankings()
    return render_template("ranking.html", rankings = rankings)

@app.route("/new_rating", methods = ["POST"])
def new_rating():
    require_login()
    check_csrf()
    rating = request.form["rating"]
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    user_id = session["user_id"]

    items.add_rating(item_id, user_id, rating)

    return redirect("/item/" + str(item_id))

@app.route("/new_comment", methods = ["POST"])
def new_comment():
    require_login()
    check_csrf()
    text = request.form["comment"]
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, text)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item = item)

@app.route("/update_item", methods = ["POST"])
def update_item():
    require_login()
    check_csrf()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    name = request.form["name"]
    team = request.form["team"]
    player_number = request.form["player_number"]
    PPG = request.form["PPG"]
    RPG = request.form["RPG"]
    APG = request.form["APG"]

    classes = []
    position = request.form["position"]
    if position:
        classes.append(("Pelipaikka", position))

    accolades = request.form.getlist("accolades[]")
    for accolade in accolades:
        classes.append(("Palkinnot", accolade))

    items.update_item(item_id, name, team, player_number, PPG, RPG, APG, classes)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        check_csrf()
        if ("remove" in request.form):
            items.remove_comments(item_id)
            items.remove_item_classes(item_id)
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))



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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            print(session)
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

