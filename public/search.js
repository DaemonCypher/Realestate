/**
 * Get the selected timeframe value from the dropdown.
 * @returns {Number} - The selected timeframe value as an integer.
 */
function getTimeFrameValue() {
    const timeFrameSelect = document.getElementById("timeFrame");
    return parseInt(timeFrameSelect.value, 10);
}

/**
 * Fetch results based on the value in the 'query' input.
 */
function fetchResults() {
    const input = document.getElementById("query");
    const filter = input.value;

    // Send a POST request to the server to search with the provided filter.
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: filter })
    })
    .then(response => response.json())
    .then(data => {
        updateTable(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Update the table with the provided data.
 * @param {Array} data - The array of data to be displayed in the table.
 */
function updateTable(data) {
    const tableBody = document.querySelector("#resultTable tbody");
    let tableHtml = '';

    const timeframe = getTimeFrameValue(); // 1 for MoM, 3 for QoQ, 12 for YoY

    // Iterate through data and create table rows.
    data.forEach(row => {
        const history = row.history.split(','); // Assuming history is comma-separated.
        const price = parseFloat(history.pop()); // Get the last value for Price.

        // Display data only if there's sufficient historical data.
        if (history.length >= timeframe) {
            const oldPrice = parseFloat(history[history.length - timeframe]);
            const percentageChange = ((price - oldPrice) / oldPrice * 100).toFixed(2) + '%'; 

            // Construct table row HTML.
            tableHtml += `<tr>
                <td>${row.address}</td>
                <td>${row.city}</td>
                <td>${row.status}</td>
                <td>${price}</td>
                <td>${percentageChange}</td>
                <td>${row.beds}</td>
                <td>${row.baths}</td>
                <td>${row.yearBuilt}</td>
                <td>${row.sqft}</td>
            </tr>`;
        }
    });

    // Update the table body with the new HTML.
    tableBody.innerHTML = tableHtml;
}

/**
 * Filter rows of the table based on various criteria.
 */
function filterColumn() {
    const table = document.getElementById("resultTable");
    const tr = table.getElementsByTagName("tr");
    const timeframe = getTimeFrameValue();

    // Get values from filter inputs.
    const bedsFilterValue = parseFloat(document.querySelector('.beds-filter').value);
    const bathsFilterValue = parseFloat(document.querySelector('.baths-filter').value);
    const yearBuiltFilterValue = parseFloat(document.querySelector('.year-built-filter').value);
    const sqftFilterValue = parseFloat(document.querySelector('.sqft-filter').value);

    // Iterate through table rows and apply filters.
    for (let i = 2; i < tr.length; i++) {
        let displayRow = true;
        const tdElements = tr[i].getElementsByTagName("td");

        // Check filters for each column.
        for (let colIndex = 0; colIndex < tdElements.length; colIndex++) {
            const td = tdElements[colIndex];
            const txtValue = td.textContent || td.innerText;

            switch (colIndex) {
                case 3:  // Price
                    const priceMinInput = document.querySelector(".price-min");
                    const priceMaxInput = document.querySelector(".price-max");

                    const priceMin = parseFloat(priceMinInput.value);
                    const priceMax = parseFloat(priceMaxInput.value);
                    const priceValue = parseFloat(txtValue);

                    if (!(isNaN(priceMin) || priceValue >= priceMin) || !(isNaN(priceMax) || priceValue <= priceMax)) {
                        displayRow = false;
                    }
                    break;
                case 4:  // YoY/MoM/QoQ
                    let minInput, maxInput;

                    switch (timeframe) {
                        case 1:  // MoM
                            minInput = document.querySelector(".yoy-min");
                            maxInput = document.querySelector(".yoy-max");
                            break;
                        case 3:  // QoQ
                            minInput = document.querySelector(".yoy-min");
                            maxInput = document.querySelector(".yoy-max");
                            break;
                        case 12: // YoY
                        default:
                            minInput = document.querySelector(".yoy-min");
                            maxInput = document.querySelector(".yoy-max");
                            break;
                    }

                    const percentageMin = parseFloat(minInput.value);
                    const percentageMax = parseFloat(maxInput.value);
                    const percentageValue = parseFloat(txtValue.replace('%', ''));

                    if (!(isNaN(percentageMin) || percentageValue >= percentageMin) || !(isNaN(percentageMax) || percentageValue <= percentageMax)) {
                        displayRow = false;
                    }
                    break;
                case 5:  // Beds
                    if (!isNaN(bedsFilterValue) && parseFloat(txtValue) < bedsFilterValue) {
                        displayRow = false;
                    }
                    break;
                case 6:  // Baths
                    if (!isNaN(bathsFilterValue) && parseFloat(txtValue) < bathsFilterValue) {
                        displayRow = false;
                    }
                    break;
                case 7:  // Year Built
                    if (!isNaN(yearBuiltFilterValue) && parseFloat(txtValue) < yearBuiltFilterValue) {
                        displayRow = false;
                    }
                    break;
                case 8:  // Sqft
                    if (!isNaN(sqftFilterValue) && parseFloat(txtValue) < sqftFilterValue) {
                        displayRow = false;
                    }
                    break;
                default: // Other columns
                    const input = document.querySelectorAll(".column-filter")[colIndex];
                    const filter = input.value.toUpperCase();
                    if (txtValue.toUpperCase().indexOf(filter) === -1) {
                        displayRow = false;
                    }
                    break;
            }
        }
        // Show or hide the row based on whether it passed all the filters.
        tr[i].style.display = displayRow ? "" : "none";
    }
}


/**
 * Debounce function to delay the execution of the provided function 
 * by the specified wait time.
 * @param {Function} func - The function to be debounced.
 * @param {Number} wait - The time in milliseconds to delay the function execution.
 * @returns {Function} - The debounced version of the provided function.
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const debouncedFilter = debounce(filterColumn, 500);

/**
 * Handler function for the filter inputs' input events.
 */
function filterInputHandler() {
    debouncedFilter();
}