def candlestick(x, close, open, high, low, xaxis='Date', yaxis='Price'):
	return {
		"x": x,
		"open": open,
		"close": close,
		"high": high,
		"low": low,
		"type": 'candlestick',
		"xaxis": xaxis,
		"yaxis": yaxis
	}

def line(name, x, y, color='#17BECF'):
	return {
		"type": "scatter",
		"mode": "lines",
		"name": name,
		"x": x,
		"y": y,
		"line": {color: color}
	}

def bar(name, x, y):
	return {
		"x": x,
		"y": y,
		"name": name,
		"type": 'bar'
	}

def layout():
	return {
		"dragmode": 'zoom', 
		"margin": {"r": 10, "t": 25, "b": 40, "l": 60},
		"showlegend": True,
		"legend": {"orientation": "h"}
	}