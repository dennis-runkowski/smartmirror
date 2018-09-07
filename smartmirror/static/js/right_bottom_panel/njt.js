// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Departure Vision for NJT
callOnInterval(18000, '/right_bottom', function(data) {     
    if (data[0]["departure_vision"][0]["status"] === "goodnight") {
        console.debug("Goodnight - NJT")  
    } else {
        var step;
        var tempClass;
        var train;
        var direction;
        for (step = 0; step < 2; step++) {
            tempClass = '#stop_' + step
            train = 'The next train is ' + data[0]["departure_vision"][step]['status']
            direction = ' (' + data[0]["departure_vision"][step]['station'] + ')'
            $(tempClass).text(train + direction)
        };
    };
    var scheduleData;
    $("#schedule_list").html("")
    $.each(data[1]['schedule'], function(index, value) {
        if (value !== undefined) {
            scheduleData = "<div id='schedule_" + index + "'>" + value + "</div>"
            $("#schedule_list").append(scheduleData)
        };
        if (index >= 4) {
            return false
        };
    });
});
