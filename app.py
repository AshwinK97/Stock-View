from flask import Flask, render_template, request
import sqlite3 as sql
import json, plotly
import numpy as np
import pandas as pd

# file imports
from setup import setup
from plot import *

# setup() # run initial setup
app = Flask(__name__)

# used to perform insert queries
def query(query, params):
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	try:
		cur.execute(query, params)
	 	return cur
	except:
	 	return "error: could not return cursor"

# Page routes
@app.route('/')
def home():
	return render_template("homepage.html", rows = query("select * from Tickers", []).fetchall())

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/compare', methods=['GET'])
def compare():
	visible, title = "invisible", ""
	ids, graphJSON = [], []
	if len(request.args) == 3:
		ticker1_cur = query('select date, {} from Prices where ticker_id = ?'.format(request.args.get('attr')), [request.args.get('compare1')])
		ticker2_cur = query('select date, {} from Prices where ticker_id = ?'.format(request.args.get('attr')), [request.args.get('compare2')])
		names_cur = query('select id, name from tickers where id = ? or id = ?', [request.args.get('compare1'), request.args.get('compare2')])
		
		names_df = pd.DataFrame(names_cur.fetchall())
		names_df.columns = list(map(lambda col: col[0], names_cur.description))
		names_df.set_index('id', inplace=True)

		ticker1_df = pd.DataFrame(ticker1_cur.fetchall())
		ticker1_df.columns = list(map(lambda col: col[0], ticker1_cur.description))

		ticker2_df= pd.DataFrame(ticker2_cur.fetchall())
		ticker2_df.columns = list(map(lambda col: col[0], ticker2_cur.description))

		if request.args.get('attr') == 'volume':
			ticker1_data = bar(names_df.name[int(request.args.get('compare1'))], ticker1_df.date, ticker1_df[request.args.get('attr')])
			ticker2_data = bar(names_df.name[int(request.args.get('compare2'))], ticker2_df.date, ticker2_df[request.args.get('attr')])
		else:
			ticker1_data = line(names_df.name[int(request.args.get('compare1'))], ticker1_df.date, ticker1_df[request.args.get('attr')])
			ticker2_data = line(names_df.name[int(request.args.get('compare2'))], ticker2_df.date, ticker2_df[request.args.get('attr')])

		data = [ticker1_data, ticker2_data]

		graphs = [{
			"data": data,
			"layout": layout()
		}]

		ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

		# Convert the figures to JSON
		# PlotlyJSONEncoder appropriately converts pandas, datetime, etc
		# objects to their JSON equivalents
		graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

		visible = "" # no longer invisible

		title = "- {} with {} - {}".format(names_df.name[int(request.args.get('compare1'))], names_df.name[int(request.args.get('compare2'))], request.args.get('attr').title())

	tickers = query("select * from Tickers", []).fetchall()
	return render_template('compare.html', tickers = tickers, ids = ids, graphJSON = graphJSON, visible = visible, title = title)

@app.route('/graph/<int:ticker>')
def graph(ticker):
	ticker_info = query("select name, company from Tickers where id = ?", [ticker]).fetchone()
	cur = query('''select Prices.date, Prices.open, Prices.close, Prices.high, Prices.low, Prices.volume
		from Prices join Tickers on Tickers.id = Prices.ticker_id 
		where Prices.ticker_id = ? order by price_id ASC limit 100''', [ticker]
	)

	rows = cur.fetchall();
	# if no rows returned, page not found
	if len(rows) == 0:
		return render_template('404.html')
	columns = list(map(lambda col: col[0], cur.description))

	df = pd.DataFrame(rows)
	df.columns = columns

	# tables = [df.head(25).to_html(classes='pure-table', index=False)]
	
	#Testing new plot functions
	plot_candlestick = candlestick(df.date.tolist(), df.open.tolist(), df.close.tolist(), df.high.tolist(), df.low.tolist())
	#plot_line_close = line(ticker_info[0]+'.Close', df.date.tolist(), df.close.tolist())

	data = [plot_candlestick]#, plot_line_close]

	graphs = [{
		"data": data,
		"layout": layout()
	}]

	# Add "ids" to each of the graphs to pass up to the client for templating
	ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

	# Convert the figures to JSON
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template("graph.html", ids = ids, graphJSON = graphJSON, name = ticker_info[0], company = ticker_info[1])

@app.route('/stock/<int:ticker>/<int:page>')
def stock(ticker, page):
	# select 50 rows after the specified offset
	price_select_all = query('''select (select count(*) from prices as t2 where t2.price_id <= t1.price_id) 
		as row, date, open, high, low, close, volume from Prices as t1 where ticker_id = ? 
		order by price_id asc limit 50 offset ?''', [ticker, page*50]
	)
	ticker_info = query("select id, name, company from Tickers where id = ?", [ticker]).fetchone()
	
	# if no rows returned, page not found
	price_rows = price_select_all.fetchall()
	if len(price_rows) == 0:
		return render_template('404.html'), 404

	price_columns = list(map(lambda col: col[0].title().replace('_', ''), price_select_all.description))
	price = pd.DataFrame(price_rows)
	price.columns = price_columns
	table = price.to_html(classes='pure-table pure-table-bordered', index=False)

	return render_template("stock.html", table = table, info = ticker_info, page = page+1)

# API calls
@app.route('/api/<ticker_name>', methods=['GET'])
def api(ticker_name):
	# default query
	string = '''
		select Prices.date, Prices.open, Prices.high, Prices.low, Prices.close, Prices.volume 
		from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)
	'''
	# default parameter
	params = [ticker_name]

	# if parameters were given
	if len(request.args) != 0:
		# column was specified
		if request.args.get('col') == 'date':
			string = '''select Prices.date from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''
		elif request.args.get('col') == 'open':
			string = '''select Prices.open from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''
		elif request.args.get('col') == 'high':
			string = '''select Prices.high from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''
		elif request.args.get('col') == 'low':
			string = '''select Prices.low from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''
		elif request.args.get('col') == 'close':
			string = '''select Prices.close from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''
		elif request.args.get('col') == 'volume':
			string = '''select Prices.volume from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''

		# start date was specified
		if request.args.get('date-start'):
			string += " and Prices.date >= ?"
			params.append(request.args.get('date-start'))
		
		# end date was specified
		if request.args.get('date-end'):
			string += " and Prices.date <= ?"
			params.append(request.args.get('date-end'))

		# row limit was specified
		if request.args.get('rows'):
			string += " limit ?"
			params.append(request.args.get('rows'))

	# execute constructed query with specified parameters
	data = query(string, params).fetchall()
	
	# if no data was retrieved
	if len(data) == 0:
		return render_template('404.html'), 404

	# return data as JSON object
	return json.dumps([dict(ix) for ix in data])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True, port=8080)
