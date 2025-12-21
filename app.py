from flask import Flask, render_template
from flask import request
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

from datetime import datetime

from info import password, sender

app = Flask(__name__)

# Configure the app to protect it from hackers, trackers, hijackers, etc.
app.config["SECRET_KEY"] = "myApplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465           # port number for gmail
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = sender
app.config["MAIL_PASSWORD"] = password

# Create the instance of database
db = SQLAlchemy(app)

# Create mail instance
mail = Mail(app)


# Create database model
class Form(db.Model):
	# Create table for database
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	email = db.Column(db.String(80))
	date = db.Column(db.Date)
	occupation = db.Column(db.String(80))


@app.route('/', methods=["GET", "POST"])
def index():
	# Get user information if method is 'POST
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
		
		# Send the mail
		message_body = f"Thank you for your submission, {first_name}." \
		               f"Here is your data:\n{first_name}\n{last_name}\n{start_date}\n" \
		               f"Thank you!"
		
		message = Message(subject="New form submission",
		                  sender=app.config["MAIL_USERNAME"],
		                  recipients=[email],
		                  body=message_body)
		
		mail.send(message)
		
		# Display successful submission of form and email sent.
		flash(f"{first_name} , your form was submitted successfully.", "success")
		
	return render_template('index.html')


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True, port=5001)