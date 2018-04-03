import sqlite3 as sql
import pandas as pd
from plot import *

# used to perform insert queries
def query(query, params):
	con = sql.connect("db/database.db")
	con.row_factory = sql.Row
	cur = con.cursor()

	cur.execute(query, params)
	return cur

def is_volume(args, dataframes):
  names_df, ticker1_df, ticker2_df = dataframes

  if args.get('attr') == 'volume':
    ticker1_data = bar(names_df.name[int(args.get('compare1'))], ticker1_df.date, ticker1_df[args.get('attr')])
    ticker2_data = bar(names_df.name[int(args.get('compare2'))], ticker2_df.date, ticker2_df[args.get('attr')])
  else:
    ticker1_data = line(names_df.name[int(args.get('compare1'))], ticker1_df.date, ticker1_df[args.get('attr')])
    ticker2_data = line(names_df.name[int(args.get('compare2'))], ticker2_df.date, ticker2_df[args.get('attr')])
  
  return [ticker1_data, ticker2_data]

def setup_df(cursor, index = None):
  df = pd.DataFrame(cursor.fetchall())
  df.columns = list(map(lambda col: col[0], cursor.description))
  if(index != None):
    df.set_index('id', inplace=True)
  
  return df

def get_ids(graphs):
  return ['{}'.format(i) for i, _ in enumerate(graphs)]

def setup_api_query(query, args, params):
  # start date was specified
  if args.get('date-start'):
    query += " and Prices.date >= ?"
    params.append(args.get('date-start'))
  
  # end date was specified
  if args.get('date-end'):
    query += " and Prices.date <= ?"
    params.append(args.get('date-end'))

  # row limit was specified
  if args.get('rows'):
    query += " limit ?"
    params.append(args.get('rows'))
  
  return query