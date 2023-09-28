function calculateTenantTurnover() {
    // Get the values from the input fields
    var totalUnits = document.getElementById('totalUnits').value;
    var vacantUnits = document.getElementById('vacantUnits').value;

    // Ensure the values are numbers and not empty
    if(isNaN(totalUnits) || isNaN(vacantUnits) || totalUnits == '' || vacantUnits == '') {
        alert('Please enter valid numbers for both fields.');
        return;
    }

    // Convert string input to numbers
    totalUnits = parseInt(totalUnits, 10);
    vacantUnits = parseInt(vacantUnits, 10);

    // Check for a division by zero error
    if(totalUnits == 0) {
        alert('Total Units cannot be zero.');
        return;
    }

    // Calculate the tenant turnover rate
    var tenantTurnoverRate = (vacantUnits / totalUnits) * 100;

    // Display the result
    var resultDiv = document.getElementById('resultTenantTurnover');
    resultDiv.innerHTML = 'Tenant Turnover Rate: ' + tenantTurnoverRate.toFixed(2) + '%';
}
