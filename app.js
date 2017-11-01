var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');

var app = express();
app.disable('x-powered-by'); // block server info

// view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // path to views

// path to css and img files
app.use(express.static(path.join(__dirname, 'public')));

// body parser middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// routes go here
app.get('/', function(req, res) {
	res.render('index', {
		title: 'Homepage'
	});
});

// start the server
app.listen(8080, function() {
	console.log('Server started on port 8080');
});