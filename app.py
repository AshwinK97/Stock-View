from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)

# perform insert query
def select(query, params):
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	try:
		cur.execute(query, params)
	except:
		return "error: could not select"
	return cur.fetchall();

@app.route('/')
def home():
	return render_template("homepage.html", rows = select("select * from tickers", []))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/stock/<ticker>')
def stock(ticker):
	info = select("select name, company from Tickers where id = ?", ticker)
	rows = select("select * from prices where ticker_id = ? order by price_id asc", ticker)
	return render_template("stock.html", rows = rows, info = info)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
	app.run(debug=True, port=8080)
