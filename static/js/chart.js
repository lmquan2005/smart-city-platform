document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('tempChart');
    if (!canvas || typeof cities === 'undefined' || typeof temperatures === 'undefined') {
        return;
    }

    if (!cities.length) {
        return;
    }

    const barColors = temperatures.map((temp) =>
        temp >= 30 ? 'rgba(248, 113, 113, 0.85)' : 'rgba(56, 189, 248, 0.85)'
    );

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: cities,
            datasets: [{
                label: 'Temperature (°C)',
                data: temperatures,
                backgroundColor: barColors,
                borderRadius: 10,
                borderSkipped: false,
                maxBarThickness: 48,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 800,
                easing: 'easeOutQuart',
            },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.96)',
                    titleColor: '#f8fafc',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(148, 163, 184, 0.3)',
                    borderWidth: 1,
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: { weight: '600', size: 13 },
                    bodyFont: { size: 13 },
                    callbacks: {
                        label: (context) => `${context.parsed.y}°C`,
                    },
                },
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: '°C',
                        color: '#64748b',
                        font: { size: 12, weight: '500' },
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 12 },
                        padding: 8,
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.2)',
                        drawTicks: false,
                    },
                    border: {
                        display: false,
                    },
                },
                x: {
                    ticks: {
                        color: '#64748b',
                        font: { size: 12, weight: '500' },
                    },
                    grid: {
                        display: false,
                    },
                    border: {
                        display: false,
                    },
                },
            },
        },
    });
});
