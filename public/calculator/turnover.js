/**
 * Calculates the Tenant Turnover Rate based on the provided total units and vacant units.
 * The turnover rate is computed using the formula: (vacantUnits / totalUnits) * 100.
 * The result is then displayed on the designated element.
 * 
 * @param {string} uniqueID - The unique identifier associated with the set of input fields.
 */
function calculateTenantTurnover(uniqueID) {
    // Fetch the total units and vacant units values from the input fields
    let totalUnits = parseInt(document.getElementById('totalUnits-' + uniqueID).value, 10);
    let vacantUnits = parseInt(document.getElementById('vacantUnits-' + uniqueID).value, 10);

    // Validate the input values to ensure they are numbers and are not empty
    if (isNaN(totalUnits) || isNaN(vacantUnits) || totalUnits === '' || vacantUnits === '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Check to prevent division by zero
    if (totalUnits === 0) {
        alert('Total Units cannot be zero.');
        return;
    }

    // Calculate the tenant turnover rate
    const tenantTurnoverRate = (vacantUnits / totalUnits) * 100;

    // Display the computed turnover rate in the designated result container
    const resultDiv = document.getElementById('resultTenantTurnover-' + uniqueID);
    resultDiv.innerHTML = `Tenant Turnover Rate: ${tenantTurnoverRate.toFixed(2)}%`;
}
