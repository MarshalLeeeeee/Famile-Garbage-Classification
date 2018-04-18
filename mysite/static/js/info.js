
    var thisURL = document.URL;
    var  getval =thisURL.split('?')[1];
    var showval= getval.split("=")[1];
    var all_info = showval.split('!');
    console.log(all_info);
    document.getElementById("user_name").value = all_info[0];
    document.getElementById("user_account").innerHTML = all_info[1];
    document.getElementById("user_phone").value = all_info[2];
    document.getElementById("user_address").value = all_info[3]
    info = all_info[4];
    document.getElementById("record").innerHTML = all_info[4];
    str = "<table><tr><td>garbage_id</td><td>username</td><td>collector_id</td></tr>";
    correct_num = info[0];
    error_num = info[1];
    info = info.substring(2);
    var arr_info = new Array();
    arr_info[0] = new Array();
    arr_info[1] = new Array();
    var temp1 = new Array();
    temp1 = info.split("$");
    if(temp1[0]){
        arr_info[0] = temp1[0].split("&");
            for(j=0;j<correct_num;j++) {
            str += "<tr>";
            str += "<td>" + arr_info[0][j] + "</td>";
            str += "</tr>";
        }
    }
    if(temp1[1]){
        arr_info[1] = temp1[1].split("&");
    }

    for(j=0;j<error_num;j++){
        str += "<tr>";
        str += "<td>" + arr_info[1][j] + "</td>";
        str += "</tr>";
    }
    str += "</table>";
    document.getElementById("record").innerHTML = str;
