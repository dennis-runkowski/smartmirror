// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Rss feed update
callOnInterval(900000, '/right_bottom',
    function(data) {
        
       var rssJsData = data
       var tempData;
       $(rss_table).html("");
       $.each( rssJsData, function( index, value ){
            tempData = "<div>" + value + "</div><div>_______________</div>"
            $(rss_table).append(tempData);

            if (index === 2) {
                return false;
            }
        });
       
});
