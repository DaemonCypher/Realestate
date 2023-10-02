function soldGetMedian(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);

    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    } else {
        return sorted[middle];
    }
}

function soldGetMostFrequentLength(histories) {
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

function soldGetMonthLabel(date) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return monthNames[date.getMonth()] + ' ' + date.getFullYear();
}

function soldProcessForChart(dataArray,userInput) {
    let labelString = `${userInput} Average Property Value`;
    console.log(dataArray);
    
    const allHistories = dataArray.map(entry => JSON.parse(entry.history));

    const mostFrequentHistoryLength = soldGetMostFrequentLength(allHistories);  // Updated function name

    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const endDate = new Date(dataArray[0].dataDate);

    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return soldGetMonthLabel(dateToUse);  // Updated function name
    }).reverse();

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return soldGetMedian(valuesAtCurrentIndex);  // Updated function name
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
            label: `${userInput} Median Property Value`,
            borderColor: '#ff6347',
            backgroundColor: 'rgba(0, 0, 0, 0)', // transparent
            data: medianData
        }]
    };
}

function soldRenderChart(data) {
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

function soldHandleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    soldFetchDataForChart();   // Call the function to fetch data for the chart
    return false;          // Prevent the form from submitting
  }
  
let soldLineChart;  // Declare the chart variable outside the functions.

function soldFetchDataForChart() {
    let userInput = document.getElementById("soldQuery").value.trim();
    const query = document.getElementById("soldQuery").value;
    if (!query) {
        alert("Please enter a city to search.");
        return;
    }
    console.log(query)

    fetch('/sold', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0 || !Array.isArray(data)) {  // Check if data is empty or not an array
            window.location.href = "noData.html";  // Redirect to no-data.html if data is empty
            return;
        }
        const chartData = soldProcessForChart(data, userInput);  // Updated function name
        // If the chart instance already exists, destroy it.
        if (soldLineChart) {
            soldLineChart.destroy();
        }

        // Render a new chart.
        soldLineChart = soldRenderChart(chartData);  // Updated function name
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        //alert("An error occurred. Please try again.");
        window.location.href = "error.html";
        return;
    });
}