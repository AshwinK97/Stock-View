from flask import Flask, render_template, url_for
from flaskext.mysql import MySQL
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("select * from tickers")
	rows = cur.fetchall();
	return render_template("homepage.html",rows = rows)

@app.route('/about')
def about():
	return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
	app.run(debug = True, port=8080)