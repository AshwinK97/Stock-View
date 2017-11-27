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