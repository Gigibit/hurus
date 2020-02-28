var selectedMood;
var selectedMoodWorkPlace;
var selectedMoodDiv;
var freetimeActivities = []
var workplaceActivities = []
var currentTought = '';
var currentToughtWorkplace = '';
var step = 0;
$('#freetime-section').hide()
$('#workplace-mood-section').hide()
$('#workplace-section').hide()
$('#daily-quote-section').hide()


$('#submit-button').click(function(event){
    switch(step){
        case 0:
            evaluateMood()
            break;
        case 1:
            evaluateFreetime()
            break;
        case 2: 
            evaluateMoodWorkPlace()
            break;
        
        case 3: 
            evaluateWorkPlace()
            break;
        case 4:
            location.href='/'
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
$('#current-tought-workplace').on('input propertychange paste', function() {
    currentToughtWorkplace = $(this).val();
});

$(document).on('click','.freetime-box-wrapper', function(){
    let element = $(this)
    let activity = element.data('activity');
    let index = freetimeActivities.indexOf(activity) 
    if( index != -1){
        $(element.children()[0]).removeClass('freetime-box-selected')
        freetimeActivities.splice(index, 1);
    }
    else if (freetimeActivities.length < 5) {
        $(element.children()[0]).addClass('freetime-box-selected')
        freetimeActivities.push(activity);
    } else {
        let selectedActivities = $('.freetime-box-selected')

        let lastActivitySelect = $(selectedActivities[selectedActivities.length - 1 ])
        let indexOfLastSelectedActivity = freetimeActivities.indexOf(lastActivitySelect.parent().data('activity'))
        
        lastActivitySelect.removeClass('freetime-box-selected')
        freetimeActivities.splice(indexOfLastSelectedActivity, 1);
        $(element.children()[0]).addClass('freetime-box-selected')
        freetimeActivities.push(activity);
    }
})
$(document).on('click','.workplace-box-wrapper', function(){
    let element = $(this)
    let activity = element.data('activity')
    let index = workplaceActivities.indexOf(activity) 
    if( index != -1){
        $(element.children()[0]).removeClass('workplace-box-selected')
        workplaceActivities.splice(index, 1);
    }
    else if(workplaceActivities.length < 5 ) {
        $(element.children()[0]).addClass('workplace-box-selected')
        workplaceActivities.push(activity);
    } else {
        let selectedActivities = $('.workplace-box-selected')

        let lastActivitySelect = $(selectedActivities[selectedActivities.length - 1 ])
        let indexOfLastSelectedActivity = workplaceActivities.indexOf(lastActivitySelect.parent().data('activity'))
        
        lastActivitySelect.removeClass('workplace-box-selected')
        workplaceActivities.splice(indexOfLastSelectedActivity, 1);
        $(element.children()[0]).addClass('workplace-box-selected')
        workplaceActivities.push(activity);
    }
})


function evaluateMood(){
    if(selectedMood != null){
        $('#mood-section').hide()
        $('#freetime-section').show()
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
        
        $('#freetime-section').hide()
        $('#workplace-mood-section').show()
        step++
    }
}

function evaluateMoodWorkPlace(){
    if(selectedMoodWorkPlace){
        $('#workplace-mood-section').hide()
        $('#workplace-section').show()
        step++
    }
}


function evaluateWorkPlace(){
    if(workplaceActivities.length > 0){
        let request = {
            'freetime': {
                'selected_mood' : selectedMood,
                'current_tought': currentTought,
                'activities' : freetimeActivities
    
            },
            'workplace': {
                'selected_mood' : selectedMoodWorkPlace,
                'current_tought': currentToughtWorkplace,
                'activities' : workplaceActivities
    
            }
        }
        $.post('/submit_survey/',request, function(response){
            $('#workplace-section').hide()
            $('#daily-quote-section').show()
            $('#quote').text('"' + response['motivational_quote']['text'] +'"')
            if(response['motivational_quote']['author'])
                $('#author').text(response['motivational_quote']['author'])
            if(response.status == 200){
                step++;
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


$('.workplace-mood').click(function(event){
    buttonEnabled = true
    if( selectedMoodDiv != null ){
        selectedMoodDiv.removeClass('mood-selected')
    }
    selectedMoodDiv = $(this)
    selectedMoodWorkPlace = $(this).data('mood')
    selectedMoodDiv.addClass('mood-selected')
});
