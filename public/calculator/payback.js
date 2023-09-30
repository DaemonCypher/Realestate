function calculatePaybackPeriod(initialInvestment, annualCashInflow) {
    if (annualCashInflow === 0) {
        throw new Error("Annual cash inflow cannot be zero.");
    }

    const paybackPeriod = initialInvestment / annualCashInflow;
    return paybackPeriod;
}

function calculateAndDisplayPaybackPeriod(uniqueID) {
    const initialInvestment = parseFloat(document.getElementById('paybackInvestment-' + uniqueID).value);
    const annualCashInflow = parseFloat(document.getElementById('annualCashInflow-' + uniqueID).value);

    try {
        const paybackPeriod = calculatePaybackPeriod(initialInvestment, annualCashInflow);
        document.getElementById('resultPayback-' + uniqueID).innerText = `Payback Period: ${paybackPeriod} years`;
    } catch (error) {
        console.error(error.message);
        document.getElementById('resultPayback-' + uniqueID).innerText = error.message;
    }
}
