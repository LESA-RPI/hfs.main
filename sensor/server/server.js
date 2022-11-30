var path = require('path');
var http = require('http');
var fs = require('fs');

var dir = path.join(__dirname, 'public');
var os = require('os');

const { Client } = require('pg');
const CLIENT_DATA = {
	user: 'postgres',
	database: 'postgres',
	port: 5433,
	password: 'admin'
	};

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

async function dbAPI(id, limit) {
	const client = new Client(CLIENT_DATA);
	await client.connect();
	var res = null;
	if (id === '*') {
		res = await client.query(`SELECT * FROM data WHERE id=${id} ORDER BY timestamp LIMIT ${limit}`);
	} else {
		res = await client.query(`SELECT * FROM data ORDER BY timestamp LIMIT ${limit}`);
	}
	await client.end();
	return res.rows
}

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

var server = http.createServer(async function (req, res) {
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
	if (reqpath.startsWith('/api/db')) {
		let id = null;
		let limit = null;
		for (const param of req.url.toString().split('?')[1].split('&')) {
			if (param.split('=')[0] === 'id') { id = param.split('=')[1] }
			if (param.split('=')[0] === 'limit') { limit = param.split('=')[1] }
		}
		return res.end(JSON.stringify(await dbAPI(id, limit)));
	}

	// Default to the index page
	return fileAPI(res, path.join(dir, reqpath.replace(/\/$/, '/index.html')));
});

server.listen(3000, function () {
    console.log('Listening on http://localhost:3000/');
});