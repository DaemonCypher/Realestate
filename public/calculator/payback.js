/**
 * Calculates the payback period given an initial investment and annual cash inflow.
 * The payback period is the time taken for an investment to generate cash flows 
 * equivalent to the initial amount of investment.
 *
 * @param {number} initialInvestment - The initial amount invested.
 * @param {number} annualCashInflow - The annual amount of cash inflow generated from the investment.
 * @returns {number} The calculated payback period in years.
 * @throws Will throw an error if annualCashInflow is zero.
 */
function calculatePaybackPeriod(initialInvestment, annualCashInflow) {
    if (annualCashInflow === 0) {
        throw new Error("Annual cash inflow cannot be zero.");
    }

    const paybackPeriod = initialInvestment / annualCashInflow;
    return paybackPeriod;
}

/**
 * Retrieves initial investment and annual cash inflow from input elements based on a unique ID,
 * then calculates and displays the payback period in the corresponding result element.
 * 
 * @param {string} uniqueID - The unique identifier used to differentiate multiple sets of input and result elements.
 */
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
