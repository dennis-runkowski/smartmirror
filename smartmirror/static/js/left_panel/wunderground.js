// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Wunderground data
callOnInterval(360000, '/left_panel',
    function(data) {
        
       var wundergroundData = data
       var condition;
       var temp;
       var time;
       var tableData;
       var for_icon;
       var icon = data["current"]["link"];
       var current_temp = data["current"]["temp_f"];
       if (current_temp !== "Null") {
            $("#weather_icon").attr('src', icon)
            $(current_weather).html(current_temp + " &#8457;")
       }
       if (wundergroundData["forecast"][0]["time"] !== "Error") {
            $(weather_table).html("");
            $.each( wundergroundData["forecast"], function( index, value ){
                condition = value["condition"]
                temp = value["temp"]
                time = value["time"]
                for_icon = value["link"]
                tableData = "<th><div>" + time + "</div><div>" + temp + " &#8457;</div><div>" + condition + "</div><img id='forecast_icon' src=" + for_icon +"></th>"
                $(weather_table).append(tableData);
            });
       };
       
});
