// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Update chuck jokes hourly
callOnInterval(3600000, '/bottom_banner',
    function(data) {
    	$(chuck).html('')
    	$.each(data, function(index, value) {
    		$(chuck).append(value);
    	});

});