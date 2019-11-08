var buttonEnabled = false;
var selectedMood;
var selectedMoodDiv;
var step = 0;
$('#tought-section').hide()
$('#freetime-section').hide()


$('#submit-button').click(function(event){
    if(buttonEnabled){
        buttonEnabled = false;
        step++;
        switch(step){
            case 1:
                $('#mood-section').hide()
                $('#tought-section').show()
                break;

        }
    }

})
$('.mood').click(function(event){
    buttonEnabled = true
    if( selectedMoodDiv != null ){
        selectedMoodDiv.removeClass('mood-selected')
    }
    selectedMoodDiv = $(this)
    selectedMood = $(this).data('mood')
    selectedMoodDiv.addClass('mood-selected')
})