function snackbar(text){
    var snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    snackbar.innerText = text;
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);

}
$(document).ready(function(){
    $('giordy').hide()

    addEventListener("keydown", function(event) {

        
        if (event.keyCode == 86){
            $('giordy').show()
            $('div').hide()
            setTimeout(
                function(){
                    $('giordy').css({
                        'height':'5px',
                        'width': '5px'
                    })
                    const interval = setInterval(()=> newPositionCount++>3 ? clearInterval(interval) : newPosition(), 1000)
                }
            ,500)
            document.body.style.background = "violet";
        }
      });
      addEventListener("keyup", function(event) {
        if (event.keyCode == 86){
            $('giordy').hide()
            $('div:not(#spinit)').show()
    
            $('giordy').css({
                'height':'100vh',
                'width': '100vh',
                'display': 'none'
            })
            document.body.style.background = "";
        }
      });

    function newPosition(){
        $('giordy').css({
            "left": Math.random() * window.innerWidth , 
            "top": Math.random() * window.innerHeight
        })
    }
    var newPositionCount = 0;
    $('giordy').hover(function(){
        $('giordy').css({
                        'width': '100vh',
                        'height': '100vh',
                        'top': '0',
                        'left': '0'
                    })
    })
    $('giordy').mouseout(function(){
            $('giordy').css({
                            'width': '5px',
                            'height': '5px',
                        });
           newPosition()
    })

})