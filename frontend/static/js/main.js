document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('research-form');
    const input = document.getElementById('ticker-input');
    const loadingState = document.getElementById('loading-state');
    const errorMsg = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    const loadingText = document.getElementById('loading-text');

    const cache = {};

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const ticker = input.value.trim().toUpperCase();
        if (!ticker) return;

        // Reset UI
        errorMsg.classList.add('hidden');
        resultsSection.classList.add('hidden');
        
        if (cache[ticker]) {
            renderReport(ticker, cache[ticker]);
            return;
        }

        loadingState.classList.remove('hidden');
        
        try {
            // Step 1: Wake up the API if it's sleeping (Absorbs Render's 50s cold start)
            loadingText.textContent = `Waking up AI Swarm (this can take 50s if sleeping)...`;
            try {
                await fetch(`${window.API_URL}/health`, { method: 'GET' });
            } catch (e) {
                console.log("Health check fetch failed, but continuing just in case.", e);
            }

            // Step 2: Request the report
            loadingText.textContent = `Swarm is actively analyzing ${ticker}...`;
            
            const response = await fetch(`${window.API_URL}/research/report`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ticker })
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || `Server error: ${response.status}`);
            }

            const data = await response.json();
            cache[ticker] = data;
            renderReport(ticker, data);

        } catch (err) {
            errorMsg.textContent = `API Error: ${err.message}`;
            errorMsg.classList.remove('hidden');
        } finally {
            loadingState.classList.add('hidden');
        }
    });

    function renderReport(ticker, data) {
        const report = data.report;
        document.getElementById('report-title').textContent = `🏆 Final Report: ${ticker}`;

        if (report.status === 'success') {
            const reportData = report.data;
            const recValue = (reportData.final_recommendation || 'UNKNOWN').toUpperCase();
            
            const banner = document.getElementById('recommendation-banner');
            banner.className = 'recommendation-banner'; // reset classes
            
            if (recValue === 'BUY') banner.classList.add('recommendation-buy');
            else if (recValue === 'SELL') banner.classList.add('recommendation-sell');
            else banner.classList.add('recommendation-hold');
            
            document.getElementById('recommendation-value').textContent = recValue;
            document.getElementById('executive-summary').textContent = reportData.executive_summary || '';
            
            const driversList = document.getElementById('key-drivers-list');
            driversList.innerHTML = '';
            (reportData.key_drivers || []).forEach(driver => {
                const li = document.createElement('li');
                li.textContent = driver;
                driversList.appendChild(li);
            });
        } else {
            const banner = document.getElementById('recommendation-banner');
            banner.className = 'recommendation-banner recommendation-sell';
            document.getElementById('recommendation-value').textContent = 'ERROR';
            document.getElementById('executive-summary').textContent = report.summary || 'Failed to generate report.';
            document.getElementById('key-drivers-list').innerHTML = '<li>Check agent breakdowns below for details.</li>';
        }

        // Render Agents Grid
        const grid = document.getElementById('agents-grid');
        grid.innerHTML = '';

        for (const [agentName, agentData] of Object.entries(data.findings)) {
            const isSuccess = agentData.status === 'success';
            
            const card = document.createElement('div');
            card.className = 'agent-card';
            
            const header = document.createElement('div');
            header.className = 'agent-header';
            header.innerHTML = `
                <span>${agentName.charAt(0).toUpperCase() + agentName.slice(1)} Agent</span>
                <span class="status-dot ${isSuccess ? 'status-success' : 'status-error'}" title="${agentData.status}"></span>
            `;
            card.appendChild(header);

            if (isSuccess && agentData.data) {
                // Show first 3 key-value pairs
                let count = 0;
                for (const [key, val] of Object.entries(agentData.data)) {
                    if (count >= 3) break;
                    if (typeof val === 'object' || Array.isArray(val)) continue; // skip complex nesting for preview
                    
                    const item = document.createElement('div');
                    item.className = 'agent-data-item';
                    item.innerHTML = `<span class="agent-data-key">${key.replace(/_/g, ' ')}:</span> <span class="agent-data-val">${val}</span>`;
                    card.appendChild(item);
                    count++;
                }
            } else {
                const err = document.createElement('div');
                err.className = 'agent-data-val';
                err.style.color = 'var(--danger)';
                err.textContent = agentData?.summary || 'Data unavailable';
                card.appendChild(err);
            }

            grid.appendChild(card);
        }

        resultsSection.classList.remove('hidden');
    }
});
