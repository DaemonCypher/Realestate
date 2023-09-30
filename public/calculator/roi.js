function calculateROI(uniqueID) {
    const initialInvestment = parseFloat(document.getElementById('roiInvestment-' + uniqueID).value);
    const finalInvestment = parseFloat(document.getElementById('finalInvestment-' + uniqueID).value);

    if (isNaN(initialInvestment) || isNaN(finalInvestment)) {
        alert("Please enter valid numbers for both fields.");
        return;
    }

    const roi = ((finalInvestment - initialInvestment) / initialInvestment) * 100;
    document.getElementById('resultROI-' + uniqueID).innerText = `Your ROI is: ${roi.toFixed(2)}%`;
}