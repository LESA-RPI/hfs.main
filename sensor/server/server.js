var path = require('path');
var http = require('http');
var fs = require('fs');

var dir = path.join(__dirname, 'public');
var os = require('os');

const { Client } = require('pg');
const CLIENT_DATA = {
	user: 'postgres',
	database: 'postgres',
	port: 5432,
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
	console.log('dbAPI: start');
	const client = new Client(CLIENT_DATA);
	
	try {
		await client.connect();
	} catch (error) {
		console.error('dbAPI: error', error);
		return {}
	}
	
	console.log('dbAPI: connected');
	var res = null;
	if (id === '*') {
		console.log('dbAPI: id = *');
		res = await client.query(`SELECT * FROM data WHERE id=${id} ORDER BY timestamp LIMIT ${limit}`);
	} else {
		console.log('dbAPI: id != *');
		res = await client.query(`SELECT * FROM data ORDER BY timestamp LIMIT ${limit}`);
	}
	await client.end();
	console.log('dbAPI: end');
	return res.rows
}

function fileAPI(res, file) {
	console.log('fileAPI: start');
	var type = mime[path.extname(file).slice(1)] || 'text/plain';
    var stream = fs.createReadStream(file);
	
	var had_error = false;
	stream.on('finish', function() {if (!had_error) {fs.unlink(file); res.end();} });
    stream.on('open', function () {
        res.setHeader('Content-Type', type);
		console.log(type);
		console.log('fileAPI: found');
        stream.pipe(res);
    });
    stream.on('error', function () {
		had_error = true;
        res.setHeader('Content-Type', 'text/plain');
        res.statusCode = 404;
		console.log('fileAPI: error 404');
        return res.end('Not found');
    });
	console.log('fileAPI: end');
}

var server = http.createServer(async function (req, res) {
	console.log('server: request');
    var reqpath = req.url.toString().split('?')[0];
	// Only accept GET requests from here onward
    if (req.method !== 'GET') {
		console.log('server: GET');
        res.statusCode = 501;
        res.setHeader('Content-Type', 'text/plain');
        return res.end('Method not implemented');
    }
	if (reqpath.startsWith('/api/file/')) {
		console.log('server: file API');
		return fileAPI(res, path.join(dir, reqpath.replace('/api/file', '')));
	}
	if (reqpath.startsWith('/api/db')) {
		console.log('server: database API ');
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