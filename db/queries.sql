-- Example api calls
-- https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?rows=1000
-- https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?column=4&sort_order=asc&collapse=quarterly&trim_start=2012-01-01&trim_end=2013-12-31

-- create Tickers table
CREATE TABLE Tickers ( 
	id INT NOT NULL,
	name VARCHAR ( 45 ),
	company VARCHAR ( 45 ),
	PRIMARY KEY(id) 
)

-- new Prices table
CREATE TABLE Prices ( 
	price_id INTEGER NOT NULL PRIMARY KEY autoincrement, 
	ticker_id INT NOT NULL, 
	date VARCHAR(30) NOT NULL, 
	open DECIMAL NULL, 
	high DECIMAL NULL, 
	low DECIMAL NULL, 
	close DECIMAL NULL, 
	volume DECIMAL NULL, 
	FOREIGN KEY (ticker_id) REFERENCES Tickers (id), 
	UNIQUE(ticker_id, date) ON CONFLICT REPLACE 
)

-- new Prices entry
INSERT INTO Prices(ticker_id, date, open, high, low, close, volume) 
VALUES (1, 1, "2017-11-24", 1054.39, 1060.07, 1051.92, 1056.52, 825342)