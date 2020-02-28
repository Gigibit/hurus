class Calendar {
  
  constructor () {
    this.monthDiv = document.querySelector('.cal-month__current')
    this.headDivs = document.querySelectorAll('.cal-head__day')
    this.bodyDivs = document.querySelectorAll('.cal-body__day')
    this.nextDiv = document.querySelector('.cal-month__next')
    this.prevDiv = document.querySelector('.cal-month__previous')
  }
  
  init () {
    moment.locale(window.navigator.userLanguage || window.navigator.language) 
    
    this.month = moment()
    this.today = this.selected = this.month.clone()
    this.weekDays = moment.weekdaysShort(true)
    
    this.headDivs.forEach((day, index) => {
      day.innerText = this.weekDays[index]
    })
    
    this.nextDiv.addEventListener('click', _ => { this.addMonth() })
    this.prevDiv.addEventListener('click', _ => { this.removeMonth() })
    
    this.bodyDivs.forEach(day => {
      day.addEventListener('click', e => {
        const date = +e.target.innerHTML < 10 ? `0${e.target.innerHTML}` : e.target.innerHTML
        
        if (e.target.classList.contains('cal-day__month--next')) {
          this.selected = moment(`${this.month.add(1, 'month').format('YYYY-MM')}-${date}`)
        } else if (e.target.classList.contains('cal-day__month--previous')) {
          this.selected = moment(`${this.month.subtract(1, 'month').format('YYYY-MM')}-${date}`)
        } else {
          this.selected = moment(`${this.month.format('YYYY-MM')}-${date}`)
        }
        if(this.selected.isBefore(new Date())){
          computeDate(this.selected.date(), this.selected.month(), this.selected.year())
        }
        else{
          snackbar(i18n['SELECT_DATE_BEFORE_TODAY'])
        }
        this.update()
      })
    })
    
    this.update()
  }
  
  update () {
    this.calendarDays = {
      first: this.month.clone().startOf('month').startOf('week').date(),
      last: this.month.clone().endOf('month').date()
    }
    
    this.monthDays = {
      lastPrevious: this.month.clone().subtract(1,'months').endOf('month').date(),
      lastCurrent: this.month.clone().endOf('month').date()
    }
    
    this.monthString = this.month.clone().format('MMMM YYYY')
    
    this.draw()
  }
  
  
  addMonth () {
    this.month.add(1, 'month')
    
    this.update()
  }
  
  removeMonth () {
    this.month.subtract(1, 'month')
    
    this.update()
  }
  
  draw () {
    this.monthDiv.innerText = this.monthString
    
    let index = 0
    
    if (this.calendarDays.first > 1) {
      for (let day = this.calendarDays.first; day <= this.monthDays.lastPrevious; index ++) {
        this.bodyDivs[index].innerText = day++
        
        this.cleanCssClasses(false, index)
        
        this.bodyDivs[index].classList.add('cal-day__month--previous')
      } 
    }
    
    let isNextMonth = false
    for (let day = 1; index <= this.bodyDivs.length - 1; index ++) {
      if (day > this.monthDays.lastCurrent) {
        day = 1
        isNextMonth = true
      }
      
      this.cleanCssClasses(true, index)
      
      if (!isNextMonth) {
        if (day === this.today.date() && this.today.isSame(this.month, 'day')) {
          this.bodyDivs[index].classList.add('cal-day__day--today') 
        }
        
        if (day === this.selected.date() && this.selected.isSame(this.month, 'month')) {
          this.bodyDivs[index].classList.add('cal-day__day--selected') 
        }
        
        this.bodyDivs[index].classList.add('cal-day__month--current')
      } else {
        this.bodyDivs[index].classList.add('cal-day__month--next')
      }
      
      this.bodyDivs[index].innerText = day++
    }
  }
  
  cleanCssClasses (selected, index) {
    this.bodyDivs[index].classList.contains('cal-day__month--next') && 
    this.bodyDivs[index].classList.remove('cal-day__month--next')
    this.bodyDivs[index].classList.contains('cal-day__month--previous') && 
    this.bodyDivs[index].classList.remove('cal-day__month--previous')
    this.bodyDivs[index].classList.contains('cal-day__month--current') &&
    this.bodyDivs[index].classList.remove('cal-day__month--current')
    this.bodyDivs[index].classList.contains('cal-day__day--today') && 
    this.bodyDivs[index].classList.remove('cal-day__day--today')
    if (selected) {
      this.bodyDivs[index].classList.contains('cal-day__day--selected') && 
      this.bodyDivs[index].classList.remove('cal-day__day--selected') 
    }
  }
}

$(document).ready(()=>{
  const cal = new Calendar()
  cal.init()
})



function computeDate(day, month, year){
  
  if(!manager)
  $.ajax({
    url : '/tought_for_day/?day='+day + '&' +
    'month=' + (month + 1) + '&' +
    'year='  + year,
    method: 'GET',
    success:function(response){
      try{
        let freetime = response['toughts_for_day'][0]
        let workplace = response['toughts_for_day'][1]

        $('#tought-modal-mood-freetime').html('<img class="mood" src="/static/'+ freetime['mood']['icon'] +'"/>')
        $('#tought-modal-tought-freetime').text(freetime['tought'])
        let freetimeActivities = JSON.parse(freetime['activities'])
        if(freetimeActivities){
          $('#tought-modal-activities-freetime').html('')
          for( var i = 0; i < freetimeActivities.length; i++ ){
            let activity = freetimeActivities[i]
            $('#tought-modal-activities-freetime').append(
              '<div class="col-md-3 activity-box-container">'+
              '<div class="activity-box">' +
              '<img class="activity-icon" src="/static/'+ activity['icon']+'"/>'+
              '<p>'+ (activity['i18n_key'] || activity['name']) +'</p>'+
              '</div>'+
              '</div>'
              )
            }
          }
          
          $('#tought-modal-mood-workplace').html('<img class="mood" src="/static/'+ workplace['mood']['icon'] +'"/>')
          $('#tought-modal-tought-workplace').text(workplace['tought'])
          
          let workplaceActivities = JSON.parse(workplace['activities'])
          if(workplaceActivities){
            $('#tought-modal-activities-workplace').html('')
            for( var i = 0; i < workplaceActivities.length; i++ ){
              let activity = workplaceActivities[i]
              $('#tought-modal-activities-workplace').append(
                '<div class="col-md-3 activity-box-container">'+
                '<div class="activity-box">' +
                '<img class="activity-icon" src="/static/'+ activity['icon']+'"/>'+
                '<p>'+ (activity['i18n_key']) +'</p>'+
                '</div>'+
                '</div>'
                )
              }
            }
            $('#tought-modal-motivational-quote').text(( freetime['motivational_quote'] && freetime['motivational_quote']['text'] ) || (workplace['motivational_quote'] && workplace['motivational_quote']['text']))
            
            $('#tought-modal').modal('toggle')
            $('#view-statistics').click(function(event){
              location.href = '/statistics_for_day?day='+day + '&' +'month=' + (month + 1) + '&' +'year='  + year
            });
          }
          catch(exception){
            snackbar(i18n['COULD_NOT_PROCESS_SELECTED_DATE'])
          }
        }
      });
      else {
        $.ajax({
          url : '/manager_tought_moods_count_in_day/?day='+ day + '&' +
          'month=' + ( month + 1 ) + '&' +
          'year='  + year,
          method: 'GET',
          success:function(response){
            try{
              let ftMoods = Object.keys(response['FT']) || [] 
              let mpMoods = Object.keys(response['MP']) || []
              
              if(ftMoods.length == 0 || mpMoods.length == 0){
                return snackbar(i18n['COULD_NOT_PROCESS_SELECTED_DATE'])
              }

              $('#tought-modal #result').empty()
              
              
              $('#tought-modal #result').append('<div class="row" id="ft-row"></div>')
              $('#ft-row').append('<h1>'+ i18n['FREETIME_MOOD_COUNT'] + '</h1>')
              ftMoods.forEach((value,i)=>{
                $('#ft-row').append(
                  '<div class="chart col-md-3 col-centered">'+
                  '<div id="ft-'+i+'-mood-counter-chart-legend"></div>' +
                  '<canvas id="ft-'+i+'-mood-counter-chart'+'"></canvas>'+
                  '</div>'
                  )
                  doughnutMoodCountChart( 'ft-'+i + '-mood-counter-chart', response['FT'][value])
                })
                
                $('#tought-modal #result').append('<div class="row" id="mp-row"></div>')
                $('#mp-row').append('<h1>'+ i18n['WORKPLACE_MOOD_COUNT'] + '</h1>')
                mpMoods.forEach((value,i)=>{
                  $('#mp-row').append(
                    '<div class="chart col-md-3 col-centered">'+
                    '<div id="mp-'+i+'-mood-counter-chart-legend"></div>' +
                    '<canvas id="mp-'+i+'-mood-counter-chart'+'"></canvas>'+
                    '</div>'
                    )
                    doughnutMoodCountChart('mp-' + i + '-mood-counter-chart', response['MP'][value])
                  })
                  
                  
                  $('#tought-modal').modal('toggle')
                  
                  
                  
                }
                
                catch(exception){
                  snackbar(i18n['COULD_NOT_PROCESS_SELECTED_DATE'])
                }
              }
            })
          }
        }
        
        
        $(document).ready(function() {
          var bindDatePicker = function() {
            $(".date")
            .datetimepicker({
              format: "DD-MM-YYYY",
              icons: {
                time: "fa fa-clock-o",
                date: "fa fa-calendar",
                up: "fa fa-arrow-up",
                down: "fa fa-arrow-down"
              }
            })
            .find("input:first")
            .on("blur", function() {
              // check if the date is correct. We can accept dd-mm-yyyy and yyyy-mm-dd.
              // update the format if it's yyyy-mm-dd
              var date = moment($(this).val(), 'DD-MM-YYYY', true)
              if (date.isValid()) {
                //create date based on momentjs (we have that)
                computeDate(date.date(), date.month(), date.year())
              }
              $(this).val('');
              
            });
          };
          
          var parseDate = function(value) {
            var m = value.match(/^(\d{1,2})(\/|-)?(\d{1,2})(\/|-)?(\d{4})$/);
            if (m)
            value =
            ("00" + m[1]).slice(-2)+ "-" + ("00" + m[3]).slice(-2) + "-" +  m[5];
            
            return value;
          };
          
          bindDatePicker();
        });
        