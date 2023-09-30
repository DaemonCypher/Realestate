function calculateOER(uniqueID) {
    // Get the values from the input fields
    var operatingExpenses = document.getElementById('operatingExpenses-' + uniqueID).value;
    var grossOperatingIncome = document.getElementById('grossOperatingIncome-' + uniqueID).value;

    // Ensure the values are numbers and not empty
    if(isNaN(operatingExpenses) || isNaN(grossOperatingIncome) || operatingExpenses === '' || grossOperatingIncome === '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Convert string input to numbers
    operatingExpenses = parseFloat(operatingExpenses);
    grossOperatingIncome = parseFloat(grossOperatingIncome);

    // Check for a division by zero error
    if(grossOperatingIncome == 0) {
        alert('Gross Operating Income cannot be zero.');
        return;
    }

    // Calculate the operating expense ratio
    var oer = (operatingExpenses / grossOperatingIncome) * 100;

    // Display the result
    var resultDiv = document.getElementById('resultOER-' + uniqueID);
    resultDiv.innerHTML = 'Operating Expense Ratio: ' + oer.toFixed(2) + '%';
}
