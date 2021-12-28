var api_url = '/api/open/measurement/list/';
var base_url = api_url + '?limit=48&order_by=-created_on&sensor_uuid=';
var base_url_last = api_url + 'last/?sensor_uuid=';
var ds18b20 = '9bd60';
var dht22 = '90eab';
var pressure = 'f7909564';
var system = '88cbb2f2';
var wifi = '7a7f970c';


var info = {
    temperature : {
        all: base_url + ds18b20,
        last: base_url_last + ds18b20,
        uuid: ds18b20,
        id: 'ds18b20'
    },
    humidity: {
        all: base_url + dht22,
        last: base_url_last + dht22,
        uuid: dht22,
        id: 'dht22_h',
    },
    pressure: {
        all: base_url + pressure,
        last: base_url_last + pressure,
        uuid: pressure,
        id: 'bmp280',
    },
    system: {
        all: base_url + system,
        last: base_url_last + system,
        uuid: system,
        id: 'system',
    },
    wifi: {
        all: base_url + wifi,
        last: base_url_last + wifi,
        uuid: wifi,
        id: 'wifi',
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
var sys = document.getElementById("system").getContext('2d');
var wf = document.getElementById("wifi").getContext('2d');

// draw empty chart
var temperature_chart = new Chart(tmp, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Θερμοκρασία/Temperature (DS18B20 ±0.85%)',
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
            label: "Υγρασία/Humidity (DHT-22 +-5%)",
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
            label: 'Βαρόμετρρο / Pressure (BMP280 ±1 hPa)',
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


var system_chart = new Chart(sys, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Θερμοκρασία συστήματος / System temperature',
            data: [],
            "fill":true,
            backgroundColor: [
                'rgba(70, 255, 73, 0.3)',
            ],
            borderColor: [
                'rgb(70, 255, 73)',
            ],
            borderWidth: 2
        }]
    },
    options: same_options
});


var wifi_chart = new Chart(wf, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Ένταση WiFi / WiFi signal',
            data: [],
            "fill":true,
            backgroundColor: [
                'rgba(14, 246, 227, 0.3)',
            ],
            borderColor: [
                'rgb(14, 246, 227)',
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
        var created = '';

        $.each(response.results, function(index, measurement) {
            if (measurement.custom_created_on){
                created = measurement.custom_created_on
            }
            else{
                created = measurement.created_on
            }
            values.push(measurement.value);
            labels.push(extract_time(created));
        });
        chart.data.datasets[0].data = values.reverse();
        chart.data.labels = labels.reverse();
        chart.update(); // update the chart
        $('#last, #to').text(extract_time(created, plus=true));
    });
}

function add_date_filters(url) {
    var date = new Date();
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    return url + '?&date__year=' + year + '&date__month=' + month + '&date__day=' + day;
}


function extract_time(value, plus=false){
    var d = new Date(value);
    if (plus){
        return d.toLocaleString()
    }
    else{
        return d.getHours() + ":" + (d.getMinutes()<10?'0':'') + d.getMinutes()
    }

}

function update_singles(url, id){
    var tries = 0;
    $.getJSON(url, function(response) {
        $('#' + id).text(response.value);

    }).fail(function(response) {
        tries = tries + 1;
        if (response.status > 201 && tries < 6) {
            setTimeout(function(){
                update_singles(url, id)
            },2000);
        }
    });
}

function get_max_min_of_day(sensor, id, max_min){
    var order = '';
    var tries = 0;
    if (max_min == 'min'){
        order = 'value'
    }
    else if(max_min == 'max'){
        order = '-value'
    }
    var url = add_date_filters(api_url) + '&sensor_uuid=' + sensor + '&order_by=' + order + '&limit=1';

    $.getJSON(url, function(response) {
        $('#' + id).html(response.results[0]?.value);

    }).fail(function(response) {
        tries = tries + 1;
        if (response.status > 201 && tries < 6) {
            setTimeout(function(){
                get_max_min_of_day(sensor, id, max_min)
            },2000);
        }
    });
}

ajax_chart(temperature_chart, info.temperature.all);
ajax_chart(humidity_chart, info.humidity.all);
ajax_chart(pressure_chart, info.pressure.all);
ajax_chart(wifi_chart, info.wifi.all)
ajax_chart(system_chart, info.system.all)

update_singles(info.temperature.last, info.temperature.id)
update_singles(info.humidity.last, info.humidity.id)
update_singles(info.pressure.last, info.pressure.id)

get_max_min_of_day(info.temperature.uuid, 'max_tempr', 'max')
get_max_min_of_day( info.temperature.uuid, 'min_tempr', 'min')

get_max_min_of_day( info.humidity.uuid, 'max_hum', 'max')
get_max_min_of_day( info.humidity.uuid, 'min_hum', 'min')

get_max_min_of_day( info.pressure.uuid, 'max_prs', 'max')
get_max_min_of_day( info.pressure.uuid, 'min_prs', 'min')
