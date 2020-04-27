if (document.title=='Blogging App | Login')
{
    var x = document.getElementById('login');
    x.classList.add('active');
}

else if(document.title=="Blogging App | Register")
{
    var x =document.getElementById("register");
    x.classList.add('active');
}

else if(document.title=="Feedback")
{
    var x =document.getElementById("feedback");
    x.classList.add('active');
}


function change()
{
    var ele = document.getElementById('id_feedback');
    var c  =document.getElementById("hint_id_feedback");
    if(ele.value === "")
    {
        c.innerHTML="Currently Typed: 0";
    }
    else{
    c.innerHTML="Currently Typed: "+(ele.value.length+1);
    }
}