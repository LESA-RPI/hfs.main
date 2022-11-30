const assert = require('assert');
const Database = require('../index.js');

describe('# Database', function() {
    before(function() {
        Database.execute('CREATE DATABASE test_database');
    })

    describe('## initialize', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database.initialize);
        });

        it('should be able to initialize', function() {
            try {
                Database.initialize('test_database');
                assert.ok(true);
            } catch (error) {
                assert.fail(error);
            }
        });
    });

    describe('## execute', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database.execute);
        });
        
        it('should return the result of execution', function() {
            assert.equal('CREATE TABLE', Database.execute('CREATE TABLE test_table (id SERIAL, string VARCHAR (100), number INTEGER)'));
            assert.equal('INSERT 0 1', Database.execute('INSERT INTO test_table ("string", "number") VALUES (\'some\', 50)'));
        });
    });

    describe('## query', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database.query);
        });

        it('should return an array', function() {
            assert.notEqual(undefined, Database.query('SELECT * FROM test_table').length);
        });

        it('should return the result of query', function() {
            assert.deepEqual([{ id: '1', string: 'some', number: 50 }], Database.query('SELECT * FROM test_table'));
        });

        it('should return the numerical values as number', function() {
            assert.equal('number', typeof (Database.query('SELECT * FROM test_table')[0].number));
        });
    });

    describe('## insert', function() {
        const testItem = { string: 'other' };

        it('should be of type function', function() {
            assert.equal('function', typeof Database.insert);
        });

        it('should return number of items inserted', function() {
            assert.equal('1', Database.insert('test_table', testItem));
        });

        it('should be returned in query', function() {
            assert.deepEqual(testItem.string, Database.query('SELECT * FROM test_table WHERE string=\'' + testItem.string +'\'')[0].string);
        });
    });

    describe('## update', function() {
        const testItem = { string: 'another' };

        it('should be of type function', function() {
            assert.equal('function', typeof Database.update);
        });

        it('should return number of items updated', function() {
            assert.equal('1', Database.update('test_table', testItem, '"id"=\'2\''));
        });

        it('should be returned in query', function() {
            assert.deepEqual(testItem.string, Database.query('SELECT * FROM test_table WHERE id=\'' + 2 +'\'')[0].string);
        });
    });

    describe('## get', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database.get);
        });

        it('should return an array', function() {
            assert.notEqual(undefined, Database.get('test_table').length);
        });

        it('should return the result of query', function() {
            assert.deepEqual(Database.query('SELECT * FROM test_table'), Database.get('test_table'));
        });

        it('should respect the condition', function() {
            assert.deepEqual(Database.query('SELECT * FROM test_table WHERE id=\'' + 2 +'\''), Database.get('test_table', '"id"=\'2\''));
        });
    });

    describe('## delete', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database.delete);
        });

        it('should respect the condition', function() {
            Database.delete('test_table', '"id"=\'2\'');
            assert.deepEqual(1, Database.get('test_table').length);
        });

        it('should delete all when there is no condition', function() {
            Database.delete('test_table');
            assert.deepEqual(0, Database.get('test_table').length);
        });

        it('should return number of items deleted', function() {
            assert.equal(0, Database.delete('test_table'));
            Database.insert('test_table', { string: 'value' });
            assert.equal(1, Database.delete('test_table'));
        });
    });

    describe('## _isANumber', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database._isANumber);
        });

        it('should return true for a number', function() {
            assert.equal(true, Database._isANumber(2));
        });

        it('should return true for a number in string', function() {
            assert.equal(true, Database._isANumber('2'));
        });

        it('should return true for a float in string', function() {
            assert.equal(true, Database._isANumber('2.2'));
        });

        it('should return false for a alphabet in string', function() {
            assert.equal(false, Database._isANumber('a'));
        });

        it('should return false for a symbol in string', function() {
            assert.equal(false, Database._isANumber('+'));
        });
    });

    describe('## _encapsulateWithQuoteIfNotNumber', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database._encapsulateWithQuoteIfNotNumber);
        });

        it('should return as it is for a number', function() {
            assert.equal(2, Database._encapsulateWithQuoteIfNotNumber(2, '"'));
        });

        it('should return as it is for a number in string', function() {
            assert.equal(2, Database._encapsulateWithQuoteIfNotNumber('2', '"'));
        });

        it('should return as it is for a float in string', function() {
            assert.equal(2.2, Database._encapsulateWithQuoteIfNotNumber('2.2', '"'));
        });

        it('should return with quote for a alphabet in string', function() {
            assert.equal('"a"', Database._encapsulateWithQuoteIfNotNumber('a', '"'));
        });

        it('should return with quote for a symbol in string', function() {
            assert.equal('"+"', Database._encapsulateWithQuoteIfNotNumber('+', '"'));
        });
    });

    describe('## _toCSV', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database._toCSV);
        });

        it('should return a CSV', function() {
            assert.equal('"a", "b", "c"', Database._toCSV(['a', 'b', 'c'], '"'));
            assert.equal('\'a\', \'b\', \'c\'', Database._toCSV(['a', 'b', 'c'], '\''));
            assert.equal('\'a\', \'b\', \'c\'', Database._toCSV(['a', 'b', 'c'], '\''));
        });

        it('should return without quotes for numbers', function() {
            assert.equal('"a", 3, "c"', Database._toCSV(['a', 3, 'c'], '"'));
            assert.equal('"a", "c", 4.2', Database._toCSV(['a', 'c', 4.2], '"'));
        });

        it('should return with quotes for a single item', function() {
            assert.equal('\'a\'', Database._toCSV(['a'], '\''));
        });

        it('should return empty string for empty array', function() {
            assert.equal('', Database._toCSV([], '\''));
        });
    });

    describe('## _toKeyValuePairArray', function() {
        it('should be of type function', function() {
            assert.equal('function', typeof Database._toKeyValuePairArray);
        });

        it('should return a key value pair array from object', function() {
            assert.deepEqual(['"a"=\'b\''], Database._toKeyValuePairArray({ 'a': 'b' }));
            assert.deepEqual(['"a"=\'b\'', '"c"=\'d\''], Database._toKeyValuePairArray({ 'a': 'b', 'c': 'd' }));
        });

        it('should return without quotes for numbers', function() {
            assert.equal('"a"=3', Database._toKeyValuePairArray({'a': 3}, '"'));
            assert.equal('"a"=4.2', Database._toKeyValuePairArray({'a': 4.2}, '"'));
        });

        it('should return empty string for empty object', function() {
            assert.equal('', Database._toKeyValuePairArray({}));
        });
    });

    after(function() {
        Database.initialize('');
        Database.execute('DROP DATABASE test_database');
    });
});    
