ocument.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/analysis');
        if (!response.ok) throw new Error("Failed to fetch data from backend");
        
        const data = await response.json();
        const insights = data.insights;
        const txns = data.transactions;
        // Number formatter
        const usdFmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
        // 1. Populate KPIs
        document.getElementById('total-vol').textContent = usdFmt.format(insights.total_value);
        document.getElementById('total-txn').textContent = insights.total_transactions;
        document.getElementById('total-risk').textContent = insights.high_risk_count;
        // 2. Populate Table
        const tbody = document.getElementById('txn-body');
        // Show only latest 10 or so in this view
        txns.slice(0, 15).forEach(t => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${t.TransactionID}</td>
                <td>${t.Date}</td>
                <td>${usdFmt.format(t.Amount)}</td>
                <td>${t.Vendor}</td>
                <td><strong style="color: ${t.IsHighRisk ? '#f85149' : '#2ea043'}">${t.RiskScore}</strong></td>
                <td><span class="badge ${t.IsHighRisk ? 'risk' : 'safe'}">${t.IsHighRisk ? 'Flagged' : 'Cleared'}</span></td>
            `;
            tbody.appendChild(tr);
        });
        // 3. Department Chart using Chart.js
        const deptCtx = document.getElementById('deptChart').getContext('2d');
        const deptNames = Object.keys(insights.departments);
        const deptRisks = Object.values(insights.departments);
        new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels: deptNames,
                datasets: [{
                    data: deptRisks,
                    backgroundColor: ['#86bc25', '#0d1117', '#f85149', '#00d2ff', '#6c757d'],
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    hoverOffset: 4
                }]
            },
            options: {
                cutout: '75%',
                plugins: { 
                    legend: { position: 'right', labels: { color: '#c9d1d9' } } 
                }
            }
        });
        // 4. Trend Chart using Chart.js
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        const dates = Object.keys(insights.risk_trends).sort();
        const counts = dates.map(d => insights.risk_trends[d]);
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'High Risk Flags Detected',
                    data: counts,
                    borderColor: '#f85149',
                    backgroundColor: 'rgba(248, 81, 73, 0.15)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4 // Creates smooth curves
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grid: { color: 'rgba(255,255,255,0.05)' }, 
                        ticks: { stepSize: 1, color: '#8b949e' } 
                    },
                    x: { 
                        grid: { display: false }, 
                        ticks: { color: '#8b949e' } 
                    }
                },
                plugins: { 
                    legend: { labels: { color: '#c9d1d9' } } 
                }
            }
        });
    } catch (err) {
        console.error("Dashboard Loading Error:", err);
        alert("Could not load data. Ensure the backend server is running.");
    }
});
