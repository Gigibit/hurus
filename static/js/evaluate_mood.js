var selectedMood;
var selectedMoodMarketPlace;
var selectedMoodDiv;
var freetimeActivities = []
var marketplaceActivities = []
var currentTought = '';
var currentToughtMarketplace = '';
var step = 0;
$('#freetime-section').hide()
$('#marketplace-mood-section').hide()
$('#marketplace-section').hide()


$('#submit-button').click(function(event){
    switch(step){
        case 0:
            evaluateMood()
            break;
        case 1:
            evaluateFreetime()
            break;
        case 2: 
            evaluateMoodMarketPlace()
            break;
        
        case 2: 
            evaluateMarketplace()
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
$('#current-tought-marketplace').on('input propertychange paste', function() {
    currentToughtMarketplace = $(this).val();
});

$('.freetime-box-wrapper').click(function(event){
    let element = $(this)
    let activity = element.data('activity')
    if(freetimeActivities.indexOf(activity) != -1){
        $(element.children()[0]).removeClass('freetime-box-selected')
        freetimeActivities.splice(index, 1);
    }
    else {
        $(element.children()[0]).addClass('freetime-box-selected')
        freetimeActivities.push(activity);
        console.log(freetimeActivities)
    }
})
$('.marketplace-box-wrapper').click(function(event){
    let element = $(this)
    let activity = element.data('activity')
    if(marketplaceActivities.indexOf(activity) != -1){
        $(element.children()[0]).removeClass('marketplace-box-selected')
        marketplaceActivities.splice(index, 1);
    }
    else {
        $(element.children()[0]).addClass('marketplace-box-selected')
        marketplaceActivities.push(activity);
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
        
        console.log(freetimeActivities)
        $('#freetime-section').hide()
        $('#marketplace-mood-section').show()
        step++
    }
}

function evaluateMoodMarketPlace(){
    if(selectedMoodMarketPlace){
        $('#marketplace-mood-section').hide()
        $('#marketplace-section').show()
        step++
    }
}


function evaluateMarketPlace(){
    if(marketplaceActivities.length > 0){
        let request = {
            'freetime': {
                'selected_mood' : selectedMood,
                'toughts' : toughts,
                'current_tought': currentTought,
                'activities' : freetimeActivities
    
            },
            'marketplace': {
                'selected_mood' : selectedMoodMarketPlace,
                'current_tought': currentToughtMarketplace,
                'activities' : marketplaceActivities
    
            }
        }
        console.log(request)
        $.post('/submit_survey/',request, function(response){
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


$('.marketplace-mood').click(function(event){
    buttonEnabled = true
    if( selectedMoodDiv != null ){
        selectedMoodDiv.removeClass('mood-selected')
    }
    selectedMoodDiv = $(this)
    selectedMoodMarketPlace = $(this).data('mood')
    selectedMoodDiv.addClass('mood-selected')
});
