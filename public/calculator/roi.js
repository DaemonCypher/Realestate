/**
 * Calculates the Return on Investment (ROI) based on the provided initial and final investments.
 * ROI is computed using the formula: ((finalInvestment - initialInvestment) / initialInvestment) * 100.
 * The result is then displayed on the designated element.
 * 
 * @param {string} uniqueID - The unique identifier associated with the set of ROI input fields.
 */
function calculateROI(uniqueID) {
    // Fetch the initial and final investment values from the input fields
    const initialInvestment = parseFloat(document.getElementById('roiInvestment-' + uniqueID).value);
    const finalInvestment = parseFloat(document.getElementById('finalInvestment-' + uniqueID).value);

    // Check if the provided values are valid numbers
    if (isNaN(initialInvestment) || isNaN(finalInvestment)) {
        alert("Please enter valid numbers for both fields.");
        return;
    }

    // Calculate the ROI
    const roi = ((finalInvestment - initialInvestment) / initialInvestment) * 100;

    // Display the computed ROI in the designated result container
    document.getElementById('resultROI-' + uniqueID).innerText = `Your ROI is: ${roi.toFixed(2)}%`;
}
