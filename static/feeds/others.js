function myFunction()
{
  var x = document.getElementById("id_api_key");
  if (x.type === "password") {
      x.type = "text";
  } 
  else {
    x.type = "password";
  }
}