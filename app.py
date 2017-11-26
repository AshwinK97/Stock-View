from flask import Flask, render_template
from flaskext.mysql import MySQL
import sqlite3 as sql

app = Flask(__name__)

# https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?column=4&sort_order=asc&collapse=quarterly&trim_start=2012-01-01&trim_end=2013-12-31

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