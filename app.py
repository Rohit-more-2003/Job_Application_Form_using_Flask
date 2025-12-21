from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		first_name = request.form['firstName']
		last_name = request.form['lastName']
		email = request.form['email']
		start_date = request.form['startDate']
		occupation = request.form['occupation']
		
	
	return render_template('index.html')




if __name__ == "__main__":
	app.run(debug=True, port=5001)