

function get_spaces(url){
    var token = $('#token').val();

    // get_data = {"space_uuid": "875bfbed", "sensor_uuid":"09cbb"};

    $.ajax({ 
        type: 'GET', 
        url: url, 
        // data: get_data, 
        dataType: 'json',
        headers: {
            "Authorization": "Token " + token
          },
        success: function (data) { 

            // var template = $("#houses").html();
            // var templateScript = Handlebars.compile(template);

            // var context = {
            //     houses:data
            // }
            // var theCompiledHtml = templateScript(context);
            // $("#holder").html(theCompiledHtml);
            console.log(data)


        }
    });

}


$(document).ready(function() {
	$('#house').addClass('active');

    get_spaces('/api/house/my/');

});