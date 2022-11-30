# postgresql-js

[![npm version](https://badge.fury.io/js/postgresql-js.svg)](https://badge.fury.io/js/postgresql-js)
[![npm downloads](https://img.shields.io/npm/dt/postgresql-js.svg)](https://www.npmjs.com/package/postgresql-js)

[![NPM](https://nodei.co/npm/postgresql-js.png?downloads=true&downloadRank=true&stars=true)](https://nodei.co/npm/postgresql-js/)

A simple library that lets you control and query local PostgreSQL server.

**Note:** It is built over `psql` CLI interface, so it won't work unless `psql` is executable through terminal.

## How to install?

You need to have Node.js installed on your system before you can use this package. Get it here: [Node.js](https://nodejs.org/)

Once you have Node.js and NPM setup, the installation is as simple as running a command.

### Linux/Mac

    npm install -s postgresql-js

### Windows

Within a command prompt window with administrative privileges:

    npm install -s postgresql-js

## How to use?

You can initialize the library to use a particular database by passing the name:

    const Database = require('postgresql-js');
    Database.initialize('my_database');

------

To execute queries or PostgreSQL commands like /c to get raw response, you can use the function `execute`:

    Database.execute('CREATE TABLE my_table (id SERIAL, text VARCHAR (100)');
    Database.execute('INSERT INTO my_table ("text") VALUES (\'the value\')');

------

For queries where you expect JSON array as response, you can call the function `query`:

    Database.query('SELECT * FROM my_table');

The query function returns something like:

    [{ id: '1', text: 'the value' }]

------

For SELECT queries, you can call the function `get` with table name and optional conditions:

    Database.get('SELECT * FROM my_table');
    Database.get('SELECT * FROM my_table', '"id"=\'1\'');

The query function returns something like:

    [{ id: '1', text: 'the value' }]

------

For INSERT queries, you can call the function `insert` with table name and object to insert:

    Database.insert('my_table', { text: 'another value' });

It returns the number of items inserted.

------

For UPDATE queries, you can call the function `update` with table name, object with updated content and condition:

    Database.update('my_table', { text: 'yet another value' }, '"id"=\'2\'');

It returns the number of items updated.

------

For DELETE queries, you can call the function `delete` with table name and optional conditions:

    Database.delete('my_table', '"id"=\'2\'');
    Database.delete('my_table');

It returns the number of items deleted.

## How to contribute?

Feel free to raise a pull request!
