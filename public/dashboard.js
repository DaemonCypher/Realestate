function showCalculator(option) {
  var sections = [
    "Payback",
    "ROI",
    "TenantTurnover",
    "RentPerProperty",
    "OER",
    "RMC",
  ];
  sections.forEach(function (section) {
    var elem = document.getElementById(section);
    if (section === option) {
      elem.style.display = "block";
    } else {
      elem.style.display = "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var grid = GridStack.init({
    acceptWidgets: ".grid-stack",
    removable: "#delete-zone",
    removeTimeout: 100,
  });

  grid.on("removed", function (event, items) {
    console.log("Removed ", items.length, " items");
  });

  window.createCard = function () {
    const content = prompt("Enter card content:", "New Card");
    if (content === null || content === "") return;
    const uniqueID = "contentContainer-" + new Date().getTime();
    var widget = grid.addWidget({
        content: `
            <div class="grid-stack-item-content new-card" id="card-${uniqueID}">
                <p style="text-align: center">${content}</p>
                <input type="color" value="#ffffff" onchange="changeCardColor('card-${uniqueID}', this.value)">
                <div class="centered-items">
                    <select class="w3-select w3-padding" onchange="showContent(this.value, '${uniqueID}')">
                        <option value="" disabled selected>Select an option</option>
                        <option value="Payback">Payback Period</option>
                        <option value="ROI">Return on Investment</option>
                        <option value="TenantTurnover">Tenant Turnover</option>
                        <option value="RentPerProperty">Average Rent Price per Property</option>
                        <option value="OER">Operating Expense Ratio</option>
                        <option value="RMC">Repair and Maintenance Costs</option>
                        <!-- ... other options ... -->
                    </select>
                    <div id="${uniqueID}"></div>
                </div>
            </div>`,
        autoPosition: true,
    });
};


window.changeCardColor = function (cardID, colorValue) {
  console.log('changeCardColor called with', cardID, colorValue);
  const cardElement = document.getElementById(cardID);
  cardElement.style.backgroundColor = colorValue;
};




  window.showContent = function (selectedOption, uniqueID) {
    var contentContainer = document.getElementById(uniqueID);
    if (selectedOption === "Payback") {
      contentContainer.innerHTML = `
      <div id="Payback-${uniqueID}" class="content">
      <label for="paybackInvestment-${uniqueID}">Initial Investment:</label>
      <input type="number" id="paybackInvestment-${uniqueID}" name="paybackInvestment-${uniqueID}" required>
      <label for="annualCashInflow-${uniqueID}">Annual Cash Inflow:</label>
      <input type="number" id="annualCashInflow-${uniqueID}" name="annualCashInflow-${uniqueID}" required>
      <input type="button" value="Calculate" onclick="calculateAndDisplayPaybackPeriod('${uniqueID}')">
      <div id="resultPayback-${uniqueID}"></div>
  </div>
      `;
    } else if (selectedOption === "ROI") {
      contentContainer.innerHTML = `
      <div id="ROI-${uniqueID}" class="content">
      <label for="roiInvestment-${uniqueID}">Initial Investment:</label>
      <input type="number" id="roiInvestment-${uniqueID}" name="roiInvestment-${uniqueID}" required>
      <br>
      <label for="finalInvestment-${uniqueID}">Final Value of Investment:</label>
      <input type="number" id="finalInvestment-${uniqueID}" name="finalInvestment-${uniqueID}" required>
      <br>
      <button onclick="calculateROI('${uniqueID}')">Calculate ROI</button>
      <div id="resultROI-${uniqueID}"></div>
  </div>
    `;
    } else if (selectedOption === "TenantTurnover") {
      contentContainer.innerHTML = `
      <div id="TenantTurnover-${uniqueID}" class="content">
      <label for="totalUnits-${uniqueID}">Total Units:</label>
      <input type="number" id="totalUnits-${uniqueID}" name="totalUnits-${uniqueID}" required>
      <br>
      <label for="vacantUnits-${uniqueID}">Vacant Units:</label>
      <input type="number" id="vacantUnits-${uniqueID}" name="vacantUnits-${uniqueID}" required>
      <br>
      <button onclick="calculateTenantTurnover('${uniqueID}')">Calculate Tenant Turnover</button>
      <div id="resultTenantTurnover-${uniqueID}"></div>
  </div>
    `;
    } else if (selectedOption === "RentPerProperty") {
      contentContainer.innerHTML = `
      <div id="RentPerProperty-${uniqueID}" class="content">
      <label for="totalRentCollected-${uniqueID}">Total Rent Collected:</label>
      <input type="number" id="totalRentCollected-${uniqueID}" name="totalRentCollected-${uniqueID}" required>
      <br>
      <label for="numberRentedUnits-${uniqueID}">Number of Rented Units:</label>
      <input type="number" id="numberRentedUnits-${uniqueID}" name="numberRentedUnits-${uniqueID}" required>
      <br>
      <button onclick="calculateAverageRent('${uniqueID}')">Calculate Average Rent</button>
      <div id="resultAverageRent-${uniqueID}"></div>
  </div>
`;
    } else if (selectedOption === "OER") {
      contentContainer.innerHTML = `
      <div id="OER-${uniqueID}" class="content">
      <label for="operatingExpenses-${uniqueID}">Operating Expenses:</label>
      <input type="number" id="operatingExpenses-${uniqueID}" name="operatingExpenses-${uniqueID}" required>
      <br>
      <label for="grossOperatingIncome-${uniqueID}">Gross Operating Income:</label>
      <input type="number" id="grossOperatingIncome-${uniqueID}" name="grossOperatingIncome-${uniqueID}" required>
      <br>
      <button onclick="calculateOER('${uniqueID}')">Calculate OER</button>
      <div id="resultOER-${uniqueID}"></div>
  </div>
`;
    } else if (selectedOption === "RMC") {
      contentContainer.innerHTML = `
      <div id="RMC-${uniqueID}" class="content">
      <div id="rmc-inputs-${uniqueID}">
          <!-- Initial empty container for repair and maintenance inputs -->
      </div>
      <button onclick="addRMCInput('${uniqueID}')">Add Repair/Maintenance</button>
      <button onclick="calculateRMC('${uniqueID}')">Calculate Total Repair and Maintenance Costs</button>
      <div id="resultRMC-${uniqueID}"></div>
  </div>
`;
    } else {
      contentContainer.innerHTML = "";
    }
  };
});
