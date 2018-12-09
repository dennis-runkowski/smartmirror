// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Yahoo data
callOnInterval(60000, '/left_panel',
    function(data) {
       var condition;
       var high;
       var low;
       var date;
       var tableData;
       var forecastIcon;
       var location;

       if (data) {
           console.log(data["conditions"][0])
           var icon = data["conditions"][0]["link"];
           var location = data["conditions"][0]["location"]
           var current_temp = data["conditions"][0]["temp"];
           $("#weather_icon").attr('src', icon)
           $(current_weather).html(current_temp + " &#8457;")
           $(".weather_location").html("Weather in " + location)

           $(weather_table).html("");
           $.each(data["forecast"], function( index, value ){
               condition = value["text"]
               low = value["low"]
               high = value["high"]
               date = value["date"]
               forecastIcon = value["link"]
               tableData = "<th><div>" + date + "</div><div>High:"
                   + high + " &#8457;</div><div>Low:"
                   + low + " &#8457;</div><div>"
                   + condition + "</div><img id='forecast_icon' src="
                   + forecastIcon +"></th>"
               $(weather_table).append(tableData);
           });
       };
       
});
