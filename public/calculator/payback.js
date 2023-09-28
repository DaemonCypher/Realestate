function calculatePaybackPeriod(initialInvestment, annualCashInflow) {
    if (annualCashInflow === 0) {
        throw new Error("Annual cash inflow cannot be zero.");
    }

    const paybackPeriod = initialInvestment / annualCashInflow;
    return paybackPeriod;
}

function calculateAndDisplayPaybackPeriod() {
    const initialInvestment = parseFloat(document.getElementById('paybackInvestment').value);
    const annualCashInflow = parseFloat(document.getElementById('annualCashInflow').value);

    try {
        const paybackPeriod = calculatePaybackPeriod(initialInvestment, annualCashInflow);
        document.getElementById('result').innerText = `Payback Period: ${paybackPeriod} years`;
    } catch (error) {
        console.error(error.message);
        document.getElementById('result').innerText = error.message;
    }
}