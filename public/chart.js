function getMostFrequentLength(histories) {
    const frequency = {};

    histories.forEach(history => {
        const length = history.length;
        frequency[length] = (frequency[length] || 0) + 1;
    });

    let maxFrequency = -1;
    let mostFrequentLength = -1;

    for (const length in frequency) {
        if (frequency[length] > maxFrequency) {
            maxFrequency = frequency[length];
            mostFrequentLength = parseInt(length);
        }
    }

    return mostFrequentLength;
}

function getMonthLabel(date) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return monthNames[date.getMonth()] + ' ' + date.getFullYear();
}

function processForChart(dataArray,userInput) {
    let labelString = `${userInput} Average Property Value`;
    console.log(dataArray);
    // Convert string histories to arrays
    const allHistories = dataArray.map(entry => JSON.parse(entry.history));

    // Determine the most frequent history length
    const mostFrequentHistoryLength = getMostFrequentLength(allHistories);

    // Filter out histories that don't match the most frequent length
    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    // Generate labels based on the month
    const endDate = new Date(dataArray[0].dataDate); // Assuming all entries have the same dataDate
    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index); // Subtract months based on the index
        return getMonthLabel(dateToUse);
    }).reverse(); // Reverse labels to have them in the correct order

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    return {
        labels: labels,
        datasets: [{
            label: labelString,
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
