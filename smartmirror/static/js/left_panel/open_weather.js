// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Yahoo data
callOnInterval(6000, '/left_panel',
    function(data) {
       var condition;
       var high;
       var low;
       var date;
       var tableData;
       var forecastIcon;
       var location;
       var units = {
           "imperial": "&#8457;",
           "standard": "&#8490;",
           "metric": "&#8451;"
       };

       if (data) {
           var icon = data["current_weather"]["icon"];
           location = data["current_weather"]["location"];
           var current_temp = data["current_weather"]["temp"];
           var forecastType = data["type"];
           var unit = data["unit"];
           var unitString = units[unit] || "&#8457";
           $("#weather_icon").attr('src', icon);
           $(current_weather).html(current_temp + " " + unitString);
           $(".weather_location").html("Weather in " + location);

            if (data["forecast"] !== "cached") {
                $(weather_table).html("");
                // Daily
                if (forecastType === "daily") {
                    $.each(data["forecast"], function (index, value) {
                        condition = value["description"];
                        low = value["temp_low"];
                        high = value["temp_high"];
                        date = value["date"];
                        forecastIcon = value["icon"];
                        tableData = "<th><div>" + date + "</div><div>High:"
                            + high + " " + unitString + "</div><div>Low:"
                            + low + " " + unitString +"</div><div>"
                            + condition + "</div><div><img id='forecast_icon' src="
                            + forecastIcon + "></div></th>"
                        $(weather_table).append(tableData);
                    })
                } else if (forecastType === 'hourly') {
                    $.each(data["forecast"], function (index, value) {
                        condition = value["description"];
                        temp = value["temp"];
                        date = value["date"];
                        forecastIcon = value["icon"]
                        tableData = "<th><div>" + date + "</div><div>Temperature: "
                            + temp + " " + unitString +"</div><div>"
                            + condition + "</div><div><img id='forecast_icon' src="
                            + forecastIcon + "></div></th>"
                        $(weather_table).append(tableData);
                        if (index === 3) {
                            return false
                        }
                    })
                }
            };
       };
       
});
