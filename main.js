document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // 2. Mobile Sidebar Toggle
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.querySelector('.mobile-menu-toggle');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('active') && !sidebar.contains(e.target) && e.target !== menuToggle) {
                sidebar.classList.remove('active');
            }
        });
    }

    // 3. Auto-Dismiss Alert Messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Auto-close after 5 seconds
        const timeout = setTimeout(() => {
            dismissAlert(alert);
        }, 5000);

        // Manual close button
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(timeout);
                dismissAlert(alert);
            });
        }
    });

    function dismissAlert(alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }

    // 4. Carbon Footprint Quiz Wizard
    initCarbonWizard();

    // 5. Load Visual Charts
    initCharts();
});

/**
 * Handle Carbon Footprint Quiz Progression
 */
function initCarbonWizard() {
    const wizard = document.getElementById('carbonQuizWizard');
    if (!wizard) return;

    const steps = wizard.querySelectorAll('.quiz-step');
    const prevBtn = wizard.querySelector('#prevStepBtn');
    const nextBtn = wizard.querySelector('#nextStepBtn');
    const progressFill = wizard.querySelector('.quiz-progress-fill');
    
    let currentStep = 0;
    const totalSteps = steps.length;

    function updateWizard() {
        steps.forEach((step, idx) => {
            step.classList.toggle('active', idx === currentStep);
        });

        // Update progress bar
        const progressPercentage = ((currentStep) / (totalSteps - 1)) * 100;
        if (progressFill) {
            progressFill.style.width = `${progressPercentage}%`;
        }

        // Update navigation buttons
        if (currentStep === 0) {
            prevBtn.style.visibility = 'hidden';
        } else {
            prevBtn.style.visibility = 'visible';
        }

        if (currentStep === totalSteps - 1) {
            nextBtn.innerHTML = 'Calculate <i class="lucide-icon" data-lucide="calculator"></i>';
            nextBtn.type = 'submit';
        } else {
            nextBtn.innerHTML = 'Next <i class="lucide-icon" data-lucide="chevron-right"></i>';
            nextBtn.type = 'button';
        }

        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (currentStep < totalSteps - 1) {
                // Perform quick validation on current step inputs
                const currentInputs = steps[currentStep].querySelectorAll('input, select');
                let valid = true;
                currentInputs.forEach(input => {
                    if (input.hasAttribute('required') && !input.value) {
                        valid = false;
                        input.classList.add('is-invalid');
                    } else {
                        input.classList.remove('is-invalid');
                    }
                });

                if (valid) {
                    currentStep++;
                    updateWizard();
                } else {
                    alert('Please complete the current step fields.');
                }
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateWizard();
            }
        });
    }

    updateWizard();
}

/**
 * Chart.js Integration
 */
function initCharts() {
    if (typeof Chart === 'undefined') return;

    // Define common chart styling overrides
    Chart.defaults.color = '#94a3b8'; // text-muted
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    // Dashboard line charts (Carbon Emissions history)
    const carbonHistoryCtx = document.getElementById('carbonHistoryChart');
    if (carbonHistoryCtx) {
        fetch('/api/carbon/history')
            .then(res => res.json())
            .then(data => {
                new Chart(carbonHistoryCtx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Monthly Carbon Footprint (kg CO2e)',
                            data: data.data,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                        }
                    }
                });
            });
    }

    // Dashboard Waste Category breakdown (Donut)
    const wasteBreakdownCtx = document.getElementById('wasteBreakdownChart');
    if (wasteBreakdownCtx) {
        fetch('/api/waste/breakdown')
            .then(res => res.json())
            .then(data => {
                new Chart(wasteBreakdownCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: [
                                '#f87171', // Reduce - Coral red
                                '#fbbf24', // Reuse - Yellow
                                '#10b981'  // Recycle - Green
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            });
    }

    // Water Usage Tracker Trends (Bar Chart)
    const waterChartCtx = document.getElementById('waterChart');
    if (waterChartCtx) {
        fetch('/api/water/trends')
            .then(res => res.json())
            .then(data => {
                new Chart(waterChartCtx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Liters Consumed',
                            data: data.data,
                            backgroundColor: 'rgba(56, 189, 248, 0.6)',
                            borderColor: '#38bdf8',
                            borderWidth: 1,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                        }
                    }
                });
            });
    }

    // Electricity Usage Tracker Trends (Bar Chart)
    const electricityChartCtx = document.getElementById('electricityChart');
    if (electricityChartCtx) {
        fetch('/api/electricity/trends')
            .then(res => res.json())
            .then(data => {
                new Chart(electricityChartCtx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'kWh Consumed',
                            data: data.data,
                            backgroundColor: 'rgba(251, 191, 36, 0.6)',
                            borderColor: '#fbbf24',
                            borderWidth: 1,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                        }
                    }
                });
            });
    }

    // Tree Plantation Variety Distribution (Polar Area / Bar Chart)
    const treeChartCtx = document.getElementById('treeChart');
    if (treeChartCtx) {
        fetch('/api/tree/distribution')
            .then(res => res.json())
            .then(data => {
                new Chart(treeChartCtx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Trees Planted',
                            data: data.data,
                            backgroundColor: 'rgba(52, 211, 153, 0.6)',
                            borderColor: '#34d399',
                            borderWidth: 1,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { precision: 0 } },
                            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                        }
                    }
                });
            });
    }
}
