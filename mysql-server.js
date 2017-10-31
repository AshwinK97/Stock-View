/*
Example of how to connect to mysql server with mysql node module
*/

// include mysql node module
var mysql = require('mysql');

// connection string
var connection = mysql.createConnection({
  host     : 'localhost',
  port     : '3306',
  user     : 'root',
  password : 'ashwin97',
  database : 'Lab6'
});

// connect and check if connection was successfull
connection.connect(function(err) {
  if (err) {
    console.error('error connecting: ' + err.stack);
    return;
  }

  console.log('connected as id ' + connection.threadId);
});

// query the database
connection.query('SELECT * FROM Employees;', function (err, rows, fields) {
	if (err) throw err // if error in query

	// rows contains a list of objects
	// loop through the list, get the data from each object
	for (var i = 0; i < rows.length; i++) {
		var row = rows[i];
		console.log(row.EmployeeName + " --> " + row.Title);
	}
})

// kill the connection
connection.end()