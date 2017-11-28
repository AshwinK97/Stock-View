# SOFE3700 Final Project
This repository contains files for the data management systems final project.

## Overview
This project will provide stock information for various companies within the last 10 years. This will be used to help analyze the price of a company's stock over a period of time. Using this data, users can analyze and predict future trends for a specific company, and make comparisons between multiple companies.

## Setup and Installation
* Clone the repository to your local machine
* Make sure you have python 2.7 installed and it is added to your `$PATH`
* Make sure you have a recent version of pip installed and it is added to your `$PATH`
* Open a terminal and `cd` into the project directory 
* Run the command `python app.py` to start the server
* If you do not already have a database.db file, the setup will make the necessary API calls and create a SQLite database under `db/database.db`
* This process can take up to 30 minutes depending on your internet connection
* The setup will then make sure you have the following python packages installed
  * Flask
  * sqlite3
  * plotly
  * numpy
  * pandas
* Make sure there were no errors installing these packages
* In your terminal you should see `* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)`
* You can now open a web browser and enter `http://127.0.0.1:8080` into the search bar

## API

Our api allows users to query our database for datasets and retrieve them as JSON objects. These datasets can be used for analysis and other similar projects.

Ex - Get up to 100 rows of Google stock information  
```http://localhost:8080/api/GOOGL?rows=100```

Ex - Get all rows of Apple stock information, between January 1, 2016 and January 1, 2017  
```http://localhost:8080/api/AAPL?date-start=2016-1-1&date-end=2017-1-1```

Ex - Get up to 500 volumes of Tesla stock, before July 5, 2014  
```http://localhost:8080/api/TSLA?col=volume&date-end=2014-7-5&rows=500```

Ex - Get all the closes of Microsoft stock, after November 10, 2015  
```http://localhost:8080/api/MSFT?col=close&date-start=2015-11-10```

## Views

#### Homepage
```
http://localhost:8080/
```
The homepage shows a list of stocks that are queriable in the database. Each one of these links to their relevent stock page.

#### Stock Page
```
http://localhost:8080/stock/<ticker_id>/<page>
```
The stock page shows a list of entries sorted by date for a specified `ticker_id`. It will only show 50 entries at a time based on which page you are currently on. From here you can navigate to the graph page for this stock, or you load the next 50 entries.

#### Graph page
```
http://localhost:8080/graph/<ticker_id>
```
The graph page shows a candlestick plot of the last 500 rows of data for the specified `ticker_id`. The candlestick will show increases and decreases in the stock value, as well as the individual numerical values for each point. The plot has many functions such as zooming, panning and selecting values. You can also export the plot as a .png, or upload it the cloud to edit it as a spread sheet.

#### Graph with volume
```
http://localhost:8080/graph/<ticker_id>?Volume=on
```
This page will contain the candlestick plot for the specified stock as well a graph of the volume data for that stock. The volume graph will have all of the same features as the above graph.

#### Graph date range
```
http://localhost:8080/graph/<ticker_id>?date_start=<date-start>&date_end=<date_end>
```
This page will contain the candlestick plot for the specifeid stock but it will be narrowed down to only the information within the specified dates.

#### Compare form
```
http://localhost:8080/compare
```
The compare page will display 3 column select form that allows the user to pick 2 ticker ids specifying which two stocks they would like to compare, as well as the individual attribute they would like to focus on. Upon submitting a valid selection, the page will reload with the newly produced graph

#### Compare graphs
```
http://localhost:8080/compare?compare1=<ticker1_id>&compare2=<ticker2_id>&attr=<attribute>
```
The compare graphs page will take the `compare1` and `compare2` values as ticker_ids and construct a single graph with both data sets, comparing the attribute speccified by `attr`. The graphs will have all the same features as those on the graph page. The compare form from the view will still be at the bottom of the page, and the user can select a new set of stocks and attributes to compare with.

## Images
Comparison of Tesla and Amazon
![Tesla vs AMAZON](https://i.imgur.com/3Q4PEdw.png)

Comparison of NVIDIA and AMD
![NVIDIA vs AMD](https://i.imgur.com/IWhQvsM.png)

Comparison of Qualcomm and Cisco
![Qualcom vs Cisco](https://i.imgur.com/zY7ND9l.png)

Comparison of IBM and HP
![IBM vs HP](https://i.imgur.com/r0xjrvV.png)
