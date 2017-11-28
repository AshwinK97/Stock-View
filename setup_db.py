import sqlite3, urllib2

# list of urls for api calls
urls = [
	'https://www.quandl.com/api/v1/datasets/WIKI/GOOGL.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/AMZN.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/NVDA.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/TSLA.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/INTC.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/IBM.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/CSCO.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/AMD.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/ORCL.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/QCOM.csv?rows=100',
	'https://www.quandl.com/api/v1/datasets/WIKI/HPQ.csv?rows=100'
]
# list of prepared statements to execute queries
queries = [
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (1, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (2, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (3, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (4, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (5, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (6, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (7, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (8, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (9, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (10, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (11, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (12, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (13, ?, ?, ?, ?, ?, ?)'
]

# perform insert transaction
def insert(conn, url, query, cols):
	csv = urllib2.urlopen(url).read().split('\n') # get csv from api
	for i, row in enumerate(csv): # iterate through each row
		if i == 0: # skip heading row
			continue
		data = row.strip().split(',')[:-cols] # get specific number of columns
		if len(data) == 6: # if correct amount of data was retrieved, execute query
			try:
				conn.execute(query, data)
				conn.commit()
			except:
				print "error: could not insert"
				return False
	return True

def setup_db():
	# create database connection
	conn = sqlite3.connect('db/database.db')
	print "database.db - connected"

	# create tickers table if it does not already exist
	conn.execute('CREATE TABLE if not exists Tickers ( id INT NOT NULL, name VARCHAR ( 45 ), company VARCHAR ( 45 ), PRIMARY KEY(id) )')
	# add the tickers we are using for our project
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (1, 'GOOGL', 'Alphabet Inc Class A')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (2, 'MSFT', 'Microsoft Corporation')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (3, 'AAPL', 'Apple Inc.')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (4, 'AMZN', 'Amazon.com, Inc.')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (5, 'NVDA', 'NVIDIA Corporation')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (6, 'TSLA', 'Tesla Inc')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (7, 'INTC', 'Intel Corporation')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (8, 'IBM', 'IBM Common Stock')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (9, 'CSCO', 'Cisco Systems, Inc.')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (10, 'AMD', 'Advanced Micro Devices, Inc.')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (11, 'ORCL', 'Oracle Corporation')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (12, 'QCOM', 'QUALCOMM, Inc.')''')
	conn.execute('''INSERT INTO Tickers (id, name, company) VALUES (13, 'HPQ', 'Hewlett-Packard Inc.')''')

	print "Tickers table - done"

	# create prices table if it does not already exist
	conn.execute('''
		CREATE TABLE if not exists Prices ( 
		price_id INTEGER NOT NULL PRIMARY KEY autoincrement, 
		ticker_id INT NOT NULL, 
		date VARCHAR(30) NOT NULL, 
		open DECIMAL NULL, 
		high DECIMAL NULL, 
		low DECIMAL NULL, 
		close DECIMAL NULL,
		volume DECIMAL NULL, 
		FOREIGN KEY (ticker_id) REFERENCES Tickers (id), 
		UNIQUE(ticker_id, date) ON CONFLICT REPLACE )
	''')
	print "Prices table - done"

	# preform each api call
	for url, query in zip(urls, queries):
		if insert(conn, url, query, 7):
			print url, "- success"

	conn.close()