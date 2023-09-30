function calculateAverageRent(uniqueID) {
    // Get the values from the input fields
    var totalRentCollected = document.getElementById('totalRentCollected-' + uniqueID).value;
    var numberRentedUnits = document.getElementById('numberRentedUnits-' + uniqueID).value;

    // Ensure the values are numbers and not empty
    if(isNaN(totalRentCollected) || isNaN(numberRentedUnits) || totalRentCollected === '' || numberRentedUnits === '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Convert string input to numbers
    totalRentCollected = parseFloat(totalRentCollected);
    numberRentedUnits = parseInt(numberRentedUnits, 10);

    // Check for a division by zero error
    if(numberRentedUnits == 0) {
        alert('Number of Rented Units cannot be zero.');
        return;
    }

    // Calculate the average rent price per property
    var averageRentPrice = totalRentCollected / numberRentedUnits;

    // Display the result
    var resultDiv = document.getElementById('resultAverageRent-' + uniqueID);
    resultDiv.innerHTML = 'Average Rent Price per Property: $' + averageRentPrice.toFixed(2);
}
