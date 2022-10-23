function convert_time_string(date_time_object){
    hours = date_time_object.getHours();
    minutes = date_time_object.getMinutes();
    seconds = date_time_object.getSeconds();

    hours = hours<10 ? "0" + hours : hours;
    minutes = minutes<10 ? "0"+minutes : minutes;
    seconds = seconds<10 ? "0"+seconds : seconds;

    time_ = hours + ":" + minutes + ":" + seconds;
    return time_;
}
function convert_seconds_to_string_time(miliseconds){
    hours = Math.floor(miliseconds / (60*60*1000));
    minutes = Math.floor((miliseconds / (60*1000))%60);
    seconds = Math.floor((miliseconds / (1000))%60);

    hours = hours >= 10 ? hours: "0"+hours;
    minutes =minutes >= 10 ? minutes : "0"+minutes;
    seconds = seconds >= 10 ? seconds : "0"+seconds;
    return hours + " : " + minutes + " : " + seconds;
    
}
function get_forex_time(){
    return new Date(new Date().getTime()+ forex_offset);;
}
function forex_time(){
    document.getElementById("forex_clock").innerHTML = convert_time_string(get_forex_time());
    setTimeout(forex_time, 1000);
}

// this function receive args(miliseconds remain time) and add clock style to document
var next_time = "";
function clock_time_remaining(){ 
    // use local time because input date time from python converted to local!!!!
    now_time_forex = new Date();
    
    time_remain = next_time - now_time_forex;
    console.log(time_remain);
    // if time remain (miliseconds) lower 1 seconds...
    if (time_remain < 0){
        next_time = "";
        $("#remain_time_clock").text("waiting")
        eel.get_data(user_id, url_address, interval_time_request);
        id_time_out_remaining = "";
    }else {
        // add one seconds for replace miliseconds... 
        console.log(convert_seconds_to_string_time(time_remain+1000));
        $("#remain_time_clock").text(convert_seconds_to_string_time(time_remain+1000));
        id_time_out_remaining=setTimeout(clock_time_remaining, 1000);
    }
}
function start_stop_btn(){
    document.getElementById("start_btn").onclick = function(){
        if (this.innerHTML=="start"){
            // change to stop
            this.innerHTML = "stop";
            this.style.backgroundColor="rgb(232, 75, 75)";
            insert_text("start program....\n");
            start_stop_time_remaining("waiting");
            eel.get_data(user_id, url_address, interval_time_request);
              
        }else{
            // change to start
            this.innerHTML = "start";
            this.style.backgroundColor="rgb(74, 211, 115)";
            insert_text("stopped program.\n")
            start_stop_time_remaining("stop");
            clearTimeout(id_time_out_remaining);
            eel.stop_btn_clicked();
        }
    }
}
eel.expose(insert_text);
function insert_text(text){
    text_area_element = document.getElementById("text_area");
    pre_text = text_area_element.value;
    text_area_element.value = pre_text + convert_time_string(get_forex_time())+ "    " + text;
    text_area_element.focus();
}
eel.expose(start_stop_time_remaining);
function start_stop_time_remaining(state, new_time_=""){
    if (state=="start"){
        if (id_time_out_remaining == ""){
            // means we start new time out or stopped!!!
            console.log("enter here 1");
            next_time = new Date(new_time_);
            clock_time_remaining();
        }else{
            //this is not allowed condition
            alert("clock time remaining started before....");
        }
        return "ok";

    }
    if (state=="stop"){
        //this means we must stop clock
        clearTimeout(id_time_out_remaining);
        id_time_out_remaining="";
        document.getElementById("remain_time_clock").innerHTML = "stopped";
        return "ok";
    }
    if (state=="waiting"){
        document.getElementById("remain_time_clock").innerHTML = "waiting";
        return "ok";
    }
    alert ("state for clock remaining not correct please check "+state);
}

function check_selected_data(){
    // if user id and url address and interval time selected...(disabled)
    var user_id_el = $(".container .header .user_input input")
    var url_address_el = $(".container .header .url_address input")
    var select_interval_el = $("select")

    if (user_id_el.val()=="" || url_address_el.val() == ""){
        alert("first complete and try again");
    }else {
        
        user_id = user_id_el.val();
        url_address = url_address_el.val();
        interval_time_request = select_interval_el.val();
        user_id_el.prop("disabled", true);
        url_address_el.prop("disabled", true);
        select_interval_el.prop("disabled", true);
        
        $("#start_btn").prop("disabled", false);

    }
}

