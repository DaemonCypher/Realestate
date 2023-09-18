function processForChart(dataArray) {
    // Convert string histories to arrays
    const allHistories = dataArray.map(entry => JSON.parse(entry.history));

    // Generate labels based on the longest history
    const maxHistoryLength = Math.max(...allHistories.map(history => history.length));
    const labels = Array.from({ length: maxHistoryLength }, (_, i) => `Point ${i + 1}`);

    const averageData = Array.from({ length: maxHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = allHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    return {
        labels: labels,
        datasets: [{
            label: 'Average Property Value',
            borderColor: '#4e19e0',
            backgroundColor: 'rgba(255, 87, 51, 0.2)',
            data: averageData
        }]
    };
}
function renderChart(data) {
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    // Rendering the chart
    return new Chart(
        document.getElementById('myLineChart'),
        config
    );
}
