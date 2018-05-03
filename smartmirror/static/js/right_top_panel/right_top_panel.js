// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Update date/time endpoint every 30s
callOnInterval(3000, '/date_time',
    function(data) {
    	$("#time").text(data["time"]);
    	$("#date").text(data["date"]);
    });