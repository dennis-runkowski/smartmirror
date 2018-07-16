// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Departure Vision for NJT
callOnInterval(200000, '/right_bottom',
    function(data) {
        
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
        var i;
        var scheduleClass;
        var stop;
        for (i = 0; i < 5; i++) {
                scheduleClass = '#schedule_' + i
                stop = data[1]['schedule'][i]
                if (stop !== undefined) {
                    scheduleClass = '#schedule_' + i
                    $(scheduleClass).text(stop)
                };
            };
    });
