/**
 * Returns the median of an array of numbers.
 * @param {number[]} arr - An array of numbers.
 * @returns {number} The median of the array.
 */
function compareGetMedian(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const middle = Math.floor(sorted.length / 2);

    if (sorted.length % 2 === 0) {
        return (sorted[middle - 1] + sorted[middle]) / 2;
    } else {
        return sorted[middle];
    }
}

/**
 * Determines the most frequently occurring history length from an array of histories.
 * @param {Array<Array<number>>} histories - An array of property histories.
 * @returns {number} The most frequent history length.
 */
function compareGetMostFrequentLength(histories) {
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
 * Returns a string representation of the month and year of a date.
 * @param {Date} date - A date object.
 * @returns {string} The month and year of the date.
 */
function compareGetMonthLabel(date) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return monthNames[date.getMonth()] + ' ' + date.getFullYear();
}

/**
 * Processes city data and a user property history to produce chart data.
 * @param {Object[]} cityData - An array of city data.
 * @param {string} userInput - The user's inputted city name.
 * @param {number[]} userPropertyHistory - The user's property price history.
 * @returns {Object} Data for rendering the chart.
 */
function compareProcessForChart(cityData, userInput, userPropertyHistory) {
    const cityName = cityData[0].city;
    const allHistories = cityData.map(entry => JSON.parse(entry.history));

    const mostFrequentHistoryLength = compareGetMostFrequentLength(allHistories);
    const matchingHistories = allHistories.filter(history => history.length === mostFrequentHistoryLength);

    const propertyData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        return userPropertyHistory[index] || 0;
    });

    const endDate = new Date(cityData[0].dataDate);
    const labels = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const dateToUse = new Date(endDate);
        dateToUse.setMonth(dateToUse.getMonth() - index);
        return compareGetMonthLabel(dateToUse);
    }).reverse();

    const averageData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        const sum = valuesAtCurrentIndex.reduce((acc, value) => acc + value, 0);
        return sum / valuesAtCurrentIndex.length;
    });

    const medianData = Array.from({ length: mostFrequentHistoryLength }).map((_, index) => {
        const valuesAtCurrentIndex = matchingHistories.map(history => history[index] || 0);
        return compareGetMedian(valuesAtCurrentIndex);
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

/**
 * Renders a line chart using the given data.
 * @param {Object} data - Data for the chart.
 * @returns {Object} The Chart object.
 */
function compareRenderChart(data) {
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
        document.getElementById('compareChart'),
        config
    );
}

/**
 * Handles the form submission event.
 * @param {Event} event - The form submission event.
 * @returns {boolean} Always returns false to prevent the default form submission behavior.
 */
function compareHandleFormSubmit(event) {
    event.preventDefault();
    compareFetchDataForChart();
    return false;
}

let compareLineChart;

/**
 * Fetches data for the chart and updates the chart with the new data.
 */
function compareFetchDataForChart() {
    const userInput = document.getElementById("compareQuery").value.trim();

    if (!userInput) {
        alert("Please enter a city to search.");
        return;
    }

    // First, fetch data for the specific address inputted by the user
    fetch('/property', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error fetching from /property: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const city = data[0].city;
        const userPropertyHistory = JSON.parse(data[0].history || '[]');

        // Now, fetch data for the entire city
        return fetch('/compare', {
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
        const chartData = compareProcessForChart(cityData, userInput, userPropertyHistory);

        if (compareLineChart) {
            compareLineChart.destroy();
        }
        compareLineChart = compareRenderChart(chartData);
    })
    .catch(error => {
        console.error('Error:', error);
        const outputElement = document.getElementById('debug-output');
        outputElement.textContent = JSON.stringify({ errorMessage: error.message }, null, 2);
    });
}

/**
 * Outputs data to the debug-output element on the page.
 * @param {Object} data - The data to output.
 */
function outputDataToPage(data) {
    const outputElement = document.getElementById('debug-output');
    outputElement.textContent = JSON.stringify(data, null, 2);
}
