from test import *
from plot import *

set_number_of_tests(1)
set_test_number(1)
set_test_passed(0)

init_test_file(os.path.splitext(os.path.basename(__file__))[0])
blockPrint()

# Test candlestick
parameters = [5, 76, 54, 99, 45, 'Date', 'Price']
log_test("ask_player", {"x": 5, "open": 54, "close": 76, "high": 99, "low": 45, "type": 'candlestick', "xaxis": 'Date', "yaxis": 'Price'}, parameters, candlestick(*parameters))

# # Test bar
# parameters = ["X"]
# log_test("ask_player", "tested", parameters, "Your turn Player X")

# # Test line
# parameters = ["X"]
# log_test("ask_player", "tested", parameters, "Your turn Player X")

# # Test layout
# parameters = ["X"]
# log_test("ask_player", "tested", parameters, "Your turn Player X")

summarize_tests()
close_test_file()