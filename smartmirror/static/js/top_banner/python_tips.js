// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}
console.log("hello")
console.log(tips_timer)
// Update date/time endpoint every 30m
callOnInterval(tips_timer, '/top_banner',
    function(data) {
    	$("#py_tips").text(data["tip"]);
    });