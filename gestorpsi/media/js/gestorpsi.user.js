function jsupdateemail() {
    
if (document.getElementsByName("email_mini")[0].value != document.getElementsByName("email_mini_conf")[0].value || document.getElementsByName("email_mini")[0].value == '' || document.getElementsByName("email_mini_conf")[0].value == ''){
    document.getElementsByName("email_mini")[0].value="";
    document.getElementsByName("email_mini_conf")[0].value="";
    return;
}else{
    document.getElementsByName("email")[0].value=document.getElementsByName("email_mini")[0].value
    document.getElementsByName("email_mini")[0].value="";
    document.getElementsByName("email_mini_conf")[0].value="";
}
    
}
