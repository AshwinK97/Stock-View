from flask import Flask, render_template, request
import sqlite3 as sql
import json, plotly
import numpy as np
import pandas as pd

# file imports
from setup import setup

# setup() # run initial setup
app = Flask(__name__)

# perform insert query
def select(query, params):
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	try:
		cur.execute(query, params)
	 	return cur
	except:
	 	return "error: could not return cursor"

# Define routes
@app.route('/')
def home():
	return render_template("homepage.html", rows = select("select * from Tickers", []).fetchall())

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/compare', methods=['GET'])
def compare():
	visible = "invisible"
	if len(request.args) == 2:
		ticker1 = select('select date, close from Prices where ticker_id = ?', [request.args.get('compare1')])
		ticker2 = select('select date, close from Prices where ticker_id = ?', [request.args.get('compare2')])

		## kaushal's graph

		visible = ""

	tickers = select("select * from Tickers", []).fetchall()
	return render_template('compare.html', tickers = tickers, visible = visible)

## move to seperate file
@app.route('/graph/<int:ticker>')
def graph(ticker):
	ticker_info = select("select name, company from Tickers where id = ?", [ticker]).fetchone()
	cur = select('''select Prices.date, Prices.open, Prices.close, Prices.high, Prices.low, Prices.volume
		from Prices join Tickers on Tickers.id = Prices.ticker_id
		where Prices.ticker_id = ?
		order by price_id ASC''', [ticker])

	rows = cur.fetchall();
	columns = list(map(lambda col: col[0], cur.description))

	df = pd.DataFrame(rows)
	df.columns = columns

	tables = [df.head(25).to_html(classes='pure-table', index=False)]

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
			"title": ticker_info[0],
			"dragmode": 'zoom', 
			"margin": {
				"r": 10, 
				"t": 25, 
				"b": 40, 
				"l": 60
			},
			"showlegend": False
		}
	}]

	# Add "ids" to each of the graphs to pass up to the client
	# for templating
	ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

	# Convert the figures to JSON
	# PlotlyJSONEncoder appropriately converts pandas, datetime, etc
	# objects to their JSON equivalents
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template("graph.html", tables = tables, ids = ids, graphJSON = graphJSON, name = ticker_info[0], company = ticker_info[1])

@app.route('/stock/<int:ticker>/<int:page>')
def stock(ticker, page):
	# select 100 prices after the specified offset
	price_select_all = select('''
		select (select count(*) from prices as t2 where t2.price_id <= t1.price_id) as row, date, open, high, low, close, volume from Prices as t1 where ticker_id = ? 
		order by price_id asc limit 50 offset ?''', [ticker, page*100]
	)
	ticker_info = select("select id, name, company from Tickers where id = ?", [ticker]).fetchone()

	price_rows = price_select_all.fetchall()
	price_columns = list(map(lambda col: col[0].title().replace('_', ''), price_select_all.description))
	
	price = pd.DataFrame(price_rows)
	price.columns = price_columns
	table = price.to_html(classes='pure-table pure-table-bordered', index=False)

	return render_template("stock.html", table = table, info = ticker_info, page = page+1)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True, port=8080)
