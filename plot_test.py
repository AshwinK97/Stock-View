from test import *
from plot import *
import random

set_number_of_tests(4)
set_test_number(1)
set_test_passed(0)

init_test_file(os.path.splitext(os.path.basename(__file__))[0])
blockPrint()

# Setup variables
x = random.randint(0, 100)
y = random.randint(0, 100)
close = random.randint(0, 100)
open = random.randint(0, 100)
high = random.randint(0, 100)
low = random.randint(0, 100)
xaxis='Date'
yaxis='Price'
color='#17BECF'
name = 'Testing Set'
date = []
showlegend=True

# Test candlestick
parameters = [x, close, open, high, low, xaxis, yaxis]
log_test("candlestick", {
		"x": x,
		"open": open,
		"close": close,
		"high": high,
		"low": low,
		"type": 'candlestick',
		"xaxis": xaxis,
		"yaxis": yaxis
	}, parameters, candlestick(*parameters))

# Test bar
parameters = [name, x, y]
log_test("bar", {
		"x": x,
		"y": y,
		"name": name,
		"type": 'bar'
	}, parameters, bar(*parameters))

# Test line
parameters = [name, x, y, color]
log_test("line", {
		"type": "scatter",
		"mode": "lines",
		"name": name,
		"x": x,
		"y": y,
		"line": {color: color}
	}, parameters, line(*parameters))

# Test layout
parameters = [date, showlegend]
log_test("layout", {
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
	}, parameters, layout(*parameters))

summarize_tests()
close_test_file()