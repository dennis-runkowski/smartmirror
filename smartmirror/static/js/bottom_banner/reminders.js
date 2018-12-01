// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Check and update Reminders - every 60sec
callOnInterval(10000, "/bottom_banner",
    function(data) {
    	$("#reminders").html("")
        var arraySize = data.length;
        var more = ""
    	$.each(data, function(index) {
            if (index === arraySize - 1) {
                more = ""
            } else if (index >= 0) { 
                more = " & "
            };    
            $("#reminders").append("<span>"+ data[index] + more + "</span>")
        
        });
    }
);