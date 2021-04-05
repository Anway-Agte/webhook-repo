/* function that calls python module to fetch data from database and updates the UI */
function getData() {
    $.ajax({
        url: "/webhook/getEvents/",
        type: "post",
        success: function (response) {
            $("#events").html(response);
        },
        error: function (xhr) {

        }
    });
};

/* Calling ajax function after every 15 seconds */

$(document).ready(function () {
    getData();
    setInterval(getData, 15000);
})
