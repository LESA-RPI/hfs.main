let chart; // Declare a variable to hold the Chart instance

// Function to initialize an empty chart
function initializeChart() {
    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Flourecence Value',
                data: [],
                borderColor: '#2e7d32',
                fill: false
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Flourescence' } }
            }
        }
    });
}

// Function to update the chart with fetched data
function fetchData() {
    const startDate = document.getElementById('start-date').value;
    const dayRange = parseInt(document.getElementById('day-range').value, 10);

    if (!startDate || isNaN(dayRange) || dayRange < 1) {
        alert("Please provide a valid start date and day range.");
        return;
    }

    fetch(`/data?start_date=${startDate}&day_range=${dayRange}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item.date);
            const values = data.map(item => item.value);
            // Update the chart with new data or show an empty graph
            if (labels.length > 0) {
                chart.data.labels = labels;
                chart.data.datasets[0].data = values;
            } else {
                chart.data.labels = []; // Empty labels for an empty graph
                chart.data.datasets[0].data = []; // Empty dataset for an empty graph
            }

            chart.update();
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Initialize the empty chart when the page loads
window.onload = initializeChart;
