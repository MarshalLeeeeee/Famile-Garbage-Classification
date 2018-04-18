function check(){
    if(document.getElementById("user_password").value!=
        document.getElementById("user_confirm_password").value)
    {
        document.getElementById("warning").innerHTML="   两次密码的输入不一致";
    }else{
        document.getElementById("warning").innerHTML="   ";
    }
}