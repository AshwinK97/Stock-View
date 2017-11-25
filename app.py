from flask import Flask, render_template, flash, redirect, url_for, session, logging
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='templates', static_folder='static')
mysql = MySQL()
# MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ashwin'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost:3306'
mysql.init_app(app)

@app.route('/')
def home():
	return render_template('homepage.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
	app.run(debug = True, port=8080)