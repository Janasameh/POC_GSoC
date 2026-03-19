let telemetryChart;
const API_URL = '/v1/telemetry';

// Initialize Chart.js
function initChart() {
    const ctx = document.getElementById('telemetryChart').getContext('2d');
    
    // Gradient for temperature line
    const tempGradient = ctx.createLinearGradient(0, 0, 0, 400);
    tempGradient.addColorStop(0, 'rgba(244, 63, 94, 0.5)'); // Rose
    tempGradient.addColorStop(1, 'rgba(244, 63, 94, 0.0)');
    
    // Gradient for humidity line
    const humGradient = ctx.createLinearGradient(0, 0, 0, 400);
    humGradient.addColorStop(0, 'rgba(14, 165, 233, 0.5)'); // Sky blue
    humGradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";

    telemetryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: '#f43f5e',
                    backgroundColor: tempGradient,
                    borderWidth: 2,
                    pointBackgroundColor: '#0f172a',
                    pointBorderColor: '#f43f5e',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Humidity (%)',
                    data: [],
                    borderColor: '#0ea5e9',
                    backgroundColor: humGradient,
                    borderWidth: 2,
                    pointBackgroundColor: '#0f172a',
                    pointBorderColor: '#0ea5e9',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f8fafc',
                    bodyColor: '#cbd5e1',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    boxPadding: 4
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    beginAtZero: false,
                    suggestedMin: 15,
                    suggestedMax: 80
                }
            }
        }
    });
}

// Fetch data from API and update UI
async function fetchAndUpdateData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        if (!data || data.length === 0) return;

        // Process data for charts
        const labels = [];
        const temps = [];
        const hums = [];
        const uniqueDevices = new Set();

        data.forEach(record => {
            // Format time HH:MM:SS
            const date = new Date(record.received_at + 'Z'); // parse as UTC
            labels.push(date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'}));
            
            // Extract payload values
            temps.push(record.payload.temperature || null);
            hums.push(record.payload.humidity || null);
            
            // Track unique active devices
            uniqueDevices.add(record.device_id);
        });

        // Update Chart
        telemetryChart.data.labels = labels;
        telemetryChart.data.datasets[0].data = temps;
        telemetryChart.data.datasets[1].data = hums;
        telemetryChart.update();

        // Update Widgets with latest record
        const latestInfo = data[data.length - 1].payload;
        if(latestInfo.temperature !== undefined) {
            document.getElementById('current-temp').innerText = latestInfo.temperature.toFixed(1);
        }
        if(latestInfo.humidity !== undefined) {
            document.getElementById('current-hum').innerText = latestInfo.humidity.toFixed(1);
        }
        
        document.getElementById('active-devices').innerText = uniqueDevices.size;
        
        // Update timestamp
        const now = new Date();
        document.getElementById('last-updated').innerText = `Last updated: ${now.toLocaleTimeString()}`;
        
    } catch (error) {
        console.error('Error fetching telemetry data:', error);
        document.getElementById('last-updated').innerText = 'Connection error. Retrying...';
    }
}

// Initialization and Polling
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    fetchAndUpdateData();
    // Poll every 5 seconds
    setInterval(fetchAndUpdateData, 5000);
});
