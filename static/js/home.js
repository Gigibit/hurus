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
          console.log(this.selected.isBefore(new Date()))
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
                        let freetime = response['toughts_for_day'][0]
                        let marketplace = response['toughts_for_day'][1]

                        $('#tought-modal-mood-freetime').html('<img class="mood" src="/static/'+ freetime['mood']['icon'] +'"/>')
                        $('#tought-modal-tought-freetime').text(freetime['tought'])
                        let freetimeActivities = JSON.parse(freetime['activities'])
                        if(freetimeActivities){
                            $('#tought-modal-activities-freetime').html()
                            for( var i = 0; i < freetimeActivities.length; i++ ){
                                let activity = freetimeActivities[i]
                                $('#tought-modal-activities-freetime').append(
                                    '<div class="col-md-2 activity-box-container">'+
                                        '<div class="activity-box">' +
                                            '<img class="activity-icon" src="/static/'+ activity['icon']+'"/>'+
                                            '<p>'+ (activity['text'] || activity['name']) +'</p>'+
                                        '</div>'+
                                    '</div>'
                                )
                            }
                        }

                        $('#tought-modal-mood-marketplace').html('<img class="mood" src="/static/'+ marketplace['mood']['icon'] +'"/>')
                        $('#tought-modal-tought-marketplace').text(marketplace['tought'])
                        
                        let marketplaceActivities = JSON.parse(marketplace['activities'])
                        console.log(response)
                        if(marketplaceActivities){
                            $('#tought-modal-activities-marketplace').html()
                            for( var i = 0; i < marketplaceActivities.length; i++ ){
                                let activity = marketplaceActivities[i]
                                $('#tought-modal-activities-marketplace').append(
                                    '<div class="col-md-2 activity-box-container">'+
                                        '<div class="activity-box">' +
                                            '<img class="activity-icon" src="/static/'+ activity['icon']+'"/>'+
                                            '<p>'+ (activity['text']) +'</p>'+
                                        '</div>'+
                                    '</div>'
                                )
                            }
                        }
                        $('#tought-modal-motivational-quote').text(( freetime['motivational_quote'] && freetime['motivational_quote']['text'] ) || (marketplace['motivational_quote'] && marketplace['motivational_quote']['text']))
         
                        $('#tought-modal').modal('toggle')
                        $('#view-statistics').click(function(event){
                            location.href = '/statistics_for_day?day='+day + '&' +'month=' + (month + 1) + '&' +'year='  + year
                        });
                    }
                });
                else {
                  $.ajax({
                    url : '/manager_tought_moods_count_in_day/?day='+ day + '&' +
                    'month=' + ( month + 1 ) + '&' +
                    'year='  + year,
                    method: 'GET',
                    success:function(response){
                      let ftMoods = Object.keys(response['FT'])
                      let mpMoods = Object.keys(response['MP'])
                      console.log(response)
                      $('#tought-modal .modal-content').empty()
                      ftMoods.forEach((value,i)=>{
                        $('#tought-modal .modal-content').append(
                          '<div class="chart">'+
                            '<div id="ft-'+i+'-mood-counter-chart-legend"></div>' +
                            '<canvas id="ft-'+i+'-mood-counter-chart'+'"></canvas>'+
                          '</div>'
                          )
                        doughnutMoodCountChart( 'ft-'+i + '-mood-counter-chart', response['FT'][value])
                      })
                      mpMoods.forEach((value,i)=>{
                        $('#tought-modal .modal-content').append(
                          '<div class="chart">'+
                            '<div id="mp-'+i+'-mood-counter-chart-legend"></div>' +
                            '<canvas id="mp-'+i+'-mood-counter-chart'+'"></canvas>'+
                          '</div>'
                        )
                        doughnutMoodCountChart('mp-' + i + '-mood-counter-chart', response['MP'][value])
                      })
                      $('#tought-modal').modal('toggle')
                    }
                  })
                }
}