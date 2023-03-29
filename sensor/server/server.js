const path = require('path');
const http = require('http');
const fs = require('fs');
const os = require('os');

const CONFIG = require('./config.json');
const DIR = path.join(__dirname, 'public');

const promisify = require('util').promisify;

///////////////
/* Start BLE */
///////////////
const pyshell = require('python-shell');
const PY_OPTIONS  = {
	pythonOptions: ['-u'], // get print results in real-time
	pythonPath: CONFIG['py-path'],
	mode: 'json'
}
var shell = new pyshell.PythonShell(CONFIG['bt-path'], PY_OPTIONS)
	.on('stderr', function (stderr) {console.log('ERROR! ${stderr}')})
	.on('error', function (error) {console.log('ERROR! ${error}')})
	.on('message', function (message) {
	  // received a message sent from the Python script (a simple "print" statement)
	  console.log(message);
	})
	.on('close', function (code) {
	  console.log('The exit code was: ' + code);
	  console.log('finished');	  
	});
const CMD = { SET_RUNNABLE_CMD: 2, GET_DEVICE_LIST: 3, SET_RUN_FREQUENCY: 4 }
DEVICES = {}

/////////////////////////
/* Database Access API */
/////////////////////////
const { Client } = require('pg')
async function dbAPI(id, limit) {
	console.log('dbAPI: start');
	const client = new Client(CONFIG["postgres"]);
	
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

/////////////////////
/* File Access API */
/////////////////////
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

/////////////////
/* Server Init */
/////////////////
function waitForEvent( emitter, eventType, func ){
    return new Promise( function( resolve, reject ){
        emitter.once( eventType, resolve.bind(func) )
    })
}
const mime = { html: 'text/html', txt: 'text/plain', jpg: 'image/jpeg', json: 'application/json', css: 'text/css' };
var server = http.createServer(async function (req, res) {
	console.log('server: request');
    var reqpath = req.url.toString().split('?')[0];
	if (req.method === 'POST') {
		console.log('server: post API');
		var req_body = '';
		req.on('data', function(data) { req_body += data; });
		await waitForEvent(req, 'end', function() {});
		// todo: get request body
		console.log(JSON.parse(req_body))
		shell.send(JSON.parse(req_body));
		msg_json = await waitForEvent(shell, 'message', function(msg){return msg;});
		res.setHeader('Content-Type', mime.json);
		res.statusCode = 200;
		console.log(JSON.stringify(msg_json));
		return res.end(JSON.stringify(msg_json));
	}
	// Only accept GET requests from here onward
    if (req.method !== 'GET') {
        res.statusCode = 501;
		console.log('huh')
        res.setHeader('Content-Type', 'text/plain');
        return res.end('Method not implemented');
    }
	if (reqpath.startsWith('/api/file/')) {
		console.log('server: file API');
		return fileAPI(res, path.join(DIR, reqpath.replace('/api/file', '')));
	}
	if (reqpath.startsWith('/dev/restart/')) {
		console.log('server: restarting');
		import { spawn } from "child_process";
		const process = spawn("sh", ["-c", "sudo systemctl restart hfs-local.service"]);
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
	if (reqpath.startsWith('/api/sensors/')) {
		console.log('server: sensor API');
		shell.send({cmd: CMD.GET_DEVICE_LIST, addr: "", data: 0});
		shell.once('message', function (message_json) {
			res.setHeader('Content-Type', mime.json);
			res.statusCode = 200;
			return res.end(message_json);
		});
	}
	// Default to the index page
	return fileAPI(res, path.join(DIR, reqpath.replace(/\/$/, '/index.html')));
}).listen(3000, function () {
    console.log('Listening on http://localhost:3000/');
});

process.on('SIGINT', function() {
	console.log('\nSIGINT detected, shutting down server');
	server.close();
	shell.end();
	process.exit();
});
process.on('uncaughtException', err => {
  console.log(`Uncaught Exception: ${err.message}`)
  process.exit(1)
})
process.on('exit', function(code) {
	console.log(`exit ${code} detected, shutting down server`);
	server.close();
	shell.end();
	process.exit();
});
