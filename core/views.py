from django.shortcuts import render, redirect
from django.http import JsonResponse
import os, base64, json, random
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
import datetime
from django.db.models import IntegerField, Value
from django.shortcuts import get_object_or_404
from django.utils import translation
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
    date_to_evaulate = datetime.date(year=int(request.GET['year']), 
                                              month=int(request.GET['month']), 
                                              day=int(request.GET['day'])) 
    mood_max_value = max(mood.value for mood in moods )

    analysis = calculate_average_moods(manager, mood_max_value=mood_max_value, end_day=date_to_evaulate)
    average_moods = analysis['average_moods']
    return render(request, 'core/manager/statistics.html', {
        'average_mood_freetime_percentage': round(analysis['freetime_mood_value_percentage']),
        'average_mood_marketplace_percentage': round(analysis['marketplace_mood_value_percentage']),
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_marketplace': analysis['podium_moods_marketplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_marketplace_activities': analysis['activities_podium_count_marketplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_marketplace'])+1)))

    })

def statistics_manager(request, manager):
    moods = Mood.objects.all()
    mood_max_value = max(mood.value for mood in moods )
    analysis = calculate_average_moods(manager, mood_max_value=mood_max_value)
    average_moods = analysis['average_moods']
    return render(request, 'core/manager/statistics.html', {
        'average_mood_freetime_percentage': round(analysis['freetime_mood_value_percentage']),
        'average_mood_marketplace_percentage': round(analysis['marketplace_mood_value_percentage']),
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_marketplace': analysis['podium_moods_marketplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_marketplace_activities': analysis['activities_podium_count_marketplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_marketplace'])+1)))

    })
def calculate_average_moods(manager, end_day=None, start_day=None, mood_max_value = 8):
    if start_day and end_day :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__gte=start_day, created_at__lte=end_day)
    elif start_day and not end_day :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__gte=start_day)
    elif not start_day and end_day :
        toughts = Tought.objects.filter(employee__team__manager=manager, created_at__lte=end_day)
    else :
        toughts = Tought.objects.filter(employee__team__manager=manager)
    

    average_moods = []
    count = 0
    average_mood_value_freetime      = .0
    average_mood_value_marketplace   = .0

    freetime_toughts = [t for t in toughts if t.tought_type == FREETIME ]
    marketplace_toughts = [t for t in toughts if t.tought_type == MARKET_PLACE ]

    moods = Mood.objects.all()
    moods_count = {}
    dates = []
    for mood in moods:
        moods_count[mood.value] = 0
    for t in freetime_toughts:
        dates.append( datetime.date(t.created_at.year, t.created_at.month, t.created_at.day) )
        moods_count[t.mood.value] += 1
    
    podium_moods_freetime = sorted([{'mood': key, 'count' : value } for key,value in moods_count.items()],key=lambda x: x['count'], reverse=True)

    activities_for_podium_moods = flat([ tought.activities.all().annotate(mood=Value(tought.mood.pk, output_field=IntegerField())).values('name','i18n_key', 'mood') for tought in freetime_toughts if tought.mood.value in [ p['mood'] for p in podium_moods_freetime] ])[:6]
    
    activity_count_freetime = []
    for mood in moods:
        #max number of activity displayed
        activities = [activity for activity in activities_for_podium_moods if activity['mood'] == mood.pk][:MAX_NUMBER_DISPLAYED]
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
    for t in marketplace_toughts:
        moods_count[t.mood.value] += 1
        
    
    podium_moods_marketplace = sorted([{'mood': key, 'count' : value } for key, value in moods_count.items()], key=lambda x: x['count'], reverse=True)[:3]

    activities_for_podium_moods = flat([ tought.activities.all().annotate(mood=Value(tought.mood.pk, output_field=IntegerField())).values('name','i18n_key', 'mood') for tought in marketplace_toughts if tought.mood.value in [ p['mood'] for p in podium_moods_marketplace] ])[:6]
    activity_count_marketplace = []
    for mood in moods:
        #max number of activity displayed
        activities = [ activity for activity in activities_for_podium_moods if activity['mood'] == mood.pk][:MAX_NUMBER_DISPLAYED]
        if len(activities) > 0:
            activity_count_marketplace.append({
                'mood_value': mood.value,
                'mood_icon': mood.icon.name,
                'mood_color_code': mood.color_code,
                'mood_i18n_key': mood.i18n_key,
                'activities': activities
            })




    for date in set(dates):

        average_mood_freetime = calculate_average_mood_for_day(date, toughts, FREETIME)
        average_mood_marketplace = calculate_average_mood_for_day(date, toughts, MARKET_PLACE)
        average_mood_value_freetime += average_mood_freetime / mood_max_value
        average_mood_value_marketplace += average_mood_marketplace / mood_max_value
        count += 1
        freetime_counts = get_mood_count_for_date(date, toughts, FREETIME)
        marketplace_counts = get_mood_count_for_date(date, toughts, MARKET_PLACE)
        
        average_moods.append({
            'date' : date,
            'average_mood_freetime' : average_mood_freetime,
            'average_mood_marketplace' : average_mood_marketplace,
            'moods' : {
                'freetime_moods_count': freetime_counts,
                'marketplace_moods_count': marketplace_counts
            }
        })


    return {
        'freetime_mood_value_percentage' : (average_mood_value_freetime / count) * 100,
        'marketplace_mood_value_percentage' : (average_mood_value_marketplace/ count) * 100,
        'average_moods' : sorted(average_moods, key=lambda x: x['date'], reverse=False),
        'podium_moods_freetime' : podium_moods_freetime,
        'activities_podium_count_freetime': activity_count_freetime,
        'podium_moods_marketplace' : podium_moods_marketplace,
        'activities_podium_count_marketplace': activity_count_marketplace,
    }




def get_mood_count_for_date(date, toughts, for_type):
    moods = {}
    for mood in Mood.objects.all():
        moods[mood.value] = 0
    for tought in filter(lambda t: same_day(t.created_at,date), toughts):
        if(tought.tought_type == for_type):
            moods[tought.mood.value] += 1

    return moods


def calculate_average_mood_for_day(date, toughts, for_type):
    count = 0
    moods = 0

    for tought in filter(lambda t: same_day(t.created_at, date), toughts):

        if tought.tought_type == for_type:
            count += 1
            moods += tought.mood.value

    return moods/count if count > 0 else 1




def e_learning_manager(request, manager):
    courses = list(Course.objects.filter(language__iexact=translation.get_language()))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    if len(not_seen_courses) == 0:
        request.user.seen_courses.set([])
        not_seen_courses = courses
        request.user.course_to_see = None
        request.user.last_seen_course_date = None
        request.user.save()


    if request.user.has_to_get_new_course():
        not_seen_course = random.sample(not_seen_courses, len(not_seen_courses))
        course_to_see = not_seen_courses[0]
        request.user.course_to_see = course_to_see
        request.user.last_seen_course_date =  datetime.datetime.now()
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
    courses = list(Course.objects.filter(language__iexact=translation.get_language()))
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
        'marketplace_toughts' : filter( lambda t : t['tought_type'] == MARKET_PLACE, toughts),
        'courses': not_seen_courses[:2],
    })


def statistics_employee(request, employee):
    toughts = [ tought.to_public_dict() for tought in Tought.objects.filter(employee = employee).order_by('created_at') ]
    moods = Mood.objects.all()
    return render(request, 'core/employee/statistics.html', {
        'moods' : moods,
        'toughts' : filter( lambda t : t['tought_type'] == FREETIME, toughts),
        'marketplace_toughts' : filter( lambda t : t['tought_type'] == MARKET_PLACE, toughts)
    })





def e_learning_employee(request, employee):
    courses = list(Course.objects.filter(language__iexact=translation.get_language()))
    not_seen_courses = list(filter(lambda c: c not in request.user.seen_courses.all(), courses))
    if len(not_seen_courses) == 0:
        request.user.seen_courses.set([])
        not_seen_courses = courses
        request.user.course_to_see = None
        request.user.last_seen_course_date = None
        request.user.save()


    if request.user.has_to_get_new_course():
        not_seen_course = random.sample(not_seen_courses, len(not_seen_courses))
        course_to_see = not_seen_courses[0]
        request.user.course_to_see = course_to_see
        request.user.last_seen_course_date =  datetime.datetime.now()
        # request.user.seen_courses.add(course_to_see)
        request.user.save()
    else:
        course_to_see = request.user.course_to_see


    courses_check_list = []
    for c in courses:
        if c.pk != course_to_see.pk:
            courses_check_list.append({
                'seen' : c in request.user.seen_courses.all(),
                'course': c
            })
    return render(request, 'core/employee/e_learning.html', {
        'courses': sorted(courses_check_list, key=lambda c: c['seen'], reverse=True),
        'course_to_see': course_to_see
    })


def e_learning_detail(request,id):
    course = Course.objects.get(pk=id)
    if course not in request.user.seen_courses.all():
        request.user.seen_courses.add(course)
    if request.user.course_to_see and request.user.course_to_see == course.pk:
        request.user.course_to_see = None

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

        activity = Activity.objects.create(
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
            'marketplace_available_choose':  filter( lambda a : a.activity_type == MARKET_PLACE, default_activity_choose),
            'team_marketplace_available_choose':  filter( lambda a : a.activity_type == MARKET_PLACE, team_activity_choose),

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

def statistics_for_day(request):
    toughts = [t.to_public_dict() for t in Tought.objects.filter(
        created_at__day__lte=request.GET['day'],
        created_at__month__lte=request.GET['month'],
        created_at__year__lte=request.GET['year'],
        employee__email = request.user.email
    ).order_by('created_at')]
        
    moods = Mood.objects.all()
    return render(request, 'core/employee/statistics.html', {
        'moods' : moods,
        'toughts' : filter( lambda t : t['tought_type'] == FREETIME, toughts),
        'marketplace_toughts' : filter( lambda t : t['tought_type'] == MARKET_PLACE, toughts)
    })

@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        #freetime
        employee = Employee.objects.get(email = request.user.email)
        employee.last_seen_survey = datetime.datetime.now()
        employee.save()
        mood = Mood.objects.get(pk=request.POST['freetime[selected_mood]'])


        sentences = list(EncouragingSentence.objects.exclude(pk__in= request.user.read_encouraging_sentences.all().values('pk')))

        if len(sentences) == 0:
            daily_quote = EncouragingSentence.objects.first()
            request.user.read_encouraging_sentences.set([daily_quote])
        else:
            daily_quote = random.sample(sentences, len(sentences))[0]
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


        ### marketplace
        employee = Employee.objects.get(email = request.user.email)
        employee.last_seen_survey = datetime.datetime.now()
        employee.save()
        mood = Mood.objects.get(pk=request.POST['marketplace[selected_mood]'])
        activities = Activity.objects.filter(pk__in=request.POST.getlist('marketplace[activities][]'))
        tought = Tought.objects.create(  
                        tought_type=MARKET_PLACE,
                        mood=mood,
                        motivational_quote=daily_quote,
                        text=request.POST['marketplace[current_tought]'],
                        employee=employee
                        )
        if activities and len(activities) > 0:
            tought.activities.add(*activities)



        return JsonResponse({
          'status' : 200,
          'motivational_quote' : model_to_dict(daily_quote)
        })
    return None


def home(request):
    user, is_employee = get_employee_from_request_user(request.user)

    return check_survey(home_employee, request, user) if is_employee else home_manager(request, user)

def statistics(request):
    user, is_employee = get_employee_from_request_user(request.user)
    return check_survey(statistics_employee, request, user) if is_employee else statistics_manager(request, user)


#TODO: uncomment right query
def happy_corus(request):
    #curus = Curus.objects.get(language=request.user.preferred_language)
    curus = Curus.objects.get(language__iexact= translation.get_language())
    return render(request, 'core/employee/happy_curus.html', {
        'curus': curus,
    })
    
    
    # return check_survey(happy_curus_employee, request, user) if is_employee else  happy_curus_manager(request, user)

def e_learning(request):
    user, is_employee = get_employee_from_request_user(request.user)
    return check_survey(e_learning_employee, request, user) if is_employee else e_learning_manager(request, user)


   


def home_manager(request, manager):
    courses = list(Course.objects.filter(language__iexact=translation.get_language()))
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
        'average_mood_marketplace_percentage': round(analysis['marketplace_mood_value_percentage']),
        'average_moods': average_moods,
        'podium_moods_freetime': analysis['podium_moods_freetime'],
        'podium_moods_marketplace': analysis['podium_moods_marketplace'],
        'podium_moods_freetime_activities': analysis['activities_podium_count_freetime'],
        'podium_moods_marketplace_activities': analysis['activities_podium_count_marketplace'],
        'moods' : moods,
        'best_mood_counts' : list(range(1, max(len(analysis['activities_podium_count_freetime']) +1 ,len(analysis['activities_podium_count_marketplace'])+1))),
        'courses': not_seen_courses[:2],
    })
# Login engine
def engine(request):
    return JsonResponse({
     's':  encrypt('sara cannella')
    })


def login_user_from_token(request, token):
    try:
        decrypted_email = decrypt(token)
        user = UserProfile.objects.get(email = decrypted_email)
        login(request, user)
        return redirect('/')
    except (InvalidToken, UserProfile.DoesNotExist):
        return JsonResponse({
            'info_cripted':  encrypt(token)
        })




def decrypt(plain): 
    return Fernet(key).decrypt(plain.encode()).decode('utf-8')

def encrypt(plain): 
    return Fernet(key).encrypt(plain.encode()).decode('utf-8')






