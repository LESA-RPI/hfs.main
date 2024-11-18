const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');
const app = express();
const port = 3000;
const { isAsyncFunction } = require('util/types');

// Serve static files
app.use(express.static('public'));

// Use EJS as the template engine
app.set('view engine', 'ejs');

// Function to read and parse the CSV file
function readCSV(callback) {
    const results = [];
    fs.createReadStream('data_log.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            callback(results);
        });
}

// Get all categories from the CSV
app.get('/', (req, res) => {
    readCSV((data) => {
        const categories = [...new Set(data.map(item => item.category))];
        res.render('index', { categories });
    });
});

// Fetch data from the CSV based on selected date range
app.get('/data', (req, res) => {
    const { start_date, day_range } = req.query;
    const sd = start_date.split(' ')[0];
    const startDate = new Date(sd);
// Parse day_range to an integer
    const dayRange = parseInt(day_range, 10);
    const endDate = new Date(sd);
    endDate.setDate(endDate.getDate() + dayRange);

    readCSV((data) => {
        const filteredData = data.reduce((acc, item) => {

            const entryDate = new Date(item.Timestamp.split(' ')[0]);
            // Check if the entry date falls within the specified range (inclusive)
            if (entryDate >= startDate && entryDate < endDate) {
                const numericValue = parseInt(item.Signal_Strength, 10); // Convert value to number
                acc[item.Timestamp] = numericValue; // Map date to value
            }
            return acc; // Return the accumulator for the next iteration
        }, {});
// Convert to an array format suitable for Chart.js
        const resultArray = Object.keys(filteredData).map(date => ({
            date,
            value: filteredData[date]
        }));
        res.json(resultArray);
    });
});



// Start the server
app.listen(port, () => {
    console.log(`Dashboard running at http://localhost:${port}`);
});
