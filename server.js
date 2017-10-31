var http = require("http");

http.createServer(function (request, response) {
	// Send the HTTP header
	// HTTP Status: 200 :OK
	// Content Type: text/plain
	response.writeHead(200, {'Content-Type': 'text/plain'});

	// Send the response body as "Hello World"
	response.end('Hello World\n');
}).listen(8080);

console.log('Server is running at localhost:8080');
