# import setup
from setup import setup
setup() # run inital setup

# import necessary packages
from flask import Flask, render_template, request
# import sqlite3 as sql
import json, plotly
import numpy as np
import pandas as pd

# file imports
from request import *
from indicator import *

app = Flask(__name__)

# Page routes
@app.route('/')
def home():
	return render_template("homepage.html", rows = query("select * from Tickers", []).fetchall())

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/about/api')
def api_info():
	return render_template('api_info.html')

@app.route('/compare', methods=['GET'])
def compare():
	visible, title = "invisible", ""
	ids, graphJSON = [], []

	if len(request.args) == 3:
		# Setup cursors from db queries for data
		ticker1_cur = query('select date, {} from Prices where ticker_id = ?'.format(request.args.get('attr')), [request.args.get('compare1')])
		ticker2_cur = query('select date, {} from Prices where ticker_id = ?'.format(request.args.get('attr')), [request.args.get('compare2')])
		names_cur = query('select id, name from tickers where id = ? or id = ?', [request.args.get('compare1'), request.args.get('compare2')])
		
		# Create dataframes out of queried data
		names_df = setup_df(names_cur, index=True)
		ticker1_df = setup_df(ticker1_cur)
		ticker2_df = setup_df(ticker2_cur)

		# Checks for a volume attr
		# returns a line display, else a candlestick
		data = is_volume(request.args, [names_df, ticker1_df, ticker2_df])

		date = [ticker1_df.date.tolist()[0], ticker1_df.date.tolist()[-1]]
		
		graphs = [{
			"data": data,
			"layout": layout(date)
		}]

		ids = get_ids(graphs)

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
	data = []
	graphs = []
	ticker_info = query("select name, company from Tickers where id = ?", [ticker]).fetchone()
	cur = query('''select Prices.date, Prices.open, Prices.close, Prices.high, Prices.low, Prices.volume
		from Prices join Tickers on Tickers.id = Prices.ticker_id 
		where Prices.ticker_id = ? order by price_id ASC limit 500''', [ticker]
	)

	# Setup dataframe
	df = setup_df(cur)

	# if no rows returned, page not found
	if df.empty:
		return render_template('404.html')

	# get absolute date range
	date = [df.date.tolist()[-1], df.date.tolist()[0]]

	# if parameters were given
	if(request.args.get('date_start') != None):
			date = [request.args.get('date_start'), request.args.get('date_end')]

	# get candlestick plot data
	plot_candlestick = candlestick(df.date.tolist(), df.open.tolist(), df.close.tolist(), df.high.tolist(), df.low.tolist())
	data.append(plot_candlestick)

	graphs.append({
		"data": data,
		"layout": layout(date, showlegend=False)
	})

	if request.args.get('Volume') == 'on':
			volume = [(Volume(ticker, date))]
			graphs.append({
				"data": volume,
				"layout": layout(date)
			})

	# Add "ids" to each of the graphs to pass up to the client for templating
	ids = get_ids(graphs)

	# Convert the figures to JSON
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template("graph.html", ids = ids, graphJSON = graphJSON, name = ticker_info[0], company = ticker_info[1], ticker = ticker)

@app.route('/stock/<int:ticker>/<int:page>')
def stock(ticker, page):
	# select 50 rows after the specified offset
	price_select_all = query('''select (select count(*) from prices as t2 where t2.price_id <= t1.price_id) 
		as row, date, open, high, low, close, volume from Prices as t1 where ticker_id = ? 
		order by price_id asc limit 50 offset ?''', [ticker, page*50]
	)
	ticker_info = query("select id, name, company from Tickers where id = ?", [ticker]).fetchone()
	
	# Setup df
	price = setup_df(price_select_all)

	# if no rows returned, page not found
	if price.empty:
		return render_template('404.html'), 404

	# Create dataframe from query and convert to html table
	price.columns = list(map(lambda col: col[0].title().replace('_', ''), price_select_all.description))
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
		col = request.args.get('col')
		
		if col == None:
			col = 'close'

		string = '''select Prices.{} from Prices where Prices.ticker_id = (select tickers.id from Tickers where name = ?)'''.format(col)

		string = setup_api_query(string, request.args, params)

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
	app.run(port=8080)
