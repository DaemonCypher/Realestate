function addRMCInput(uniqueID) {
    var rmcInputsDiv = document.getElementById('rmc-inputs-' + uniqueID);
    var inputIndex = rmcInputsDiv.children.length + 1;  // updated to account for delete buttons
    var newEntryDiv = document.createElement('div');
    newEntryDiv.id = 'rmc-entry-' + inputIndex + '-' + uniqueID;
    var newInputLabel = document.createElement('label');
    newInputLabel.htmlFor = 'rmc-' + inputIndex + '-' + uniqueID;
    newInputLabel.textContent = 'Repair/Maintenance ' + inputIndex + ' Cost:';
    var newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.id = 'rmc-' + inputIndex + '-' + uniqueID;
    newInput.name = 'rmc-' + inputIndex + '-' + uniqueID;
    newInput.required = true;
    var deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() { removeRMCInput(uniqueID, inputIndex); };
    newEntryDiv.appendChild(newInputLabel);
    newEntryDiv.appendChild(newInput);
    newEntryDiv.appendChild(deleteButton);
    rmcInputsDiv.appendChild(newEntryDiv);
}

function removeRMCInput(uniqueID, inputIndex) {
    var entryDiv = document.getElementById('rmc-entry-' + inputIndex + '-' + uniqueID);
    entryDiv.remove();
}

function calculateRMC(uniqueID) {
    var rmcInputsDiv = document.getElementById('rmc-inputs-' + uniqueID);
    var totalCost = 0;
    for (var i = 0; i < rmcInputsDiv.children.length; i++) {
        var inputField = rmcInputsDiv.children[i].children[1];  // get the input element within each entry div
        var cost = parseFloat(inputField.value);
        if (isNaN(cost)) {
            alert('Please enter valid numbers for all fields.');
            return;
        }
        totalCost += cost;
    }
    var resultDiv = document.getElementById('resultRMC-' + uniqueID);
    resultDiv.innerHTML = 'Total Repair and Maintenance Costs: $' + totalCost.toFixed(2);
}