var selectedMood;
var selectedMoodDiv;
var toughts = []
var freetimeActivities = []
var currentTought = '';
var step = 0;
$('#tought-section').hide()
$('#freetime-section').hide()


$('#submit-button').click(function(event){
    switch(step){
        case 0:
            evaluateMood()
            break;
        case 1:
            evaluateToughts()
            break;
        case 2: 
            evaluateFreetime()
            break;
        
    }
})

$('.tought').click(function(event){
    let element = $(this)
    let tought = element.data('tought')
    let index = toughts.indexOf(tought)
    if( index!= -1){
        element.removeClass('tought-selected')
        toughts.splice(index, 1);
    }
    else {
        element.addClass('tought-selected')
        toughts.push(tought);
    }
})



$('#current-tought').on('input propertychange paste', function() {
    currentTought = $(this).val();
});


$('.freetime-box-wrapper').click(function(event){
    let element = $(this)
    let activity = element.data('activity')
    if(toughts.indexOf(activity) != -1){
        $(element.children()[0]).removeClass('freetime-box-selected')
        freetimeActivities.splice(index, 1);
    }
    else {
        $(element.children()[0]).addClass('freetime-box-selected')
        freetimeActivities.push(activity);
    }
})


function evaluateMood(){
    if(selectedMood != null){
        $('#mood-section').hide()
        $('#tought-section').show()
        step++;
    }
}

function evaluateToughts(){
    if(toughts.length > 0) {
        $('#tought-section').hide()
        $('#freetime-section').show()
        step++;
    }
}


function evaluateFreetime(){
    if(freetimeActivities.length > 0){
        console.log({
            'selected_mood' : selectedMood,
            'toughts' : toughts,
            'current_tought': currentTought,
            'activities' : freetimeActivities
            
        })
        $.post('/submit_survey/',{
            'selected_mood' : selectedMood,
            'toughts' : toughts,
            'current_tought': currentTought,
            'activities' : freetimeActivities
            
        }, function(response){
            if(response.status == 200){
                location.href='/'
            }
        })
    }
}


$('.mood').click(function(event){
    buttonEnabled = true
    if( selectedMoodDiv != null ){
        selectedMoodDiv.removeClass('mood-selected')
    }
    selectedMoodDiv = $(this)
    selectedMood = $(this).data('mood')
    selectedMoodDiv.addClass('mood-selected')
});

