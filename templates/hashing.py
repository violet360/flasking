from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
# from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 1)


@app.route('/home')
def home():
	return render_template('home.html')


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		user = request.form["lame"]
		return redirect(url_for("user", usr=user))
        

@app.route('/<usr>')
def user(usr):
	return f"hello {usr}"


if __name__ == '__main__':
	app.run(debug=True)