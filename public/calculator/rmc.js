/**
 * Dynamically adds a new repair/maintenance cost (RMC) input field with an associated delete button.
 * The added input field is appended to a designated container element.
 * 
 * @param {string} uniqueID - The unique identifier to differentiate multiple sets of RMC input fields.
 */
function addRMCInput(uniqueID) {
    // Get the container for the RMC input fields
    const rmcInputsDiv = document.getElementById('rmc-inputs-' + uniqueID);
    
    // Determine the index for the new input based on the number of existing children
    const inputIndex = rmcInputsDiv.children.length + 1;
    
    // Create the new input container, label, input field, and delete button
    const newEntryDiv = document.createElement('div');
    newEntryDiv.id = 'rmc-entry-' + inputIndex + '-' + uniqueID;

    const newInputLabel = document.createElement('label');
    newInputLabel.htmlFor = 'rmc-' + inputIndex + '-' + uniqueID;
    newInputLabel.textContent = 'Repair/Maintenance ' + inputIndex + ' Cost:';
    
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.id = 'rmc-' + inputIndex + '-' + uniqueID;
    newInput.name = 'rmc-' + inputIndex + '-' + uniqueID;
    newInput.required = true;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() { removeRMCInput(uniqueID, inputIndex); };
    
    // Append the elements to the new container
    newEntryDiv.appendChild(newInputLabel);
    newEntryDiv.appendChild(newInput);
    newEntryDiv.appendChild(deleteButton);
    
    // Append the new container to the main RMC inputs container
    rmcInputsDiv.appendChild(newEntryDiv);
}

/**
 * Removes a specified repair/maintenance cost (RMC) input field.
 * 
 * @param {string} uniqueID - The unique identifier associated with the set of RMC input fields.
 * @param {number} inputIndex - The index of the RMC input field to be removed.
 */
function removeRMCInput(uniqueID, inputIndex) {
    const entryDiv = document.getElementById('rmc-entry-' + inputIndex + '-' + uniqueID);
    entryDiv.remove();
}

/**
 * Calculates and displays the total repair/maintenance cost (RMC) based on the input fields.
 * 
 * @param {string} uniqueID - The unique identifier associated with the set of RMC input fields.
 */
function calculateRMC(uniqueID) {
    const rmcInputsDiv = document.getElementById('rmc-inputs-' + uniqueID);
    let totalCost = 0;
    
    // Iterate over the RMC input fields and sum the entered values
    for (let i = 0; i < rmcInputsDiv.children.length; i++) {
        const inputField = rmcInputsDiv.children[i].children[1];
        const cost = parseFloat(inputField.value);
        
        if (isNaN(cost)) {
            alert('Please enter valid numbers for all fields.');
            return;
        }
        
        totalCost += cost;
    }

    // Display the total cost in the designated result container
    const resultDiv = document.getElementById('resultRMC-' + uniqueID);
    resultDiv.innerHTML = 'Total Repair and Maintenance Costs: $' + totalCost.toFixed(2);
}
