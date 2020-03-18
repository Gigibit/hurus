import os, base64, json, random, threading
from datetime import date, datetime, timedelta, time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from helloCurus.settings import BASE_DIR
from django.forms.models import model_to_dict
from django.db.models import Avg
from django.template.defaultfilters import date as _date

from django.db.models import IntegerField, Value
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from helloCurus.settings import CONTACT_EMAILS_RECEIVER


flat = lambda l: [item for sublist in l for item in sublist]
MAX_NUMBER_DISPLAYED = 6

def same_day(date1, date2): return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

def get_icons():
    path = os.path.join(BASE_DIR, 'static/img/freetime_available_icons')
    img_list =os.listdir(path)   
    return ['img/freetime_available_icons/' + src for src in img_list]



def get_toughts():
    return ToughtOption.objects.all()


def get_activity_available_choose():
    return Activity.objects.filter(team=None)


MY_SECRET_FOR_EVER = 'Sara Cannella' # This is input in the form of a string
KDF = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'salt_',
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(KDF.derive(MY_SECRET_FOR_EVER.encode())) # Can only use kdf oncefrom cryptography.fernet import Fernet



def statistics_manager_for_day(request):
    manager = request.user
    moods = Mood.objects.all()
    date_to_evaulate = datetime(year=int(request.GET['year']), 
                                              month=int(request.GET['month']), 
                                              day=int(request.GET['day'])) 
    mood_max_value = max(mood.value for mood in moods )
    analysis = calculate_average_moods(manager, mood_max_value=mood_max_value, end_date=date_to_evaulate)

    last_week_analysis = calculate_average_moods(manager, end_date = previous_friday(date_to_evaulate), mood_max_value=mood_max_value)
    last_month_analysis = calculate_average_moods(manager, end_date = previous_month(date_to_evaulate), mood_max_value=mood_max_value)
    

    first_two_week_of_happycurus= manager.agency.created_at + timedelta(days=14)

    when_everything_started_analysis = calculate_average_moods(manager, end_date=first_two_week_of_happycurus, mood_max_value=mood_max_value)
    



    current_average_ft = round(analysis['freetime_mood_value_percentage'])
    current_average_mp = round(analysis['workplace_mood_value_percentage'])

    average_moods = analysis['average_moods']
    return render(request, 'core/manager/statistics.html', {
        'date_to_evaluate': _date(date_to_evaulate, "d F, Y"),
        'weekly_difference_average_freetime_percentage': round(current_average_ft - last_week_analysis['freetime_mood_value_percentage']),
        'weekly_difference_average_workplace_percentage': round(current_average_mp - last_week_analysis['workplace_mood_value_percentage']),
        
        'monthly_difference_average_freetime_percentage': round(current_average_ft - last_month_analysis['freetime_mood_value_percentage']),
        'monthly_difference_average_workplace_percentage': round(current_average_mp - last_month_analysis['workplace_mood_value_percentage']),
        
        'freetime_toughts': analysis['freetime_toughts'],
        'workplace_toughts': analysis['workplace_toughts'],


        'from_begin_difference_average_freetime_percentage': round(current_average_ft - when_everything_started_analysis['freetime_mood_value_percentage']),
        'from_begin_difference_average_workplace_percentage': round(current_average_mp - when_everything_started_analysis['workplace_mood_value_percentage']),
        'average_mood_freetime_percentage': current_average_ft,
        'average_mood_workplace_percentage': current_average_mp,
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_workplace': analysis['podium_moods_workplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_workplace_activities': analysis['activities_podium_count_workplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_workplace'])+1)))
    })


def manager_tought_moods_count_in_day(request) : return JsonResponse(toughts_until_day(request, True))
def manager_tought_moods_count_overview(request) : return JsonResponse(toughts_until_day(request, False))



def toughts_until_day(request, in_day):

    if in_day:
        toughts = Tought.objects.filter(
                            employee__team__manager = request.user, 
                            created_at__lte= date (int(request.GET['year']), 
                                                    int(request.GET['month']), 
                                                    int(request.GET['day']))
                        )
    else:
        toughts = Tought.objects.filter(
                    employee__team__manager = request.user )
    return {
        'freetime_toughts': [t.to_public_dict() for t in filter(lambda x : x.tought_type == FREETIME, toughts)],
        'workplace_toughts': [t.to_public_dict() for t in filter(lambda x : x.tought_type == WORK_PLACE, toughts)]
    }

def tought_moods_count(request, in_day):
    if in_day:
        toughts = Tought.objects.filter(
                                            employee__team__manager = request.user, 
                                            created_at__year=int(request.GET['year']), 
                                            created_at__month=int(request.GET['month']), 
                                            created_at__day=int(request.GET['day'])
                                        )
    else:
        toughts = Tought.objects.filter( employee__team__manager = request.user)

    moods = {
        FREETIME: {},
        WORK_PLACE : {}
    }

    for tought in toughts:

        if tought.mood.value in [key for key,value in moods.items()]:
            moods[tought.tought_type][tought.mood.value]['count'] += 1
        else:
            moods[tought.tought_type][tought.mood.value] = {
                'value': tought.mood.value,
                'color': tought.mood.color_code,
                'count': 1,
                'icon' : tought.mood.icon.name,
                'name' : translation.gettext(tought.mood.i18n_key)
            } 
    return moods





def statistics_manager(request, manager):
    moods = Mood.objects.all()
    mood_max_value = max(mood.value for mood in moods )
    analysis = calculate_average_moods(manager, mood_max_value=mood_max_value)
    last_week_analysis = calculate_average_moods(manager, end_date = previous_friday(), mood_max_value=mood_max_value)
    last_month_analysis = calculate_average_moods(manager, end_date = previous_month(), mood_max_value=mood_max_value)
    

    first_two_week_of_happycurus= manager.agency.created_at + timedelta(days=14)

    when_everything_started_analysis = calculate_average_moods(manager, end_date=first_two_week_of_happycurus, mood_max_value=mood_max_value)
    



    current_average_ft = round(analysis['freetime_mood_value_percentage'])
    current_average_mp = round(analysis['workplace_mood_value_percentage'])


    
    
    average_moods = analysis['average_moods']
    return render(request, 'core/manager/statistics.html', {
        'weekly_difference_average_freetime_percentage': round(current_average_ft - last_week_analysis['freetime_mood_value_percentage']),
        'weekly_difference_average_workplace_percentage': round(current_average_mp - last_week_analysis['workplace_mood_value_percentage']),
        
        'monthly_difference_average_freetime_percentage': round(current_average_ft - last_month_analysis['freetime_mood_value_percentage']),
        'monthly_difference_average_workplace_percentage': round(current_average_mp - last_month_analysis['workplace_mood_value_percentage']),
        
        'from_begin_difference_average_freetime_percentage': round(current_average_ft - when_everything_started_analysis['freetime_mood_value_percentage']),
        'from_begin_difference_average_workplace_percentage': round(current_average_mp - when_everything_started_analysis['workplace_mood_value_percentage']),
        
        'freetime_toughts': analysis['freetime_toughts'],
        'workplace_toughts': analysis['workplace_toughts'],

        'average_mood_freetime_percentage': current_average_ft,
        'average_mood_workplace_percentage': current_average_mp,
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_workplace': analysis['podium_moods_workplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_workplace_activities': analysis['activities_podium_count_workplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_workplace'])+1)))

    })
def calculate_average_moods(manager, end_date=None, start_date=None, mood_max_value = 8):
    if start_date and end_date :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__gte=start_date, created_at__lte=end_date)
    elif start_date and not end_date :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__gte=start_date)
    elif not start_date and end_date :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__lte=end_date)
    else :
        toughts = Tought.objects.filter(employee__team__manager=manager)
    



    average_moods = []
    count = 0
    average_mood_value_freetime      = .0
    average_mood_value_workplace   = .0

    freetime_toughts = [t for t in toughts if t.tought_type == FREETIME ]
    workplace_toughts = [t for t in toughts if t.tought_type == WORK_PLACE ]

    moods = Mood.objects.all()
    moods_count = {}
    dates = []
    for mood in moods:
        moods_count[mood.value] = 0
    for t in freetime_toughts:
        dates.append( date(t.created_at.year, t.created_at.month, t.created_at.day) )
        moods_count[t.mood.value] += 1
    
    podium_moods_freetime = sorted([{'mood': key, 'count' : value } for key, value in moods_count.items()], key=lambda x: x['count'], reverse=True)

    activities_for_podium_moods = flat([ tought.activities.all().annotate(mood=Value(tought.mood.pk, output_field=IntegerField())).values('name','i18n_key', 'mood') for tought in freetime_toughts if tought.mood.value in [ p['mood'] for p in podium_moods_freetime[:3]] ])

    activity_count_freetime = []
    for mood in moods:
        #max number of activity displayed
        activities = [ 
            {   'name': activity['name'],
                'i18n_key' : translation.gettext( activity['i18n_key'] ) if activity.get('i18n_key', None) else activity['name'],
                'mood' : activity['mood']
            } for activity in activities_for_podium_moods if activity['mood'] == mood.pk]

        if len(activities) > 0 : 
            activity_count_freetime.append({
                'mood_value' : mood.value,
                'mood_icon': mood.icon.name,
                'mood_color_code': mood.color_code,
                'mood_i18n_key': mood.i18n_key,
                'activities': activities
            })


    moods_count = {}
    for mood in moods:
        moods_count[mood.value] = 0
    for t in workplace_toughts:
        moods_count[t.mood.value] += 1
        
    
    podium_moods_workplace = sorted([{'mood': key, 'count' : value } for key, value in moods_count.items()], key=lambda x: x['count'], reverse=True)[:3]

    activities_for_podium_moods = flat([ tought.activities.all().annotate(mood=Value(tought.mood.pk, output_field=IntegerField())).values('name','i18n_key', 'mood') for tought in workplace_toughts if tought.mood.value in [ p['mood'] for p in podium_moods_workplace[:3]] ])
    activity_count_workplace = []
    for mood in moods:
        activities = [ 
        {   'name': activity['name'],
            'i18n_key' : translation.gettext( activity['i18n_key'] ) if activity.get('i18n_key', None) else activity['name'],
            'mood' : activity['mood']
        } for activity in activities_for_podium_moods if activity['mood'] == mood.pk]  #max number of activity displayed
        if len(activities) > 0:
            activity_count_workplace.append({
                'mood_value': mood.value,
                'mood_icon': mood.icon.name,
                'mood_color_code': mood.color_code,
                'mood_i18n_key': mood.i18n_key,
                'activities': activities
            })




    for _date in set(dates):

        average_mood_freetime = calculate_average_mood_for_day(_date, toughts, FREETIME)
        average_mood_workplace = calculate_average_mood_for_day(_date, toughts, WORK_PLACE)
        average_mood_value_freetime += average_mood_freetime / mood_max_value
        average_mood_value_workplace += average_mood_workplace / mood_max_value
        count += 1
        freetime_counts = get_mood_count_for_date(_date, toughts, FREETIME)
        workplace_counts = get_mood_count_for_date(_date, toughts, WORK_PLACE)
        
        average_moods.append({
            'date' : _date,
            'average_mood_freetime' : average_mood_freetime,
            'average_mood_workplace' : average_mood_workplace,
            'moods' : {
                'freetime_moods_count': freetime_counts,
                'workplace_moods_count': workplace_counts
            }
        })



    return {
        'freetime_toughts' :  [t.to_public_dict() for t in filter( lambda t : t.tought_type == FREETIME, toughts)],
        'workplace_toughts' : [t.to_public_dict() for t in filter( lambda t : t.tought_type == WORK_PLACE, toughts)],
        'freetime_mood_value_percentage' : (average_mood_value_freetime / count if count > 0 else average_mood_value_freetime + 1) * 100,
        'workplace_mood_value_percentage' : (average_mood_value_workplace/ count if count > 0 else average_mood_value_workplace + 1) * 100,
        'average_moods' : sorted(average_moods, key=lambda x: x['date'], reverse=False),
        'podium_moods_freetime' : podium_moods_freetime,
        'activities_podium_count_freetime': sorted(activity_count_freetime, key=lambda x: x['mood_value'],reverse=False),
        'podium_moods_workplace' : podium_moods_workplace,
        'activities_podium_count_workplace': sorted(activity_count_workplace, key=lambda x: x['mood_value'],reverse=False)
    }


def android_app_link(request):
    return JsonResponse([{
                "relation": ["delegate_permission/common.handle_all_urls"],
                "target": {
                    "namespace": "android_app",
                    "package_name": "it.nogood.container",
                    "sha256_cert_fingerprints":
                    ["4D:54:10:DF:C5:B6:92:49:A8:8C:84:40:CB:C6:26:9C:E6:D0:AD:E2:8D:31:FE:9F:78:F4:27:0A:32:63:6C:12", "21:A9:0A:67:68:4D:03:EC:EB:54:16:C5:E9:97:E5:D6:FA:8C:C4:69:50:30:BA:4C:49:08:3E:B5:E6:3A:1E:0D"]
                }
            }
        ], safe=False)

def previous_friday(of_date = None):
    current_time = of_date if of_date else datetime.now()

    # get friday, one week ago, at 16 o'clock
    last_friday = (current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=4, weeks=-1))
    last_friday_at_16 = datetime.combine(last_friday, time(16))

    # if today is also friday, and after 16 o'clock, change to the current date
    one_week = timedelta(weeks=1)
    if current_time - last_friday_at_16 >= one_week:
        last_friday_at_16 += one_week
    return last_friday_at_16

def previous_month(of_date = None): return (of_date if of_date else date.today()).replace(day=1) - timedelta(days=1)


def get_mood_count_for_date(_date, toughts, for_type):
    moods = {}
    for mood in Mood.objects.all():
        moods[mood.value] = 0
    for tought in filter(lambda t: same_day(t.created_at,_date), toughts):
        if(tought.tought_type == for_type):
            moods[tought.mood.value] += 1

    return moods


def calculate_average_mood_for_day(_date, toughts, for_type):
    count = 0
    moods = 0

    for tought in filter(lambda t: same_day(t.created_at, _date), toughts):

        if tought.tought_type == for_type:
            count += 1
            moods += tought.mood.value

    return moods/count if count > 0 else 1




def e_learning_manager(request, manager):
    
    courses = list(Course.objects.filter(language__iexact=request.user.preferred_language))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    if len(not_seen_courses) == 0:
        request.user.seen_courses.set([])
        not_seen_courses = courses
        request.user.course_to_see = None
        request.user.last_seen_course_date = None
        request.user.save()


    if request.user.has_to_get_new_course():
        # shuffle if new course has to change
        not_seen_course = random.sample(not_seen_courses, len(not_seen_courses))
        course_to_see = not_seen_courses[0] if len(not_seen_course) > 0 else None
        request.user.course_to_see = course_to_see
        request.user.last_seen_course_date =  datetime.now()
        # request.user.seen_courses.add(course_to_see)
        request.user.save()
    else:
        course_to_see = request.user.course_to_see


    courses_check_list = []
    employees = Employee.objects.filter(team__manager = manager)
    employees_length = len(employees)

    for c in courses:
        employees_that_have_seen_courses = len(list(filter(lambda e: c in e.seen_courses.all(), employees)))
        if c.pk != course_to_see.pk:
            courses_check_list.append({
                'seen' : c in request.user.seen_courses.all(),
                'employees_counter':  "%d/%d"%(employees_that_have_seen_courses, employees_length),
                'course': c
            })

    course_to_see_counter =  "%d/%d"%(len(list(filter(lambda e: course_to_see in e.seen_courses.all(), employees))),employees_length)
    return render(request, 'core/manager/e_learning.html', {
        'courses': sorted(courses_check_list, key=lambda c: c['seen'], reverse=True),
        'course_to_see': course_to_see,
        'course_to_see_counter' : course_to_see_counter
    })



def home_employee(request, employee):
    courses = list(Course.objects.filter(language__iexact=request.user.preferred_language))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    if len(not_seen_courses) == 0:
        request.user.seen_courses.set([])
        not_seen_courses = courses
        request.user.course_to_see = None
        request.user.last_seen_course_date = None
        request.user.save()
    toughts = [ tought.to_public_dict() for tought in Tought.objects.filter(employee = employee).order_by('created_at') ]
    moods = Mood.objects.all()
    return render(request, 'core/employee/index.html', {
        'moods' : moods,
        'toughts' : filter( lambda t : t['tought_type'] == FREETIME, toughts),
        'workplace_toughts' : filter( lambda t : t['tought_type'] == WORK_PLACE, toughts),
        'courses': not_seen_courses[:6],
    })


def statistics_employee(request, employee):
    toughts = [ tought.to_public_dict() for tought in Tought.objects.filter(employee = employee).order_by('created_at') ]
    moods = Mood.objects.all()
    return render(request, 'core/employee/statistics.html', {
        'moods' : moods,
        'toughts' : filter( lambda t : t['tought_type'] == FREETIME, toughts),
        'workplace_toughts' : filter( lambda t : t['tought_type'] == WORK_PLACE, toughts)
    })





def e_learning_employee(request, employee):
    courses = list(Course.objects.filter(language__iexact=request.user.preferred_language))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    # if len(not_seen_courses) == 0:
    #     request.user.seen_courses.set([])
    #     not_seen_courses = courses
    #     request.user.course_to_see = None
    #     request.user.last_seen_course_date = None
    #     request.user.save()


    if request.user.has_to_get_new_course() and len(not_seen_courses) > 0:
        not_seen_course = random.sample(not_seen_courses, len(not_seen_courses))
        course_to_see = not_seen_courses[0]
        request.user.course_to_see = course_to_see
        request.user.last_seen_course_date =  datetime.now()
        # request.user.seen_courses.add(course_to_see)
        request.user.save()
    else:
        course_to_see = request.user.course_to_see


    courses_check_list = []
    for c in courses:
        if course_to_see and c.pk != course_to_see.pk:
            courses_check_list.append({
                'seen' : c in request.user.seen_courses.all(),
                'course': c
            })
    return render(request, 'core/employee/e_learning.html', {
        'courses': sorted(courses_check_list, key=lambda c: c['seen'], reverse=True),
        'course_to_see': course_to_see
    })

@login_required(login_url='/website')
def e_learning_detail(request,id):
    course = Course.objects.get(pk=id)
    if course not in request.user.seen_courses.all():
        request.user.seen_courses.add(course)
    if request.user.course_to_see and request.user.course_to_see.pk == course.pk:
        request.user.course_to_see = None
    request.user.save()

    return render(request, 'core/employee/e_learning_detail.html', {
        'course': course,
        'sections' : course.sections.all()
    })

@csrf_exempt
def add_activity(request):
    if request.method == 'POST':
        employee = Employee.objects.get(email = request.user.email)
        activity_name   = request.POST['name']
        image_src       = request.POST['src']
        activity_type   = request.POST['type']

        activity = Activity.objects.create(
            activity_type = activity_type,
            team = employee.team,
            name  = activity_name,
            icon =  image_src
        )
        activity.save()
        return JsonResponse({
            'icon' : activity.icon.name,
            'name' : activity.name,
            'id'   : activity.pk
        })


def check_survey(fn, request, employee):
    toughts = get_toughts()
    default_activity_choose = get_activity_available_choose()
    available_icons = get_icons()
    moods = Mood.objects.all()

    if employee.team:
        team_activity_choose = Activity.objects.filter(team=employee.team)
    else:
        team_activity_choose = []
        employee = Employee.objects.get(email = request.user.email)
    if not employee.has_seen_daily_survey():
        return render(request, 'core/employee/evaluate_mood.html', {
            'toughts':toughts,
            'moods' : moods,
            'available_icons' : available_icons,
            'freetime_available_choose':  filter( lambda a : a.activity_type == FREETIME, default_activity_choose),
            'team_freetime_available_choose':  filter( lambda a : a.activity_type == FREETIME, team_activity_choose),
            'workplace_available_choose':  filter( lambda a : a.activity_type == WORK_PLACE, default_activity_choose),
            'team_workplace_available_choose':  filter( lambda a : a.activity_type == WORK_PLACE, team_activity_choose),

        })
    return fn(request, employee)


def get_employee_from_request_user(user):
    return user, not user.is_manager()

@csrf_exempt
def tought_for_day(request):

    try:
        toughts_for_day = Tought.objects.filter(
            created_at__day=request.GET['day'],
            created_at__month=request.GET['month'],
            created_at__year=request.GET['year'],
            employee__email = request.user.email
        )
        
        moods = Mood.objects.all()
        return JsonResponse({
             'toughts_for_day' : [t.to_public_dict(deep=True) for t in toughts_for_day]
        })
    except Tought.DoesNotExist:
        return JsonResponse({})

@login_required(login_url='/website')
def statistics_for_day(request):
    date_to_evaulate = date(year=int(request.GET['year']), 
                                        month=int(request.GET['month']), 
                                        day=int(request.GET['day']))

    toughts = [t.to_public_dict() for t in Tought.objects.filter(
                            created_at__lte   = date_to_evaulate,
                            employee__email = request.user.email
    ).order_by('created_at')]
    
    moods = Mood.objects.all()
    return render(request, 'core/employee/statistics.html', {
        'moods' : moods,
        'toughts' : filter( lambda t : t['tought_type'] == FREETIME, toughts),
        'workplace_toughts' : filter( lambda t : t['tought_type'] == WORK_PLACE, toughts)
    })

@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        #freetime
        employee = Employee.objects.get(email = request.user.email)
        employee.last_seen_survey = datetime.now()
        employee.save()
        mood = Mood.objects.get(pk=request.POST['freetime[selected_mood]'])

        sentences = list(EncouragingSentence.objects.filter(language=request.user.preferred_language).exclude(pk__in= request.user.read_encouraging_sentences.all().values('pk')))
        if len(sentences) == 0:
            daily_quote = EncouragingSentence.objects.filter(language=request.user.preferred_language).first()
            if daily_quote:
                request.user.read_encouraging_sentences.set([daily_quote])
        else:
            daily_quote = random.sample(sentences, len(sentences))[0]
            if daily_quote:
                request.user.read_encouraging_sentences.add(daily_quote)

        request.user.save()


        activities = Activity.objects.filter(pk__in=request.POST.getlist('freetime[activities][]'))
        tought = Tought.objects.create(  
                        tought_type = FREETIME,
                        mood=mood,
                        motivational_quote= daily_quote,
                        text=request.POST['freetime[current_tought]'],
                        employee=employee
                        )

        if activities and len(activities) > 0:
            tought.activities.add(*activities)


        ### workplace
        employee = Employee.objects.get(email = request.user.email)
        employee.last_seen_survey = datetime.now()
        employee.save()
        mood = Mood.objects.get(pk=request.POST['workplace[selected_mood]'])
        activities = Activity.objects.filter(pk__in=request.POST.getlist('workplace[activities][]'))
        tought = Tought.objects.create(  
                        tought_type=WORK_PLACE,
                        mood=mood,
                        motivational_quote=daily_quote,
                        text=request.POST['workplace[current_tought]'],
                        employee=employee
                        )
        if activities and len(activities) > 0:
            tought.activities.add(*activities)



        return JsonResponse({
          'status' : 200,
          'motivational_quote' : model_to_dict(daily_quote) if daily_quote else '…'
        })
    return None

@login_required(login_url='/website')
def home(request):
    user, is_employee = get_employee_from_request_user(request.user)
    if user:
        user.preferred_language = request.LANGUAGE_CODE.upper()
        threading.Thread(target=user.save).start()
        
    return check_survey(home_employee, request, user) if is_employee else home_manager(request, user)

@login_required(login_url='/website')
def statistics(request):
    user, is_employee = get_employee_from_request_user(request.user)
    return check_survey(statistics_employee, request, user) if is_employee else statistics_manager(request, user)

@login_required(login_url='/website')
def happy_corus(request):
    curus = Curus.objects.get(language__iexact= request.user.preferred_language)
    return render(request, 'core/employee/happy_curus.html', {
        'curus': curus,
    })
    
    
@login_required(login_url='/website')
def e_learning(request):
    user, is_employee = get_employee_from_request_user(request.user)
    return check_survey(e_learning_employee, request, user) if is_employee else e_learning_manager(request, user)


   


def home_manager(request, manager):
    courses = list(Course.objects.filter(language__iexact=request.user.preferred_language))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    if len(not_seen_courses) == 0:
        request.user.seen_courses.set([])
        not_seen_courses = courses
        request.user.course_to_see = None
        request.user.last_seen_course_date = None
        request.user.save()
   
    moods = Mood.objects.all()
    mood_max_value = max(mood.value for mood in moods )
    analysis = calculate_average_moods(manager, mood_max_value=mood_max_value)
    average_moods = analysis['average_moods']
    return render(request, 'core/manager/index.html', {
        'average_mood_freetime_percentage': round(analysis['freetime_mood_value_percentage']),
        'average_mood_workplace_percentage': round(analysis['workplace_mood_value_percentage']),
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_workplace': analysis['podium_moods_workplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_workplace_activities': analysis['activities_podium_count_workplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_workplace'])+1))),
        'courses': not_seen_courses[:6],
    })
# Login engine
def engine(request):
    return JsonResponse({
     's':  ''
     })


def login_user_from_token(request, token):
    try:
        decrypted = json.loads(decrypt(token))
        expiring_date = datetime.strptime(decrypted['expiring_time'], "%Y-%m-%d").date()
        if expiring_date > datetime.now().date():
            user = UserProfile.objects.get(email = decrypted['email'])
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'core/token_expired.html')
                
    except (InvalidToken, UserProfile.DoesNotExist):
        expiring_time = date.today() + timedelta(days=1)

        return JsonResponse(encrypt(str(json.dumps({
            'email':  token,
            'expiring_time' : expiring_time
        }, indent=4, sort_keys=True, default=str)
    )),safe=False)




def decrypt(plain): 
    return Fernet(key).decrypt(plain.encode()).decode('utf-8')

def encrypt(plain): 
    return Fernet(key).encrypt(plain.encode()).decode('utf-8')

def send_contact_email(request):
    if request.POST:
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phonenumber = request.POST.get('phonenumber', None)
        message = request.POST.get('message', None)
        ContactEmail.objects.create(
            name = name,
            email = email,
            phonenumber = phonenumber,
            message = message
        )
        EmailMessage("Email from happycurus.de", "User: "+ email + 
                            '\n phonenumber: '+ phonenumber +
                            '\n name: ' + name +
                             '\n\n\n says: \n' + message, to=[CONTACT_EMAILS_RECEIVER]).send()
    return redirect('/')


