function getMedian(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);

    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    } else {
        return sorted[middle];
    }
}

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

function processForActiveChart(dataArray, userInput) {
    let labelString = `${userInput} Average Property Value for Active Listings`;
    console.log(dataArray);
    
    const allHistories = dataArray.map(entry => JSON.parse(entry.activeHistoryId));  // Assuming activeHistoryId is the field name

    const mostFrequentHistoryLength = getMostFrequentLength(allHistories);

    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const endDate = new Date(dataArray[0].dataDate);

    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return getMonthLabel(dateToUse);
    }).reverse();

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return getMedian(valuesAtCurrentIndex);
    });

    return {
        labels: labels,
        datasets: [{
            label: labelString,
            borderColor: '#4e19e0',
            backgroundColor: 'rgba(255, 87, 51, 0.2)',
            data: averageData
        },
        {
            label: `${userInput} Median Property Value for Active Listings`,
            borderColor: '#ff6347',
            backgroundColor: 'rgba(0, 0, 0, 0)', // transparent
            data: medianData
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

    return new Chart(
        document.getElementById('historyChart'),
        config
    );
}

function handleActiveFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    fetchActiveDataForChart();   // Call the function to fetch data for the chart
    return false;          // Prevent the form from submitting
  }
  
let myLineChart;  // Declare the chart variable outside the functions.

function fetchActiveDataForChart() {
    let userInput = document.getElementById("activeQuery").value.trim();
    const query = document.getElementById("activeQuery").value;
    if (!query) {
        alert("Please enter a city to search.");
        return;
    }
    console.log(query)

    fetch('/active', {  // Change the endpoint to '/active'
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        const chartData = processForActiveChart(data, userInput);  // Use processForActiveChart
        // If the chart instance already exists, destroy it
        if (myLineChart) {
            myLineChart.destroy();
        }

        // Render a new chart
        myLineChart = renderChart(chartData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        window.location.href = "error.html";
        return;
    });
}

