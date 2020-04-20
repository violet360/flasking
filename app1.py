from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))


	def __init__(self, name, email):
		self.name = name
		self.email = email


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/view")
def view():
	x = users.query.all()
	return render_template('view.html', usrs = x)


@app.route("/side/<y>")
def side(y):
	return render_template("choose.html", usr = y)


@app.route("/delete/<x>")
def delete(x):
	var = users.query.filter_by(name = x).first()
	# print(var)
	db.session.delete(var)
	db.session.commit()
	return redirect(url_for("view"))

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["lame"]
		session["user"] = user

		found_user = users.query.filter_by(name = user).first()

		if found_user:
			session["email"] = found_user.email

		else:
			usr = users(user, "")
			db.session.add(usr)
			db.session.commit()


		flash(f"login successful {user}")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			var = session["user"]
			flash(f"you are already logged in {var}", "info")
			return redirect(url_for("user"))

		return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
	email = None
	if "user" in session:
		user = session["user"]

		if request.method == "POST":
			email = request.form["email"]
			session["email"] = email
			found_user = users.query.filter_by(name = user).first()
			found_user.email = email
			db.session.commit()
			flash("email was saved")

		else:
			if "email" in session:
				email = session["email"]

		return render_template("display.html", email = email)
	else:
		flash("you are not logged in")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	# print(session)
	if "user" in session:
		# print(111)
		user = session['user']
		print(user)
		msg = f"{user} have been logged out"
		print(msg)
		flash(msg, "info")
		# var = get_flashed_messages()
		# print(var)
	session.pop('user', None)
	session.pop("email", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)
