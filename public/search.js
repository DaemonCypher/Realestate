function fetchResults() {
    var input = document.getElementById("query");
    var filter = input.value;

    // Send a POST request to /search
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


function filterColumn() {
    const table = document.getElementById("resultTable");
    const tr = table.getElementsByTagName("tr");

    for (let i = 2; i < tr.length; i++) { 
        let displayRow = true;

        for (let colIndex = 0; colIndex <= 4; colIndex++) {
            const td = tr[i].getElementsByTagName("td")[colIndex];

            if (td) {
                let txtValue = td.textContent || td.innerText;

                if (colIndex === 3 || colIndex === 4) { // Handle Price and YoY
                    let minInput, maxInput;

                    if (colIndex === 3) { // Price
                        minInput = document.querySelector(".price-min");
                        maxInput = document.querySelector(".price-max");
                    } else { // YoY
                        minInput = document.querySelector(".yoy-min");
                        maxInput = document.querySelector(".yoy-max");
                    }

                    const min = parseFloat(minInput.value);
                    const max = parseFloat(maxInput.value);
                    const value = parseFloat(txtValue.replace('%', ''));

                    if (!(isNaN(min) || value >= min) || !(isNaN(max) || value <= max)) {
                        displayRow = false;
                    }
                } else {
                    const input = document.querySelectorAll(".column-filter")[colIndex];
                    const filter = input.value.toUpperCase();
                    if (txtValue.toUpperCase().indexOf(filter) === -1) {
                        displayRow = false;
                    }
                }
            }
        }

        tr[i].style.display = displayRow ? "" : "none";
    }
}



function updateTable(data) {
    const tableBody = document.querySelector("#resultTable tbody");
    let tableHtml = '';

    data.forEach(row => {
        const history = row.history.split(','); // Assuming history is comma-separated.
        const price = parseFloat(history.pop());  // Pops the last value for Price

        const oldPrice = parseFloat(history[history.length - 12]); // Value from 12 months ago
        const YoY = ((price - oldPrice) / oldPrice * 100).toFixed(2) + '%'; // YoY as percentage

        tableHtml += '<tr>';
        tableHtml += `<td>${row.address}</td>`;
        tableHtml += `<td>${row.city}</td>`;
        tableHtml += `<td>${row.status}</td>`;
        tableHtml += `<td>${price}</td>`;
        tableHtml += `<td>${YoY}</td>`;
        tableHtml += '</tr>';
    });

    tableBody.innerHTML = tableHtml;
}

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

function filterInputHandler() {
    debouncedFilter();
}

