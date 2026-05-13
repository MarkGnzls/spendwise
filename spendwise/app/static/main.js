// Premium Fintech Dashboard JavaScript

// Theme Management
function applyTheme(theme) {
    const pageShell = document.getElementById('page-shell');
    if (!pageShell) return;

    if (theme === 'dark') {
        pageShell.classList.add('dark-theme');
        pageShell.classList.remove('light-theme');
    } else {
        pageShell.classList.remove('dark-theme');
        pageShell.classList.add('light-theme');
    }

    // Update theme toggle buttons
    const themeButtons = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
    themeButtons.forEach(btn => {
        const icon = btn.querySelector('i');
        const span = btn.querySelector('span');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            span.textContent = 'Light Mode';
        } else {
            icon.className = 'fas fa-moon';
            span.textContent = 'Dark Mode';
        }
    });

    // Save theme preference
    localStorage.setItem('spendwise-theme', theme);

    // Redraw charts with new theme
    setTimeout(() => {
        renderSpendWiseCharts();
    }, 100);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('spendwise-theme') || 'light';
    applyTheme(savedTheme);
}

function toggleTheme() {
    const pageShell = document.getElementById('page-shell');
    const currentTheme = pageShell.classList.contains('dark-theme') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

// Chart Configuration
function getChartColors() {
    const pageShell = document.getElementById('page-shell');
    const isDark = pageShell && pageShell.classList.contains('dark-theme');

    return {
        text: isDark ? '#cbd5e1' : '#475569',
        muted: isDark ? '#94a3b8' : '#64748b',
        border: isDark ? 'rgba(248, 250, 252, 0.1)' : 'rgba(15, 23, 42, 0.1)',
        grid: isDark ? 'rgba(248, 250, 252, 0.06)' : 'rgba(15, 23, 42, 0.06)',
        background: isDark ? '#1e293b' : '#ffffff'
    };
}

function getChartConfig() {
    const colors = getChartColors();

    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: colors.text,
                    font: {
                        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                        size: 12,
                        weight: '500'
                    },
                    padding: 20
                }
            },
            tooltip: {
                backgroundColor: colors.background,
                titleColor: colors.text,
                bodyColor: colors.text,
                borderColor: colors.border,
                borderWidth: 1,
                cornerRadius: 8,
                padding: 12,
                titleFont: {
                    size: 14,
                    weight: '600'
                },
                bodyFont: {
                    size: 13
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: colors.grid,
                    borderColor: colors.border
                },
                ticks: {
                    color: colors.muted,
                    font: {
                        size: 12
                    }
                }
            },
            y: {
                grid: {
                    color: colors.grid,
                    borderColor: colors.border
                },
                ticks: {
                    color: colors.muted,
                    font: {
                        size: 12
                    },
                    callback: function(value) {
                        return '$' + value.toLocaleString();
                    }
                }
            }
        },
        elements: {
            point: {
                hoverRadius: 6,
                radius: 4
            }
        },
        animation: {
            duration: 1000,
            easing: 'easeOutQuart'
        }
    };
}

// Chart Instances Management
const chartInstances = {};

function createChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    // Destroy existing chart
    if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
    }

    const ctx = canvas.getContext('2d');
    const config = {
        type: type,
        data: data,
        options: { ...getChartConfig(), ...options }
    };

    const chart = new Chart(ctx, config);
    chartInstances[canvasId] = chart;
    return chart;
}

// Render Charts
function renderSpendWiseCharts() {
    // Category Pie Chart
    if (typeof categoryLabels !== 'undefined' && typeof categoryData !== 'undefined') {
        const categoryCanvas = document.getElementById('categoryChart');
        if (categoryCanvas) {
            const categoryChartData = {
                labels: categoryLabels,
                datasets: [{
                    data: categoryData,
                    backgroundColor: [
                        '#0ea5e9', '#10b981', '#f59e0b', '#ef4444',
                        '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
                    ],
                    borderWidth: 0,
                    hoverOffset: 8
                }]
            };

            createChart('categoryChart', 'doughnut', categoryChartData, {
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                },
                cutout: '70%'
            });
        }
    }

    // Monthly Overview Chart
    if (typeof monthlyLabels !== 'undefined' &&
        typeof monthlyIncomeData !== 'undefined' &&
        typeof monthlyExpenseData !== 'undefined') {

        const monthlyCanvas = document.getElementById('monthlyChart');
        if (monthlyCanvas) {
            const monthlyChartData = {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Income',
                    data: monthlyIncomeData,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderColor: '#10b981',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2
                }, {
                    label: 'Expenses',
                    data: monthlyExpenseData,
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderColor: '#ef4444',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ef4444',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2
                }]
            };

            createChart('monthlyChart', 'line', monthlyChartData, {
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                }
            });
        }
    }

    // Reports Page Charts
    renderReportsCharts();
}

function renderReportsCharts() {
    // Category Breakdown (Reports)
    const reportCategoryCanvas = document.getElementById('reportCategoryChart');
    if (reportCategoryCanvas && typeof categoryLabels !== 'undefined') {
        const categoryChartData = {
            labels: categoryLabels,
            datasets: [{
                data: categoryData,
                backgroundColor: [
                    '#0ea5e9', '#10b981', '#f59e0b', '#ef4444',
                    '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
                ],
                borderWidth: 0
            }]
        };

        createChart('reportCategoryChart', 'pie', categoryChartData);
    }

    // Source Breakdown (Reports)
    const reportSourceCanvas = document.getElementById('reportSourceChart');
    if (reportSourceCanvas && typeof sourceLabels !== 'undefined') {
        const sourceChartData = {
            labels: sourceLabels,
            datasets: [{
                data: sourceData,
                backgroundColor: [
                    '#10b981', '#0ea5e9', '#f59e0b', '#8b5cf6',
                    '#06b6d4', '#84cc16', '#f97316', '#ef4444'
                ],
                borderWidth: 0
            }]
        };

        createChart('reportSourceChart', 'doughnut', sourceChartData, {
            cutout: '60%'
        });
    }

    // Monthly Trends (Reports)
    const reportLineCanvas = document.getElementById('reportLineChart');
    if (reportLineCanvas && typeof monthlyLabels !== 'undefined') {
        const lineChartData = {
            labels: monthlyLabels,
            datasets: [{
                label: 'Income',
                data: monthlyIncomeData,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }, {
                label: 'Expenses',
                data: monthlyExpenseData,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        };

        createChart('reportLineChart', 'line', lineChartData);
    }
}

// Number Counter Animation
function animateCounter(element, target, duration = 1000) {
    if (!element) return;

    const start = parseFloat(element.textContent.replace(/[$,]/g, '')) || 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = start + (target - start) * easeOutQuart;

        element.textContent = '$' + current.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// Initialize Dashboard
function initDashboard() {
    // Animate stat counters
    const statValues = document.querySelectorAll('.card-value');
    statValues.forEach(value => {
        const text = value.textContent;
        const number = parseFloat(text.replace(/[$,]/g, ''));
        if (!isNaN(number)) {
            animateCounter(value, number);
        }
    });

    // Add fade-in animations to cards
    const cards = document.querySelectorAll('.stats-card, .chart-container, .card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Load saved theme
    loadTheme();

    // Theme toggle buttons
    const themeButtons = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
    themeButtons.forEach(btn => {
        btn.addEventListener('click', toggleTheme);
    });

    // Initialize charts
    renderSpendWiseCharts();

    // Initialize dashboard animations
    if (document.querySelector('.stats-card')) {
        initDashboard();
    }

    // Toast auto-dismiss
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });
});

// Handle window resize for charts
window.addEventListener('resize', function() {
    // Debounce chart redraw
    clearTimeout(window.resizeTimeout);
    window.resizeTimeout = setTimeout(() => {
        renderSpendWiseCharts();
    }, 250);
});

// Export functions for global access
window.SpendWise = {
    toggleTheme,
    renderCharts: renderSpendWiseCharts
};
    setTimeout(() => window.renderSpendWiseCharts(), 100);
});
