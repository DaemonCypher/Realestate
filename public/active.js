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

function activeProcessForChart(dataArray, userInput) {
    let labelString = `${userInput} Average Property Value`;
    console.log(userInput)
    const allHistories = dataArray.map(entry => JSON.parse(entry.history));

    const mostFrequentHistoryLength = activeGetMostFrequentLength(allHistories);  // Updated function name

    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const endDate = new Date(dataArray[0].dataDate);

    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return activeGetMonthLabel(dateToUse);  // Updated function name
    }).reverse();

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return activeGetMedian(valuesAtCurrentIndex);  // Updated function name
    });

    return {
        labels: labels,
        datasets: [{
            label: labelString,
            borderColor: '#4e19e0',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            data: averageData
        },
        {
            label: `${userInput} Median Property Value`,
            borderColor: '#ff6347',
            backgroundColor: 'rgba(0, 0, 0, 0)', // transparent
            data: medianData
        }]
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
    activeFetchDataForChart();  // Updated the function name here too
    return false;
}
let activeLineChart;  // Declare the chart variable outside the functions.

function activeFetchDataForChart() {
    let userInput = document.getElementById("activeQuery").value.trim();
    const query = document.getElementById("activeQuery").value;
    if (!query) {
        alert("Please enter a city to search.");
        return;
    }
    console.log(query)

    fetch('/active', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Filter out entries with empty lists '[]'
        const filteredData = data.filter(entry => JSON.parse(entry.history).length !== 0);
    
        // Output data to page
        outputDataToPage(filteredData);  // <-- Add this line
    
        if (filteredData.length === 0) {
            window.location.href = "noData.html";
            return;
        }
    
        const chartData = activeProcessForChart(filteredData, userInput);
        if (activeLineChart) {
            activeLineChart.destroy();
        }
        activeLineChart = activeRenderChart(chartData);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
        window.location.href = "error.html";
        return;
    });
}

function outputDataToPage(data) {
    const outputElement = document.getElementById('debug-output');
    outputElement.textContent = JSON.stringify(data, null, 2);
}
