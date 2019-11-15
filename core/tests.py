

def get_toughts():
    return [
    {
      'id' : 0,
      'i18n_key': "ACTIVE",
      'is_happy': True
    },

    {
      'id' : 1,
      'i18n_key': "FOCUSED",
      'is_happy': True
    },
    {
      'id' : 2,
      'i18n_key': "JOYFUL",
      'is_happy': True
    },
    {
      'id' : 3,
      'i18n_key': "INTERESTED",
      'is_happy': True
    },
    {
      'id' : 4,
      'i18n_key': "SERENE",
      'is_happy': True
    },
    {
      'id' : 5,
      'i18n_key': "HOPEFUL",
      'is_happy': True
    },
    {
      'id' : 6,
      'i18n_key': "GLAD",
      'is_happy': True
    },
    {
      'id' : 7,
      'i18n_key': "SURPRISED",
      'is_happy': True
    },
    {
      'id' : 8,
      'i18n_key': "CHEERFUL",
      'is_happy': True
    },
    {
      'id' : 9,
      'i18n_key': "CONFIDENT",
      'is_happy': True
    },
    {
      'id' : 10,
      'i18n_key': "RELIEVED",
      'is_happy': True
    },
    {
      'id' : 11,
      'i18n_key': "IN_LOVE",
      'is_happy': True
    },
    {
      'id' : 12,
      'i18n_key': "ENTHUSIASTIC",
      'is_happy': True
    },
    {
      'id' : 13,
      'i18n_key': "RELAXED",
      'is_happy': True
    },
    {
      'id' : 14,
      'i18n_key': "SATISFACTED",
      'is_happy': True
    },
    {
      'id' : 15,
      'i18n_key': "PROUD",
      'is_happy': True
    },
    {
      'id' : 16,    
      'i18n_key': "SAD",
    },
    {
      'id' : 17,
      'i18n_key': "ASHAMED",
    },
    {
      'id' : 18,
      'i18n_key': "ANXIOUS",
    },
    {
      'id' : 19,
      'i18n_key': "AFRAID",
    },
    {
      'id' : 20,
      'i18n_key': "DEPRESSED",
    },
    {
      'id' : 21,
      'i18n_key': "LONELY",
    },
    {
      'id' : 22,
      'i18n_key': "DELUDED",
    },
    {
      'id' : 23,
      'i18n_key': "ANNOYED",
    },
    {
      'id' : 24,
      'i18n_key': "COLD",
    },
    {
      'id' : 25,
      'i18n_key': "CONFUSED",
    },
    {
      'id' : 26,
      'i18n_key': "PASSIVE",
    },
    {
      'id' : 28,
      'i18n_key': "PREOCCUPIED",
    },
    {
      'id' : 29,
      'i18n_key': "INSECURE",
    },
    {
      'id' : 30,
      'i18n_key': "REPRESSED"
    },
    {
      'id' : 31,
      'i18n_key':"FRURSTRATED"
    },
    {
      'id' : 32,
      'i18n_key': "DISGUSTED",
    },
    {
      'id' : 33,
      'i18n_key': "GUILTY",
    },
    {
      'id' : 34,
      'i18n_key': "DISCOURAGED"
    }
  ]
# Mood.objects.create(i18n_key='HAPPY', value=8, icon='img/mood_icons/happy.ico')
# Mood.objects.create(i18n_key='INSPIRED', value=7, icon='img/mood_icons/inspired.ico')
# Mood.objects.create(i18n_key='CHEERFUL', value=6, icon='img/mood_icons/cheerful.ico')
# Mood.objects.create(i18n_key='IN_A_GOOD_MOOD', value=5, icon='img/mood_icons/in_a_good_mood.ico')
# Mood.objects.create(i18n_key='LOW_ENERGY', value=4, icon='img/mood_icons/low_energy.ico')
# Mood.objects.create(i18n_key='ANGRY', value=3, icon='img/mood_icons/angry.ico')
# Mood.objects.create(i18n_key='SAD', value=2, icon='img/mood_icons/sad.ico')
# Mood.objects.create(i18n_key='AWFUL', value=1, icon='img/mood_icons/awful.ico')

def get_freetime_available_choose():
  return [{
              'id': 0,
              'i18n_key': "Extra_Work",
              'icon':  "img/freetime_icons/Extra_Work.ico"
          },
          {
              'id': 1,
              'i18n_key': "Reading",
              'icon':  "img/freetime_icons/Reading.ico"
          },{
              'id':3,
              'i18n_key': "TV",
              'icon':  "img/freetime_icons/TV.ico"
          },{
              'id':4,
              'i18n_key': "Party",
              'icon':  "img/freetime_icons/Party.ico"
          },{
              'id':5,
              'i18n_key': "Sport",
              'icon':  "img/freetime_icons/Sport.ico"
          },{
              'id':6,
              'i18n_key': "Romantic_Date",
              'icon':  "img/freetime_icons/Romantic_Date.ico"
          },{
              'id':7,
              'i18n_key': "Friends",
              'icon':  "img/freetime_icons/Friends.ico"
          },{
              'id':8,
              'i18n_key': "Family",
              'icon':  "img/freetime_icons/Family.ico"
          },{
              'id':9,
              'i18n_key': "Relax",
              'icon':  "img/freetime_icons/Relax.ico"
          },{
              'id':10,
              'i18n_key': "Helping",
              'icon':  "img/freetime_icons/Helping.ico"
          },{
              'id':11,
              'i18n_key': "Cocktail_bar",
              'icon':  "img/freetime_icons/Cocktail_bar.ico"
          },{
              'id':12,
              'i18n_key': "Restaurant",
              'icon':  "img/freetime_icons/Restaurant.ico"
          },{
              'id':13,
              'i18n_key': "Shopping",
              'icon':  "img/freetime_icons/Shopping.ico"
          },{
              'id':14,
              'i18n_key': "Art",
              'icon':  "img/freetime_icons/Art.ico"
          },{
              'id':15,
              'i18n_key': "Writing",
              'icon':  "img/freetime_icons/Writing.ico"
          },{
              'id':16,
              'i18n_key': "Praying",
              'icon':  "img/freetime_icons/Praying.ico"
          },{
              'id':17,
              'i18n_key': "Studying",
              'icon':  "img/freetime_icons/Studying.ico"
          },{
              'id':18,
              'i18n_key': "Time_in_the_nature",
              'icon':  "img/freetime_icons/Time_in_the_nature.ico"
          },{
              'id':20,
              'i18n_key': "Hobby",
              'icon':  "img/freetime_icons/Hobby.ico"
          },{
              'id':21,
              'i18n_key': "Cleaning_Home",
              'icon':  "img/freetime_icons/Cleaning_Home.ico"
          },{
              'id':22,
              'i18n_key': "Travelling",
              'icon':  "img/freetime_icons/Travelling.ico"
          },{
              'id':23,
              'i18n_key': "Doctor_appointment",
              'icon':  "img/freetime_icons/Doctor_appointment.ico"
          },{
              'id':24,
              'i18n_key': "Cooking",
              'icon':  "img/freetime_icons/Cooking.ico"
          },{
              'id':25,
              'i18n_key': "Videogames",
              'icon':  "img/freetime_icons/Videogames.ico"
          },{
              'id':26,
              'i18n_key': "Phone_call",
              'icon':  "img/freetime_icons/Phone_call.ico"
          },{
              'id':27,
              'i18n_key': "Having_a_walk",
              'icon':  "img/freetime_icons/Having_a_walk.ico"
          },{
              'id':28,
              'i18n_key': "Nothing_at_all",
              'icon':  "img/freetime_icons/Nothing_at_all.ico"
          },{
              'id':29,
              'i18n_key': "Time_with_my_partner",
              'icon':  "img/freetime_icons/Time_with_my_partner.ico"
          },{
              'id': 30,
              'i18n_key': "Cinema",
              'icon':  "img/freetime_icons/Cinema.ico"
          },
]


#marketplace
#['Meeting_with_management','Meeting_with_team','New_Tasks','Team_Rotation','Document_analysis','Held_a_Presentation','Working_with_Time_Pressure','Sick_leave','Everydays_routine','Project_Management' , 'External_Meeting','Worked_Closely_to_a_new_teammate','Mentored_someone']

#for a in ['Meeting_with_management','Meeting_with_team','New_Tasks','Team_Rotation','Document_analysis','Held_a_Presentation','Working_with_Time_Pressure','Sick_leave','Everydays_routine','Project_Management' , 'External_Meeting','Worked_Closely_to_a_new_teammate','Mentored_someone']:
 # Activity.objects.create(activity_type=MARKET_PLACE, i18n_key=a, icon='img/freetime_icons/'+a+'.ico')
