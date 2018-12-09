$(document).ready(function(){
  $('select').formSelect();
});
$(function() {
    $('#left_panel_select').on('change', function() {
        console.log($('#left_panel_select').val())
    });
});
$(function() {
    $('#next_setup').on('click', function() {
        $('#setup_view').hide()
        $('#setup_config').show()
        leftPanel = $('#left_panel_select').val()
        topBanner = $('#top_banner_select').val()
        if (topBanner) {
            $('#top_form').append(
                '<h5>Top Banner</h5><div class=input-field><input type=text name=top_banner '
                + 'value=' + topBanner + '>'
                + '<label class=active for=left_panel></label>'
                + '</div>'
            )
            $.get(
                '/setup_config/top_banner/' + topBanner,
                function(data) {
                    $.each(data['config_fields'], function(index, value){
                       $('#top_form').append(
                            '<div class=input-field><input type=text name=top_panel_' + index + '>'
                            + '<label class=active for=top_panel_' + index + '>' + value + '</label>'
                            + '</div>'
                        )
                    })
                }
            )
        }
        if (leftPanel) {
            $('#left_form').append(
                '<h5>Left Panel</h5><div class=input-field><input type=text name=left_panel '
                + 'value=' + leftPanel + '>'
                + '<label class=active for=left_panel></label>'
                + '</div>'
            )
            $.get(
                '/setup_config/left_panel/' + leftPanel,
                function(data) {
                    $.each(data['config_fields'], function(index, value){
                       $('#left_form').append(
                            '<div class=input-field><input type=text name=left_panel_' + index + '>'
                            + '<label class=active for=left_panel_' + index + '>' + value + '</label>'
                            + '</div>'
                        )
                    })
                }
            )
        }

    })
})