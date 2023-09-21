function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    fetchDataForChart();   // Call the function to fetch data for the chart
    return false;          // Prevent the form from submitting
  }
  
let myLineChart;  // Declare the chart variable outside the functions.

function fetchDataForChart() {
    let userInput = document.getElementById("query").value.trim();
    const query = document.getElementById("query").value;
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
        const chartData = processForChart(data,userInput);
        // If the chart instance already exists, destroy it.
        if (myLineChart) {
            myLineChart.destroy();
        }

        // Render a new chart.
        myLineChart = renderChart(chartData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        //alert("An error occurred. Please try again.");
        window.location.href = "error.html";
        return;
    });
}