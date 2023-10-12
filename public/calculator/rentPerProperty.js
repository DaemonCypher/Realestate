/**
 * Calculates the average rent price per property based on the total rent collected and the number of rented units.
 * Then, it displays the result in a designated HTML element.
 * 
 * @param {string} uniqueID - The unique identifier used to differentiate multiple sets of input and result elements.
 */
function calculateAverageRent(uniqueID) {
    // Get the values from the input fields
    let totalRentCollected = document.getElementById('totalRentCollected-' + uniqueID).value;
    let numberRentedUnits = document.getElementById('numberRentedUnits-' + uniqueID).value;

    // Ensure the values are numbers and not empty
    if (isNaN(totalRentCollected) || isNaN(numberRentedUnits) || totalRentCollected === '' || numberRentedUnits === '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Convert string input to numbers
    totalRentCollected = parseFloat(totalRentCollected);
    numberRentedUnits = parseInt(numberRentedUnits, 10);

    // Check for a division by zero error
    if (numberRentedUnits === 0) {
        alert('Number of Rented Units cannot be zero.');
        return;
    }

    // Calculate the average rent price per property
    const averageRentPrice = totalRentCollected / numberRentedUnits;

    // Display the result in the designated HTML element
    const resultDiv = document.getElementById('resultAverageRent-' + uniqueID);
    resultDiv.innerHTML = 'Average Rent Price per Property: $' + averageRentPrice.toFixed(2);
}
