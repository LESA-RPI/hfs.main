var path = require('path');
var http = require('http');
var fs = require('fs');

var dir = path.join(__dirname, 'public');

var mime = {
    html: 'text/html',
    txt: 'text/plain',
    css: 'text/css',
    gif: 'image/gif',
    jpg: 'image/jpeg',
    png: 'image/png',
    svg: 'image/svg+xml',
    js: 'application/javascript'
};

function fileAPI(res, file) {
	var type = mime[path.extname(file).slice(1)] || 'text/plain';
    var s = fs.createReadStream(file);
    s.on('open', function () {
        res.setHeader('Content-Type', type);
        s.pipe(res);
    });
    s.on('error', function () {
        res.setHeader('Content-Type', 'text/plain');
        res.statusCode = 404;
        return res.end('Not found');
    });
}

var server = http.createServer(function (req, res) {
    var reqpath = req.url.toString().split('?')[0];
	
	// Only accept GET requests from here onward
    if (req.method !== 'GET') {
        res.statusCode = 501;
        res.setHeader('Content-Type', 'text/plain');
        return res.end('Method not implemented');
    }
	if (reqpath.startsWith('/api/file/')) {
		
		return fileAPI(res, path.join(dir, reqpath.replace('/api/file', '')));
	}

	// Default to the index page
	return fileAPI(res, path.join(dir, reqpath.replace(/\/$/, '/index.html')));
});

server.listen(3000, function () {
    console.log('Listening on http://localhost:3000/');
});