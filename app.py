from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


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