if(document.title.startsWith("Home"))
{
    var x =document.getElementById("home");
    x.classList.add('active');
}

else if(document.title.startsWith('Profile'))
{
    var x = document.getElementById("profile");
    x.classList.add('active');
}

function change()
{
    var ele = document.getElementById('change');
    var files = document.getElementById("id_image")
    ele.innerHTML="Chosen files: "+files.files.item(0).name;
}