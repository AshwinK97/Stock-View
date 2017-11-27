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

def layout(date = [], showlegend=True):
	return {
		"dragmode": 'turntable', 
		"margin": {"r": 10, "t": 25, "b": 40, "l": 60},
		"showlegend": showlegend,
		"legend": {"orientation": "h"},
        "xaxis": {
            "autorange": False, 
            "domain": [0, 1], 
            "range": date,
            "type": "date"
        },
        "yaxis": {
            "autorange": True,
            "rangemode": "normal",
            "type": "linear"
        }
	}