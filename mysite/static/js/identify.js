
    var thisURL = document.URL;
    var  getval =thisURL.split('?')[1];
    var showval= getval.split("=")[1];
    var all_info = showval.split('!');
    document.getElementById("user_name").value = all_info[0];
    document.getElementById("user_phone").value = all_info[1];
    document.getElementById("user_address").value = all_info[2]