function activeGetMedian(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);

    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    } else {
        return sorted[middle];
    }
}

function activeGetMostFrequentLength(histories) {
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

function activeGetMonthLabel(date) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return monthNames[date.getMonth()] + ' ' + date.getFullYear();
}

function activeProcessForChart(cityData, userInput, userPropertyHistory) {
    const cityName = cityData[0].city;
    const allHistories = cityData.map(entry => JSON.parse(entry.history));

    const mostFrequentHistoryLength = activeGetMostFrequentLength(allHistories);  
    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const propertyData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        return userPropertyHistory[index] || 0;
    });

    const endDate = new Date(cityData[0].dataDate);
    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return activeGetMonthLabel(dateToUse);  
    }).reverse();

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return activeGetMedian(valuesAtCurrentIndex);  
    });

    return {
        labels: labels,
        datasets: [
            {
                label: `${cityName} Median Property Value`,
                borderColor: '#4e19e0',
                backgroundColor: 'rgba(0, 0, 0, 0)',
                data: averageData
            },
            {
                label: `${cityName} Median Property Value`,
                borderColor: '#ff6347',
                backgroundColor: 'rgba(0, 0, 0, 0)', 
                data: medianData
            },
            {
                label: `${userInput} Property Price History`,
                borderColor: '#00aaff',
                backgroundColor: 'rgba(0, 170, 255, 0.1)', 
                data: propertyData
            }
        ]
    };
}

function activeRenderChart(data) {
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

    return new Chart(
        document.getElementById('activeChart'),
        config
    );
}

function activeHandleFormSubmit(event) {
    event.preventDefault();
    activeFetchDataForChart();  
    return false;
}

let activeLineChart; 

function activeFetchDataForChart() {
    const userInput = document.getElementById("activeQuery").value.trim();

    if (!userInput) {
        alert("Please enter a city to search.");
        return;
    }

    // First, fetch data for the specific address inputted by the user
    fetch('/active', {  
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error fetching from /active: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const city = data[0].city;
        const userPropertyHistory = JSON.parse(data[0].history || '[]');

        // Now, fetch data for the entire city
        return fetch('/sold', {  
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: city })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error fetching from /sold: ' + response.statusText);
            }
            return response.json();
        })
        .then(cityData => {
            return [cityData, userPropertyHistory];
        });
    })
    .then(results => {
        const cityData = results[0];
        const userPropertyHistory = results[1];
        const chartData = activeProcessForChart(cityData, userInput, userPropertyHistory);

        if (activeLineChart) {
            activeLineChart.destroy();
        }
        activeLineChart = activeRenderChart(chartData);
    })
    .catch(error => {
        console.error('Error:', error);
        const outputElement = document.getElementById('debug-output');
        outputElement.textContent = JSON.stringify({ errorMessage: error.message }, null, 2);
    });
}

function outputDataToPage(data) {
    const outputElement = document.getElementById('debug-output');
    outputElement.textContent = JSON.stringify(data, null, 2);
}