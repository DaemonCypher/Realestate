function calculateRMC() {
    var repair1 = parseFloat(document.getElementById('repair1').value);
    var repair2 = parseFloat(document.getElementById('repair2').value);
    var maintenance1 = parseFloat(document.getElementById('maintenance1').value);
    var maintenance2 = parseFloat(document.getElementById('maintenance2').value);

    if(isNaN(repair1) || isNaN(repair2) || isNaN(maintenance1) || isNaN(maintenance2)) {
        alert('Please enter valid numbers for all fields.');
        return;
    }

    var totalCost = repair1 + repair2 + maintenance1 + maintenance2;

    var resultDiv = document.getElementById('resultRMC');
    resultDiv.innerHTML = 'Total Repair and Maintenance Costs: $' + totalCost.toFixed(2);
}
