/**
 * Calculates the Operating Expense Ratio (OER) based on the provided unique ID.
 * The unique ID helps in targeting the specific set of input fields.
 * The formula for OER is: (Operating Expenses / Gross Operating Income) x 100%
 * 
 * @param {string} uniqueID - A unique identifier to target specific input fields.
 */
function calculateOER(uniqueID) {
    // Get the values from the input fields
    const operatingExpensesValue = document.getElementById('operatingExpenses-' + uniqueID).value;
    const grossOperatingIncomeValue = document.getElementById('grossOperatingIncome-' + uniqueID).value;

    // Ensure the values are numbers and not empty
    if (isNaN(operatingExpensesValue) || isNaN(grossOperatingIncomeValue) || operatingExpensesValue === '' || grossOperatingIncomeValue === '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Convert string input to numbers
    const operatingExpenses = parseFloat(operatingExpensesValue);
    const grossOperatingIncome = parseFloat(grossOperatingIncomeValue);

    // Check for a division by zero error
    if (grossOperatingIncome === 0) {
        alert('Gross Operating Income cannot be zero.');
        return;
    }

    // Calculate the operating expense ratio
    const oer = (operatingExpenses / grossOperatingIncome) * 100;

    // Display the result
    const resultDiv = document.getElementById('resultOER-' + uniqueID);
    resultDiv.innerHTML = 'Operating Expense Ratio: ' + oer.toFixed(2) + '%';
}
