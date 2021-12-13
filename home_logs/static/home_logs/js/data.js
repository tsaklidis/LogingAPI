
var base_url = '/api/open/measurement/list/?limit=24&order_by=-created_on&sensor_uuid=';
var base_url_last = '/api/open/measurement/list/last/?sensor_uuid=';
var ds18b20 = '9bd60';
var dht22 = '90eab';
var pressure = 'f7909564';


var info = {
    temperature : {
        all: base_url + ds18b20,
        last: base_url_last + ds18b20,
    },
    humidity: {
        all: base_url + dht22,
        last: base_url_last + dht22,
    },
    pressure: {
        all: base_url + pressure,
        last: base_url_last + pressure,
    }
}

var same_options = {
    responsive: true,
    scales: {
        yAxes: [{
            ticks: {
                // beginAtZero:true,
            },
            gridLines: {
                display: true ,
                color: "#4D4D4D",
            },
        }],
        xAxes: [{
            ticks: {
                // beginAtZero:true,
            },
            gridLines: {
                display: false ,
                color: "#4D4D4D"
            },
        }]
    }
};

Chart.defaults.global.defaultFontColor = "#fff";
var tmp = document.getElementById("temperature").getContext('2d');
var hmd = document.getElementById("humidity").getContext('2d');
var prs = document.getElementById("pressure").getContext('2d');

// draw empty chart
var temperature_chart = new Chart(tmp, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Θερμοκρασία (DS18B20 ±0.85%)',
            data: [],
            "fill":true,
            backgroundColor: [
                'rgba(247, 100, 100, 0.3)',

            ],
            borderColor: [
                'rgba(247, 100, 100, 1)',

            ],
            borderWidth: 2
        }]
    },
    options: same_options
});

var humidity_chart = new Chart(hmd, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "Υγρασία (DHT-22 +-5%)",
            data: [],
            "fill":true,
            borderColor: "#3e95cd",
            backgroundColor: [
                'rgba(62, 149, 205, 0.3)',

            ],
            borderWidth: 2
        }]
    },
    options: same_options
});


var pressure_chart = new Chart(prs, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Βαρόμετρρο (BMP280 ±1 hPa)',
            data: [],
            "fill":true,
            backgroundColor: [
                'rgba(200, 70, 255, 0.3)',
            ],
            borderColor: [
                'rgba(200, 70, 255, 1)',
            ],
            borderWidth: 2
        }]
    },
    options: same_options
});

// function to update our chart
function ajax_chart(chart, url, data) {
    var data = data || {};
    var values = [];
    var labels = []

    $.getJSON(url, data).done(function(response) {

        $.each(response.results, function(index, measurement) {
            values.push(measurement.value);
            labels.push(extract_time(measurement.created_on));
        });
        chart.data.datasets[0].data = values.reverse();
        chart.data.labels = labels.reverse();
        chart.update(); // update the chart
    });
}

function add_date_filters(url) {
    var date = new Date();
    const day = date.getDay();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    return url + '&date__year=' + year + '&date__month=' + month + '&date__day=' + day;
}


function extract_time(value){
    var d = new Date(value);
    return d.getHours() + ":" + d.getMinutes()
}

ajax_chart(temperature_chart, info.temperature.all);
ajax_chart(humidity_chart, info.humidity.all);
ajax_chart(pressure_chart, info.pressure.all);

