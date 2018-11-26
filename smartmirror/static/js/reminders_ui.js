$(document).ready(function(){
    $(".datepicker").datepicker();
});
$(document).ready(function(){
    $(".timepicker").timepicker();
});
$(document).ready(function() {
   $("input#input_text, textarea#comment").characterCounter();
});
$(function() {
    $("#submit_reminder").click(function(e) {
    	e.preventDefault();
        console.log("Clicked")
        $("[id$=error]").html("")
        $.ajax({
            url: "/reminders",
            data: $("form").serialize(),
            type: "POST",
            success: function(response) {
            	console.log(response)
            	var status = response["status"]
            	if (status === "error") {
            		var data = response["data"]
            		$.each(data, function( key, value ) {
            			$("#" + key + "_error").html("<div>" + value + "</div>")
            		})
            		$(".hide_errors").show("slow");  
            	} else if (status == "success") {
            		$(".hide_errors").hide("fast");
            		M.toast({html: "Your reminder is saved!"})
            		$('#reminder-form').trigger("reset");
            	}
            }
        })
    })
});
$(function() {
    $("#delete_tab").click(function(e) {
        $("#delete_reminder").show("slow");
        $("#add_reminder").hide("fast")
        $.ajax({
            url: "/get_reminders",
            type: "GET",
            success: function(data) {
                console.log(data)
                $("#reminder_table").html("")
                $.each(data, function(index) {
                    $("#reminder_table").append(
                        "<tr><td>" + data[index]["start"]
                        + "</td><td>" + data[index]["end"] 
                        + "</td><td>" + data[index]["reminder"]
                        + "</td><td><a id='delete_row_" + data[index]["id"] + "'"
                        + "href=# class=material-icons data-id="
                        + data[index]["id"] +"> close </a></td>"
                        + "</td></tr>"
                    )
                })
                $("[id^=delete_row_]").on("click", function() {
                    console.log("delete clicked")
                    id = $(this).data("id")
                    M.toast({html: "Deleting this reminder!"})
                    $.ajax({
                        url: "/delete_reminder/" + id,
                        type: "POST"
                    })
                })

            }
        })
    });
});
$(function() {
    $("#add_tab").click(function(e) {
        $("#delete_reminder").hide("fast");
        $("#add_reminder").show("slow")
    });
});

