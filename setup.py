import imp, pip, os
from setup_db import setup_db

# use pip to install the specified package
def import_or_install(package):
	import imp
	try:
	    imp.find_module(package)
	except ImportError:
	    pip.main(['install', package])

def setup():
	print "Running Setup"
	# check for required packages, install if needed
	packages = ["flask", "sqlite3", "plotly", "numpy", "pandas"]
	for p in packages:
		import_or_install(p)

	# check if database exists, create new if needed
	if not os.path.isfile('./db/database.db'):
		setup_db()

	print "Setup done"

