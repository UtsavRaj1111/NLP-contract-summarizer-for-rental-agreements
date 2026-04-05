document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Global Document Loading (Unified ID Sync) ---
    const uploadForm = document.getElementById('upload-form-ui');
    const loader = document.getElementById('loader-overlay');

    if (uploadForm && loader) {
        uploadForm.addEventListener('submit', () => {
            loader.style.cssText = 'display: flex !important;';
        });
    }

    // --- 2. Functional Extraction Triggers (Hero & Nav) ---
    const fileInput = document.getElementById('file-input');
    const heroTrigger = document.getElementById('hero-upload-trigger');
    const navTrigger = document.getElementById('nav-upload-trigger');

    const openFileDialog = () => { if (fileInput) fileInput.click(); };
    if (heroTrigger) heroTrigger.addEventListener('click', openFileDialog);
    if (navTrigger) navTrigger.addEventListener('click', openFileDialog);

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                if (heroTrigger) heroTrigger.innerHTML = `<span style="font-size: 0.8rem; opacity: 0.8;">Analyzing...</span>`;
                if (uploadForm) uploadForm.submit();
            }
        });
    }

    // --- 3. Persistent Tab Navigation (Overview & Clauses) ---
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const tabContents = document.querySelectorAll('.tab-content');

    const switchTab = (targetTab) => {
        sidebarLinks.forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.sidebar-link[data-tab="${targetTab}"]`);
        if (activeLink) activeLink.classList.add('active');

        tabContents.forEach(content => {
            content.classList.toggle('active', content.id === `${targetTab}-tab`);
        });

        if (targetTab === 'clauses') animateConfidenceBars();
        if (targetTab === 'overview') renderConfidenceChart();
    };

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = link.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    // --- 4. Analysis Confidence Bar Animation ---
    const animateConfidenceBars = () => {
        const bars = document.querySelectorAll('.conf-inner');
        bars.forEach(bar => {
            const level = bar.getAttribute('data-confidence') || 0;
            setTimeout(() => { bar.style.width = `${level}%`; }, 100);
        });
    };

    // --- 5. Global Gauge Animation (Overview Tab) ---
    const gauge = document.querySelector('.gauge-bar');
    if (gauge) {
        const score = parseInt(gauge.getAttribute('data-quality-score')) || 0;
        const offset = (score * 339.3) / 100;
        gauge.style.strokeDasharray = `0 339.3`;
        setTimeout(() => { gauge.style.strokeDasharray = `${offset} 339.3`; }, 300);
    }

    // --- 6. Interactive Confidence Analytics (Chart.js) ---
    let confidenceChart = null;

    const renderConfidenceChart = () => {
        const ctx = document.getElementById('confidenceChart');
        const payload = document.getElementById('clauses-data-payload');
        
        if (!ctx || !payload) return;

        try {
            const clauses = JSON.parse(payload.innerText);
            const labels = clauses.map(c => c.Clause);
            const data = clauses.map(c => Math.round(c.Confidence * 100));

            if (confidenceChart) confidenceChart.destroy();

            confidenceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'AI Confidence %',
                        data: data,
                        backgroundColor: 'rgba(16, 185, 129, 0.7)',
                        borderColor: '#10B981',
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { 
                            beginAtZero: true, 
                            max: 100,
                            grid: { display: false },
                            ticks: { font: { size: 10 } }
                        },
                        x: { 
                            grid: { display: false },
                            ticks: { font: { size: 10 } }
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Chart Rendering Error:", e);
        }
    };

    // Initial load animations
    if (document.getElementById('clauses-tab')?.classList.contains('active')) animateConfidenceBars();
    if (document.getElementById('overview-tab')?.classList.contains('active')) renderConfidenceChart();
});
