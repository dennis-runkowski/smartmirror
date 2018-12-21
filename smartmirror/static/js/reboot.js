$(function() {
    $('#restart').click(function(e) {
    	e.preventDefault();
        $.ajax({
            url: '/reboot',
            type: 'POST',
            success: function(response) {
                alert(response['status']);
            }
        })
    })
});