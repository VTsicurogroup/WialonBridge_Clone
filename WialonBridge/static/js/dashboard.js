// Dashboard JavaScript functionality for Wialon Webhook Receiver

// Global variables
let activityChart = null;
let deviceChart = null;
let refreshInterval = null;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    startAutoRefresh();
    setupEventHandlers();
});

// Initialize Chart.js charts
function initializeCharts() {
    initializeActivityChart();
    initializeDeviceChart();
}

// Initialize activity chart (24-hour data)
function initializeActivityChart() {
    const ctx = document.getElementById('activityChart');
    if (!ctx) return;

    activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: generateHourLabels(),
            datasets: [{
                label: 'Data Points',
                data: new Array(24).fill(0),
                borderColor: 'var(--bs-primary)',
                backgroundColor: 'rgba(var(--bs-primary-rgb), 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        title: function(context) {
                            return `Hour ${context[0].label}`;
                        },
                        label: function(context) {
                            return `${context.parsed.y} data points`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        color: 'var(--chart-grid-color, #e9ecef)'
                    },
                    ticks: {
                        color: 'var(--chart-text-color, #6c757d)'
                    }
                },
                y: {
                    display: true,
                    beginAtZero: true,
                    grid: {
                        color: 'var(--chart-grid-color, #e9ecef)'
                    },
                    ticks: {
                        color: 'var(--chart-text-color, #6c757d)',
                        precision: 0
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Initialize device activity chart (doughnut)
function initializeDeviceChart() {
    const ctx = document.getElementById('deviceChart');
    if (!ctx) return;

    // Get data from template variables or use default
    const deviceLabels = window.deviceActivityLabels || [];
    const deviceData = window.deviceActivityData || [];

    deviceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: deviceLabels.length > 0 ? deviceLabels : ['No data'],
            datasets: [{
                data: deviceData.length > 0 ? deviceData : [1],
                backgroundColor: [
                    'var(--bs-primary)',
                    'var(--bs-success)',
                    'var(--bs-info)',
                    'var(--bs-warning)',
                    'var(--bs-danger)',
                    'var(--bs-secondary)',
                    'var(--bs-light)',
                    'var(--bs-dark)'
                ],
                borderWidth: 2,
                borderColor: 'var(--bs-body-bg)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        color: 'var(--chart-text-color, #6c757d)',
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Generate hour labels for activity chart
function generateHourLabels() {
    const labels = [];
    for (let i = 0; i < 24; i++) {
        labels.push(`${i.toString().padStart(2, '0')}:00`);
    }
    return labels;
}

// Start auto-refresh functionality
function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        refreshDashboardData();
    }, 30000); // Refresh every 30 seconds
}

// Stop auto-refresh
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// Refresh dashboard data via API
function refreshDashboardData() {
    fetch('/api/dashboard_stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateActivityChart(data.hourly_data);
            updateStatistics(data);
        })
        .catch(error => {
            console.warn('Failed to refresh dashboard data:', error);
        });
}

// Update activity chart with new data
function updateActivityChart(hourlyData) {
    if (!activityChart || !hourlyData) return;

    // Convert hourly data to 24-hour array
    const chartData = new Array(24).fill(0);
    hourlyData.forEach(item => {
        const hour = parseInt(item.hour);
        if (hour >= 0 && hour < 24) {
            chartData[hour] = item.count;
        }
    });

    activityChart.data.datasets[0].data = chartData;
    activityChart.update('none'); // Update without animation for smoother experience
}

// Update statistics counters
function updateStatistics(data) {
    // Update webhook count if available
    if (data.webhook_count !== undefined) {
        const webhookCountElement = document.getElementById('webhook-count');
        if (webhookCountElement) {
            webhookCountElement.textContent = data.webhook_count;
        }
    }
    
    // Add animation to updated elements
    const updatedElements = document.querySelectorAll('[data-auto-update]');
    updatedElements.forEach(element => {
        element.classList.add('fade-in');
        setTimeout(() => {
            element.classList.remove('fade-in');
        }, 300);
    });
}

// Setup event handlers
function setupEventHandlers() {
    // Handle visibility change to pause/resume auto-refresh
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            stopAutoRefresh();
        } else {
            startAutoRefresh();
        }
    });

    // Handle window focus/blur
    window.addEventListener('focus', function() {
        if (!refreshInterval) {
            startAutoRefresh();
        }
        refreshDashboardData(); // Immediate refresh when window gains focus
    });

    window.addEventListener('blur', function() {
        // Keep running but could be optimized for background
    });
}

// Utility functions for other pages to use
window.WialonDashboard = {
    // Copy text to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            return new Promise((resolve, reject) => {
                if (document.execCommand('copy')) {
                    resolve();
                } else {
                    reject();
                }
                textArea.remove();
            });
        }
    },

    // Format timestamps
    formatTimestamp: function(timestamp) {
        return moment(timestamp).format('YYYY-MM-DD HH:mm:ss');
    },

    // Format time ago
    formatTimeAgo: function(timestamp) {
        return moment(timestamp).fromNow();
    },

    // Show notification
    showNotification: function(message, type = 'info') {
        const alertClass = type === 'error' ? 'danger' : type;
        const alertHtml = `
            <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Find or create notification container
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        
        container.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alerts = container.querySelectorAll('.alert');
            if (alerts.length > 0) {
                alerts[0].remove();
            }
        }, 5000);
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.WialonDashboard;
}
