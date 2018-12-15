$(document).ready(function(){
  $('select').formSelect();
});
$(function() {
    $('#next_setup').on('click', function() {
        $('#setup_view').hide();
        $('#setup_config').show();
        $('#hide_next').hide();
        $('#hide_save').show();
        leftPanelSelect = $('#left_panel_select').val();
        topBannerSelect = $('#top_banner_select').val();
        rightTopSelect = $('#right_top_select').val();
        rightBottomSelect = $('#right_bottom_select').val();
        bottomBannerSelect = $('#bottom_banner_select').val();

        if (topBannerSelect) {
            getConfig('#top_form', topBannerSelect, 'Top Banner', 'top_banner');
        };
        if (leftPanelSelect) {
            getConfig('#left_form', leftPanelSelect, 'Left Panel', 'left_panel');
        };
        if (rightTopSelect) {
            getConfig(
                '#right_top_form',
                rightTopSelect,
                'Right Top Panel',
                'right_top_panel'
            );
        };
        if (rightBottomSelect) {
            getConfig(
                '#right_bottom_form',
                rightBottomSelect,
                'Right Bottom Panel',
                'right_bottom_panel'
            );
        };
        if (bottomBannerSelect) {
            getConfig(
                '#bottom_form',
                bottomBannerSelect,
                'Bottom Banner',
                'bottom_banner'
            );
        };

    })
})
function getConfig(panelId, selectData, panelName, inputName) {
    $(panelId).append(
        '<h5>' + panelName + '</h5><div class=input-field><input type=text name='
        + inputName + ' value=' + selectData + '>'
        + '<label class=active for=' + inputName + '></label>'
        + '</div>'
    )
    $.get(
        '/setup_config/' + inputName + '/' + selectData,
        function(data) {
            $.each(data['config_fields'], function(index, value){
               $(panelId).append(
                    '<div class=input-field><input type=text name=' + inputName + '_' + index + '>'
                    + '<label class=active for=' + inputName + '_' + index + '>' + value + '</label>'
                    + '</div>'
                )
            })
        }
    )
};
$(function() {
    $('#save_setup').click(function(e) {
    	e.preventDefault();
        $.ajax({
            url: '/save_plugin_config',
            data: $("form").serialize(),
            type: "POST",
            success: function(response) {
                $('#errors').html('')
            	if (response['status'] == 'error') {
            	    $.each(response['message'], function(index, value) {
            	        $('#errors').append(
            	            '<div>'
            	            + response['message'][index] +
            	            '</div>'
            	        )
            	    });
            	} else {
            	    M.toast({html: "Your config is saved! Restart the application or Pi for the changes to effect."})

            	};
            }
        })
    })
});