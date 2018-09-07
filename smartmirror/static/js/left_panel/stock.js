// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Stock data
callOnInterval(1800000, '/left_panel',
    function(data) {
        
       var stockData = data
       $(stock_table).html("");
       $.each(stockData, function( index, value ){
            tableData = "<tr><td>" + index + ": " + value + "</td></tr>" 
            $(stock_table).append(tableData);

        });
       
});