from flask import Flask, render_template
import sqlite3 as sql
import json, plotly
import numpy as np
import pandas as pd

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
	return cur

@app.route('/')
def home():
	return render_template("homepage.html", rows = select("select * from tickers", []))

@app.route('/about')
def about():
	return render_template('about.html')

## move to seperate file
@app.route('/view1')
def view1():
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute('''
	select Tickers.name, Prices.date, Prices.open, Prices.close, Prices.high, Prices.low, Prices.volume
	from Prices 
	join Tickers on Tickers.id = Prices.ticker_id
	where Prices.ticker_id = 1
	order by price_id ASC
	''')

	columns = list(map(lambda col: col[0], cur.description))
	rows = cur.fetchall();
	
	df = pd.DataFrame(rows)
	df.columns = columns
	
	tables = [df.head(25).to_html(classes='pure-table')]

	graphs = [{
		"data": [{
				"x": df.date.tolist(),
				"open": df.open.tolist(),
				"close": df.close.tolist(),
				"high": df.high.tolist(),
				"low": df.low.tolist(),
				"type": 'candlestick',
				"xaxis": 'Date',
				"yaxis": 'Price'
		}],
		"layout": {
			"title": df.name[0],
			"dragmode": 'zoom', 
			"margin": {
				"r": 10, 
				"t": 25, 
				"b": 40, 
				"l": 60
			}
		}
	}]

	# Add "ids" to each of the graphs to pass up to the client
	# for templating
	ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

	# Convert the figures to JSON
	# PlotlyJSONEncoder appropriately converts pandas, datetime, etc
	# objects to their JSON equivalents
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template("view1.html", tables = tables, ids = ids, graphJSON = graphJSON)

@app.route('/stock/<int:ticker>')
def stock(ticker):
	#ticker_info = select("select name, company from Tickers where id = ?", ticker)
	price_select_all = select("select * from prices where ticker_id = ? order by price_id asc", ticker)

	price_rows = price_select_all.fetchall()
	price_columns = list(map(lambda col: col[0].title().replace('_', ''), price_select_all.description))

	price = pd.DataFrame(price_rows)
	price.columns = price_columns

	#info = pd.DataFrame(ticker_info)

	return render_template("stock.html", table = price.to_html(classes='pure-table', index=False), info = {"company": 'Google', "name": 'GOOGL'})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
	app.run(debug=True, port=8080)
