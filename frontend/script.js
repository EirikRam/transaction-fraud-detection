const button = document.getElementById("generate-btn");
const table = document.getElementById("transactions");
const loading = document.getElementById("loading");
const summary = document.getElementById("summary");
const tbody = table.querySelector("tbody");

async function fetchData() {
    loading.classList.remove("hidden");
    table.classList.add("hidden");
    summary.classList.add("hidden");
    tbody.innerHTML = "";

    const response = await fetch("http://127.0.0.1:8000/simulate");
    const data = await response.json();

    let fraudCount = 0;
    let totalAmount = 0;

    data.forEach(tx => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${new Date(tx.timestamp).toLocaleString()}</td>
            <td>${tx.user_id}</td>
            <td>${tx.merchant_id}</td>
            <td>$${tx.amount.toFixed(2)}</td>
            <td>${tx.location}</td>
            <td>${tx.device_id}</td>
            <td><span class="badge ${tx.is_fraud ? 'fraud' : 'safe'}">
                ${tx.is_fraud ? 'Fraud' : 'Safe'}
            </span></td>
        `;
        tbody.appendChild(tr);

        totalAmount += tx.amount;
        if (tx.is_fraud) fraudCount++;
    });

    summary.innerHTML = `
        <p><strong>Total Transactions:</strong> ${data.length}</p>
        <p><strong>Total Fraudulent:</strong> ${fraudCount}</p>
        <p><strong>Total Spend:</strong> $${totalAmount.toFixed(2)}</p>
    `;

    loading.classList.add("hidden");
    table.classList.remove("hidden");
    summary.classList.remove("hidden");
}

button.addEventListener("click", fetchData);
window.addEventListener("load", fetchData);

// fetch("/simulate")
//   .then(response => response.json())
//   .then(data => {
//     console.log("Fetched transactions:", data);  // Debug line
//     // rest of the render logic
//   })
//   .catch(error => console.error("Error fetching data:", error));
