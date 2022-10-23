var user_id = "none";
var url_address = "none";
var interval_time_request = 'none';
var days_miliseconds = 24 * 60 * 60 * 1000;
var hours_miliseconds = 60 * 60 * 1000;
var minutes_miliseconds = 60 * 1000;
var seconds_miliseconds = 1000;
var id_time_out_remaining = "";
var forex_offset = -0.5*60*60*1000;

window.addEventListener("load", () => {
    
    // set interval for forex time
    forex_time();

    //start stop function
    start_stop_btn();
    // disable start btn until user input user id
    $("#start_btn").prop("disabled", true);

    // listener for confirm btn
    $("#confirm_btn").click(check_selected_data);
    
})