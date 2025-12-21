from flask import Flask, render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

# Configure the app to protect it from hackers, trackers, hijackers, etc.
app.config["SECRET_KEY"] = "myApplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


# Create database model
class Form(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	email = db.Column(db.String(80))
	date = db.Column(db.Date)
	occupation = db.Column(db.String(80))


@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		# Get the user information
		first_name = request.form['firstName']
		last_name = request.form['lastName']
		email = request.form['email']
		start_date = request.form['startDate']
		start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
		occupation = request.form['occupation']
		
		# Enter the user information in database
		form = Form(first_name=first_name, last_name=last_name, email=email,
		            date=start_date_obj, occupation=occupation)
		db.session.add(form)
		db.session.commit()
		
	return render_template('index.html')


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True, port=5001)