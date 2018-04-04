import sys, os

global number_of_tests
global test_number
global test_passed
global test_log

# Set Global Variables
def set_number_of_tests(value):
  global number_of_tests
  number_of_tests = value

def set_test_number(value):
  global test_number
  test_number = value

def set_test_passed(value):
  global test_passed
  test_passed = value

# Get Global Variables
def get_number_of_tests():
  global number_of_tests
  print(number_of_tests)
  return number_of_tests

def get_test_number():
  global test_number
  print(test_number)
  return test_number

def get_test_passed():
  global test_passed
  print(test_passed)
  return test_passed

# Init test file
def init_test_file(title):
  global test_log
  test_log = open("{}.txt".format(title), "w+")

# Init test file
def close_test_file():
  test_log.close()

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Log individual tests
def log_test(name, expected, parameters, actual):
  global number_of_tests
  global test_number
  global test_passed
  result = actual == expected

  if(result):
    result = "Passed\n"
    test_passed += 1
  else:
    result = "Failed\n"

  test_log.write("[{}/{}]: Testing {}() with Parameters (".format(test_number, number_of_tests, name))
  
  for parameter in parameters:
    if (parameter == parameters[-1]):
      test_log.write(str(parameter))
    else:
      test_log.write("{}, ".format(parameter))

  test_log.write(")\n")
  test_log.write("Expected: {}\n".format(expected))
  test_log.write("Actual: {}\n".format(actual))
  test_log.write("Result: {}{}\n\n".format(result, '-'*8))

  test_number += 1

# Summarize all tests
def summarize_tests():
  test_log.write("Tests Ran: {}\n".format(number_of_tests))
  test_log.write("Successful Runs: {}/{}\n".format(test_passed, number_of_tests))
  test_log.write("Failed Runs: {}/{}".format(number_of_tests - test_passed, number_of_tests))

# # Block all print statements
# blockPrint()

# # Test ask_player
# parameters = ["X"]
# log_test("ask_player", ask_player(*parameters), parameters, "Your turn Player X")

# summarize_tests()
# test_log.close()