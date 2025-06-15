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

        const cells = [
            new Date(tx.timestamp).toLocaleString(),
            tx.user_id,
            tx.merchant_id,
            `$${Number(tx.amount).toFixed(2)}`,
            tx.location,
            tx.device_id,
            null,  // fraud badge
            null   // button
        ];

        cells.forEach((val, i) => {
            const td = document.createElement("td");
            if (i === 6) {
                const span = document.createElement("span");
                span.className = `badge ${tx.is_fraud ? "fraud" : "safe"}`;
                span.textContent = tx.is_fraud ? "Fraud" : "Safe";
                td.appendChild(span);
            } else if (i === 7) {
                const btn = document.createElement("button");
                btn.className = "shap-btn";
                btn.textContent = "Explain";
                btn.addEventListener("click", () => fetchSHAP(tx));
                td.appendChild(btn);
            } else {
                td.textContent = val;
            }
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
        if (tx.is_fraud) fraudCount++;
        totalAmount += tx.amount;
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

async function fetchSHAP(transaction) {
    try {
        const response = await fetch("http://127.0.0.1:8000/explain", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(transaction),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        console.log("✅ SHAP response:", result);

        if (!result.top_features || !Array.isArray(result.top_features)) {
            throw new Error("Response missing 'top_features'");
        }

        const message = result.top_features.map(f =>
            `${f.feature}: ${f.value.toFixed(3)}`
        ).join("\n");

        alert(`✅ Top features influencing prediction:\n\n${message}`);

    } catch (err) {
        console.error("❌ Error in fetchSHAP:", err);
        alert(`Failed to fetch explanation: ${err.message}`);
    }
}

