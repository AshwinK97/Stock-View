import sqlite3

conn = sqlite3.connect('db/database.db')
print "Database opened successfully"

conn.execute('CREATE TABLE tickers(id INT NOT NULL, name VARCHAR(45) NULL, PRIMARY KEY (id))')
print "Tickers table created"

conn.close()