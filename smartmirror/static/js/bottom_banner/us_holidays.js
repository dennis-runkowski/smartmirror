// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Update holidays hourly
callOnInterval(3600000, '/bottom_banner',
    function(data) {
    	var more = ''
    	var arraySize = data.length;
    	$(holidays).html('')
    	$.each(data, function(index, value) {
    		if (index === arraySize - 1) {
    			more = ''
    		} else if (index >= 0) { 
    			more = ' & '
    		};
    		$(holidays).append(value + more);
    	});

    });