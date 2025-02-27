from flask import Flask, render_template, session, url_for, redirect, g, request
from database import get_db, close_db
from flask_session import Session
from forms import LoginForm, RegistrationForm, ExtraForm, AdminForm, AddForm, RemoveForm, EditForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
'''
My system has two user logins: regular and administrator.
To register normally, click Register Now on the main page,
For Administrator, click Admin and use:
Username : keely and the password : 123
'''

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
price = 0

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_req(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def index():
    return render_template("index.html")

#################REG, LOGIN, LOGOUT

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        conflict_user = db.execute(
            """SELECT * FROM users
                WHERE user_id = ?;""", (user_id,)).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("Username taken!")
        else:
            db.execute("""
                INSERT INTO users (user_id, password)
                VALUES (?, ?);""",
                (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
            
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute(
            """SELECT * FROM users
                WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("Username does not exist.")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect password.")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login_form.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )

##############ADMIN DASHBOARD

@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        admin = form.admin.data
        passw = form.passw.data
        if admin == "keely" and passw == "123":
            return redirect( url_for("admin_dash"))
        
    return render_template( "admin_log.html", form=form)

@app.route("/admin_dash")
def admin_dash():
    return render_template("admin_dash.html")

@app.route("/admin_add", methods=["GET", "POST"])
def admin_add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        desc = form.desc.data
        db = get_db()
        addItem = db.execute("""INSERT INTO coffees (name, price, description)
                             VALUES
                                ( ?, ?, ?);""", (name,price,desc))
        db.commit()
        return redirect(url_for('orders'))
    return render_template("admin_add.html", form=form)

@app.route("/admin_remove", methods=["GET", "POST"])
def admin_remove():
    form = RemoveForm()
    if form.validate_on_submit():
        name = form.name.data
        db = get_db()
        coffees = db.execute("""SELECT * FROM coffees WHERE name = ?""", (name, )).fetchone()
        if coffees is not None:
            RemoveItem = db.execute("""DELETE FROM coffees
                                    WHERE name = ?""", (name,))
            db.commit()
            return redirect(url_for('orders'))
        else:
            form.name.errors.append("Entry does not exist.")
    return render_template("admin_remove.html", form=form)

@app.route("/admin_edit", methods=["GET", "POST"])
def admin_edit():
    form = EditForm()
    if form.validate_on_submit():
        name = form.name.data
        name2 = form.name2.data
        price = form.price.data
        desc = form.desc.data
        db = get_db()
        coffees = db.execute("""SELECT * FROM coffees WHERE name = ?""", (name, )).fetchone()
        if coffees is not None:
            item = db.execute("""UPDATE coffees SET name = ?, price = ?, description = ? WHERE name = ?;""", ( name2, price, desc, name ))
            db.commit()
            return redirect(url_for('orders'))
        else:
            form.name.errors.append("Entry does not exist.")
    return render_template("admin_edit.html", form=form)

##############ORDERING 

@app.route("/orders")
def orders():
    db = get_db()
    orders = db.execute("""SELECT * FROM coffees; """).fetchall()
    return render_template("orders.html", coffees=orders)

@app.route("/order/<int:coffee_id>")
def order(coffee_id):
    db = get_db()
    order = db.execute("""SELECT * FROM coffees
                       WHERE coffee_id = ?;""", (coffee_id,)).fetchone()
    return render_template("order.html", coffee=order )


##################CART

@app.route("/basket")
@login_req
def basket():
    if "basket" not in session:
        session["basket"] = {}
    names = {}
    extras = {}
    db = get_db()
    for coffee_id in session["basket"]:
        order = db.execute("""SELECT * FROM coffees
                          WHERE coffee_id = ?;""", (coffee_id,)).fetchone()
        # price += order["price"]
        name = order["name"]
        names[coffee_id] = name
        extras = session.get('extras')
        coffee_id = session['extras']

    return render_template("basket.html", basket=session["basket"], names=names, extras=extras, price=price )

@app.route("/add_to_basket/<int:coffee_id>")
@login_req
def add_to_basket(coffee_id):
    if "basket" not in session:
        session["basket"] = {}
    if coffee_id not in session["basket"]:
        session["basket"][coffee_id] = 1
    else:
        session["basket"][coffee_id] = session["basket"][coffee_id] + 1
    session.modified = True
    return redirect( url_for("basket"))

@app.route("/remove_from_basket/<int:coffee_id>")
@login_req
def remove_from_basket(coffee_id):
    if "basket" not in session:
        session["basket"] = {}
    if coffee_id in session["basket"]:
        session["basket"].pop(coffee_id) 
        session.modified = True
    return redirect( url_for("basket"))

@app.route("/add/<int:coffee_id>")
@login_req
def add(coffee_id):
    if "basket" not in session:
        session["basket"] = {}
    if coffee_id in session["basket"]:
        session["basket"][coffee_id] = session["basket"][coffee_id] + 1
        session.modified = True
    return redirect( url_for("basket"))



@app.route("/add_to_basket/<int:coffee_id>/extra", methods=["GET", "POST"])
@login_req
def extra(coffee_id):
    if "basket" not in session:
        session["basket"] = {}
    db = get_db()
    extra = db.execute("""SELECT * FROM coffees
                     WHERE coffee_id = ?;""", (coffee_id,)).fetchone()
    form = ExtraForm()
    if form.validate_on_submit():
        session['extras'] = form.extras.data
            
        return redirect( url_for('add_to_basket', coffee=extra, coffee_id=coffee_id, form=form))
    return render_template("extra.html",coffee=extra, form=form)

