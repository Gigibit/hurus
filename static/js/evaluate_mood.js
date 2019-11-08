var buttonEnabled = false;
var selectedMood;
var selectedMoodDiv;
var button = $('#submit-button')
$('.mood').click(function(event){
    buttonEnabled = true
    if( selectedMoodDiv != null ){
        selectedMoodDiv.removeClass('mood-selected')
    }
    selectedMoodDiv = $(this)
    selectedMood = $(this).data('mood')
    selectedMoodDiv.addClass('mood-selected')
})