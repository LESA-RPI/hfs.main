const { execSync } = require('child_process');

const Database = {}

Database._exec = (query) => {
    let command = 'echo "' + query + '" | psql';

    if (Database.databaseName) {
        command += ' -d ' + Database.databaseName;
    }

    return execSync(command).toString().trim();
}

Database._isANumber = (item) => {
    return !isNaN(+item);
}

Database._encapsulateWithQuoteIfNotNumber = (item, quote) => {
    return Database._isANumber(item) ? item : (quote + item + quote);
}

Database._toCSV = (array, quote) => {
    if (array.length == 0) {
        return '';
    } else if (array.length == 1) {
        return Database._encapsulateWithQuoteIfNotNumber(array[0], quote);
    } else {
        return array.reduce((acc, current, index, source) => {
                if (index == 1) {
                    acc = Database._encapsulateWithQuoteIfNotNumber(acc, quote);
                }

                if (index < source.length) {
                    acc += ', ';
                }

                return acc + Database._encapsulateWithQuoteIfNotNumber(current, quote);
            })
    }
}

Database._toKeyValuePairArray = (items) => {
    const values = Object.values(items);

    return Object.keys(items).map((key, index) => '"' + key + '"=' + Database._encapsulateWithQuoteIfNotNumber(values[index], '\''));
}

Database.databaseName = '';

Database.initialize = (databaseName) => {
    Database.databaseName = databaseName;
}

Database.execute = (query) => {
    return Database._exec(query);
}

Database.query = (query) => {
    const response = Database._exec(query).split('\n');
    const keys = response[0].split('|').map(column => column.trim());
    const result = [];

    if (response[response.length - 1] != '(0 rows)') {
        for (let rowIndex = 2; rowIndex < response.length - 1; rowIndex++) {
            const row = response[rowIndex].split('|').map(item => item.trim());

            const resultItem = {};
            keys.forEach((key, index) => {
                const value = +row[index];
                resultItem[key] = isNaN(value) ? row[index] : value;
            })
            result.push(resultItem);
        }
    }

    return result;
}

Database.get = (table, condition) => {
    return Database.query('SELECT * FROM ' + table
        + (condition ? ' WHERE ' + condition : ''));
}

Database.insert = (table, item) => {
    const query = 'INSERT INTO ' + table
        + ' ('
        + Database._toCSV(Object.keys(item), '"')
        + ') VALUES ('
        + Database._toCSV(Object.values(item), '\'')
        + ')';

    return Database._exec(query).split(' ')[2];
}

Database.update = (table, item, condition) => {
    const query = 'UPDATE ' + table
        + ' SET '
        + Database._toKeyValuePairArray(item).join(', ')
        + ' WHERE ' + condition;

    return Database._exec(query).split(' ')[1];
}

Database.delete = (table, condition) => {
    return Database.execute('DELETE FROM ' + table
        + (condition ? ' WHERE ' + condition : '')).split(' ')[1];
}

module.exports = Database;
