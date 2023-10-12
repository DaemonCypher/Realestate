/**
 * Get the median of an array.
 * @param {Array} arr - The array of numbers.
 * @returns {Number} - The median of the array.
 */
function soldGetMedian(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);

    // If the length is even, return the average of the two middle numbers.
    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    } else {
        return sorted[middle];
    }
}

/**
 * Get the most frequent length from a list of histories.
 * @param {Array} histories - The list of history arrays.
 * @returns {Number} - The most frequent length.
 */
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

/**
 * Get the label for a given date in "Month Year" format.
 * @param {Date} date - The date object.
 * @returns {String} - The formatted date string.
 */
function soldGetMonthLabel(date) {
    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];
    return `${monthNames[date.getMonth()]} ${date.getFullYear()}`;
}

/**
 * Process the provided data array for chart rendering.
 * @param {Array} dataArray - The data for chart processing.
 * @param {String} userInput - The user input string for label purposes.
 * @returns {Object} - The processed chart data.
 */
function soldProcessForChart(dataArray, userInput) {
    let labelString = `${userInput} Average Property Value`;

    const allHistories = dataArray.map(entry => JSON.parse(entry.history));

    const mostFrequentHistoryLength = soldGetMostFrequentLength(allHistories);

    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const endDate = new Date(dataArray[0].dataDate);

    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return soldGetMonthLabel(dateToUse);
    }).reverse();

    // Calculate average data for the chart.
    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    // Calculate median data for the chart.
    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return soldGetMedian(valuesAtCurrentIndex);
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

/**
 * Render the chart with the given data.
 * @param {Object} data - The data to use for the chart.
 * @returns {Object} - The Chart object.
 */
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

/**
 * Handle the form submission, fetching data for the chart.
 * @param {Event} event - The form submission event.
 * @returns {Boolean} - Always returns false to prevent form submission.
 */
function soldHandleFormSubmit(event) {
    event.preventDefault();  // Prevent default form submission behavior.
    soldFetchDataForChart(); // Fetch data for the chart.
    return false;            // Prevent the form from submitting.
}

let soldLineChart;  // Declare the chart variable outside the functions for scope reasons.

/**
 * Fetch the data for the chart based on user input.
 */
function soldFetchDataForChart() {
    let userInput = document.getElementById("soldQuery").value.trim();
    const query = document.getElementById("soldQuery").value;
    if (!query) {
        alert("Please enter a city to search.");
        return;
    }

    fetch('/sold', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0 || !Array.isArray(data)) {  // Check if data is empty or not an array.
            window.location.href = "noData.html";        // Redirect if data is empty.
            return;
        }
        const chartData = soldProcessForChart(data, userInput);  // Process data for the chart.
        if (soldLineChart) {
            soldLineChart.destroy();  // Destroy existing chart instance if it exists.
        }
        // Render the chart.
        soldLineChart = soldRenderChart(chartData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        window.location.href = "error.html";  // Redirect to error page on fetch error.
    });
}
