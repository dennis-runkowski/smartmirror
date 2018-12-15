$(function() {
    $('#upgrade').click(function(e) {
    	e.preventDefault();
        $.ajax({
            url: '/upgrade',
            type: 'POST',
            success: function(response) {
                alert(response['status']);
            }
        })
    })
});