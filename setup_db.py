import sqlite3, urllib2

# perform insert transaction
def insert(url, query, cols):
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
				print "error executing insert statement"
				return False
	return True

# create database connection
conn = sqlite3.connect('db/database.db')
print "database.db - connected"

# create tickers table if it does not already exist
conn.execute('CREATE TABLE if not exists Tickers ( id INT NOT NULL, name VARCHAR(45) NULL, PRIMARY KEY (id) )')
print "Tickers table - done"

# create prices table if it does not already exist
conn.execute('''
	CREATE TABLE if not exists Prices ( 
	ticker_id INT NOT NULL PRIMARY KEY, 
	date VARCHAR(30) NULL, 
	open DECIMAL NULL, 
	high DECIMAL NULL, 
	low DECIMAL NULL, 
	close DECIMAL NULL, 
	volume DECIMAL NULL, 
	exdiv DECIMAL NULL, 
	spratio DECIMAL NULL, 
	FOREIGN KEY (ticker_id) REFERENCES Tickers (id) )
''')
print "Prices table - done"

# list of urls for api calls
urls = [
	'https://www.quandl.com/api/v1/datasets/WIKI/GOOGL.csv?rows=2000',
	'https://www.quandl.com/api/v1/datasets/WIKI/MSFT.csv?rows=2000',
	'https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?rows=2000',
	'https://www.quandl.com/api/v1/datasets/WIKI/AMZN.csv?rows=2000'
]
# list of prepared statements to execute queries
queries = [
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (1, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (2, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (3, ?, ?, ?, ?, ?, ?)',
	'INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) VALUES (4, ?, ?, ?, ?, ?, ?)',
]

# preform each api call
for url, query in zip(urls, queries):
	if insert(url, query, 7):
		print url, "- success"

conn.close()