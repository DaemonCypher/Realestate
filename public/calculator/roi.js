function calculateROI() {
    const initialInvestment = parseFloat(document.getElementById('roiInvestment').value);
    const finalInvestment = parseFloat(document.getElementById('finalInvestment').value);

    if (isNaN(initialInvestment) || isNaN(finalInvestment)) {
        alert("Please enter valid numbers for both fields.");
        return;
    }

    const roi = ((finalInvestment - initialInvestment) / initialInvestment) * 100;
    document.getElementById('resultROI').innerText = `Your ROI is: ${roi.toFixed(2)}%`;
}