function snackbar(text){
    var snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    snackbar.innerText = text;
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);

}