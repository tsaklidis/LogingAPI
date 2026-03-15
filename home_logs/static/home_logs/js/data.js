// Sensor UUIDs
var ds18b20 = '9bd60';
var pressure = 'f7909564';
var system = '88cbb2f2';
var wifi = '7a7f970c';

// Single bulk API endpoint
var bulk_url = '/api/open/measurement/bulk/?sensors=' +
    [ds18b20, pressure, system, wifi].join(',');

var same_options = {
    responsive: true,
    animation: { duration: 0 },
    scales: {
        yAxes: [{
            ticks: {},
            gridLines: {
                display: true,
                color: "#4D4D4D",
            },
        }],
        xAxes: [{
            ticks: {
                autoSkip: true,
                maxTicksLimit: 20,
                maxRotation: 45,
            },
            gridLines: {
                display: false,
                color: "#4D4D4D"
            },
        }]
    }
};

Chart.defaults.global.defaultFontColor = "#fff";

// Chart instances (created once, updated on each fetch)
var charts = {};

function createChart(canvasId, label, bgColor, borderColor) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                fill: true,
                backgroundColor: bgColor,
                borderColor: borderColor,
                borderWidth: 2,
                pointRadius: 1,
            }]
        },
        options: same_options
    });
}

createChart('temperature', 'Θερμοκρασία/Temperature (DS18B20 ±0.85%)',
    'rgba(247, 100, 100, 0.3)', 'rgba(247, 100, 100, 1)');
createChart('pressure', 'Βαρόμετρρο / Pressure (BMP280 ±1 hPa)',
    'rgba(200, 70, 255, 0.3)', 'rgba(200, 70, 255, 1)');
createChart('system', 'Θερμοκρασία συστήματος / System temperature',
    'rgba(70, 255, 73, 0.3)', 'rgb(70, 255, 73)');
createChart('wifi', 'Ένταση WiFi / WiFi signal',
    'rgba(14, 246, 227, 0.3)', 'rgb(14, 246, 227)');

// Map sensor UUID to chart canvas ID and display element ID
var sensorMap = {};
sensorMap[ds18b20] = { chart: 'temperature', displayId: 'ds18b20', minId: 'min_tempr', maxId: 'max_tempr' };
sensorMap[pressure] = { chart: 'pressure', displayId: 'bmp280', minId: 'min_prs', maxId: 'max_prs' };
sensorMap[system] = { chart: 'system', displayId: null, minId: null, maxId: null };
sensorMap[wifi] = { chart: 'wifi', displayId: null, minId: null, maxId: null };

function fetchAllData() {
    $.getJSON(bulk_url).done(function(response) {
        var lastTime = '';

        $.each(response, function(sensorUuid, data) {
            var mapping = sensorMap[sensorUuid];
            if (!mapping || data.error) return;

            // Update latest value display
            if (mapping.displayId && data.latest_value !== null) {
                $('#' + mapping.displayId).text(data.latest_value);
            }

            // Update min/max
            if (mapping.minId && data.min_value !== null) {
                $('#' + mapping.minId).text(data.min_value);
            }
            if (mapping.maxId && data.max_value !== null) {
                $('#' + mapping.maxId).text(data.max_value);
            }

            // Track last measurement time
            if (data.last_time) {
                lastTime = data.last_time;
            }

            // Update chart data (no re-creation, just update)
            var chart = charts[mapping.chart];
            if (chart && data.chart_labels) {
                chart.data.labels = data.chart_labels;
                chart.data.datasets[0].data = data.chart_values;
                chart.update();
            }
        });

        // Update "last measurement" timestamp
        if (lastTime) {
            $('#last').text(lastTime);
        }

    }).fail(function(response) {
        console.error('Bulk data fetch failed:', response.status);
    });
}

// Initial load
fetchAllData();

// Auto-refresh every 5 minutes
setInterval(fetchAllData, 5 * 60 * 1000);
